import json
import pandas as pd
import numpy as np
from uuid import uuid4
import psycopg2
from sqlalchemy import create_engine
import io
import time
import joblib
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.compose import ColumnTransformer
from sklearn.metrics import mean_absolute_error


##### IMPORTANT #######
# THIS FILE SHOULD NOT BE RUN IF THERE IS THE DATA IS ALREADY THERE IN THE DATABSE
#######################


# The JSON FILE is available at: https://www.dropbox.com/s/8d3ai5gvcs36vlr/listings_coord.json?dl=0
# It is a 1.8GB file, over 110k rows and 200+ fields
# Note Rana didn't upload to Github due to the huge size.


def reading_json(file_name, needed_columns):
    begin = '{"foo": ['
    end = ']}'
    with open(file_name, encoding='cp1252') as json_file:
        a = json_file.read()
        b = a.replace('}{"success"', '},{"success"')
        fixed_json_file = begin + b + end
        raw_data = json.loads(fixed_json_file)
    print ('loaded data successfully. Now converting to Pandas Datafframe...')
    data_list = []
    for every200 in range(len(raw_data['foo'])):
        for i in range(len(raw_data['foo'][every200]['bundle'])):
            row = []
            for field in needed_columns:
                row.append(raw_data['foo'][every200]['bundle'][i][field])
            data_list.append(row)
    data = pd.DataFrame(data_list, columns=needed_columns)
    print ('converted to Pandas Dataframe successfully.')
    return data


def clean_home_sale_data(data):

    # converting coordinates into two columns (latitude and longitude), then removing the coordinates column
    dataCopy = data.copy()

    print ('before the cleaning: ', data.shape)

    lat = []
    long = []
    for i in dataCopy['Coordinates']:
        if i is None:
            lat.append(np.nan)
            long.append(np.nan)
        elif i[0] == -1 and i[1] == -1:
            lat.append(np.nan)
            long.append(np.nan)
        else:
            lat.append(i[1])
            long.append(i[0])

    dataCopy['latitude'] = lat
    dataCopy['Longitude'] = long
    dataCopy = dataCopy.drop(columns=['Coordinates'])

    # converting the levels into the correct format.
    lvl = []
    for i in dataCopy.Levels:
        if len(i) == 0:
            lvl.append(None)
        else:
            lvl.append(i[0])
    dataCopy['Levels'] = lvl

    # dropping duplicates
    duplicated_row = dataCopy.duplicated()
    no_duplicate = dataCopy[[not i for i in duplicated_row]].reset_index(drop=True)

    print ('After Dropping all duplicates: ', no_duplicate.shape)

    # there is only one data point with no date, so I set it to 2019
    no_duplicate.loc[[i is None for i in no_duplicate.ListingContractDate], 'ListingContractDate'] = '2019-01-01'
    # get the max date of the duplicated address
    latest_data = no_duplicate[no_duplicate.groupby(['UnparsedAddress']).ListingContractDate.transform('max') == no_duplicate['ListingContractDate']]
    latest_data = latest_data.reset_index(drop=True)

    print('After Dropping all old records: ', latest_data.shape)

    bathrooms = []
    for i in latest_data.BathroomsTotalDecimal:
        if i == 0:
            bathrooms.append(np.nan)
        else:
            bathrooms.append(i)
    latest_data['BathroomsTotalDecimal_2'] = bathrooms
    data_with_important_feature = latest_data.dropna(subset=['LivingArea', 'BedroomsTotal', 'BathroomsTotalDecimal_2'], how='all')
    data_with_important_feature = data_with_important_feature.drop(columns=['BathroomsTotalDecimal_2']).reset_index(drop=True)

    print('After Dropping data without Sqft, Bedrooms, and Bathrooms: ', data_with_important_feature.shape)

    # eliminating listing price <= 10000
    data_larger_than_10k = data_with_important_feature.loc[data_with_important_feature.ListPrice > 10000, ]
    # keeping the city to Austin only
    data_austinOnly = data_larger_than_10k.loc[data_larger_than_10k.City == 'Austin',]
    # eliminating Sqft <= 100 sqft.
    data_austinOnly = data_austinOnly.loc[data_austinOnly.LivingArea > 100, ].reset_index(drop=True)

    # cleaning association fees (HOA)
    data_austinOnly.AssociationFee = data_austinOnly.AssociationFee.fillna(value=0)

    print('After limiting to Austin Only, removing listing price <= 10000 or sqft <= 100: ', data_austinOnly.shape)

    return data_austinOnly


file_name = 'listings_coord.json'

needed_columns = ['UnparsedAddress', 'City', 'PostalCode', 'ListingId', 'MlsStatus',
                  'ListingContractDate', 'ListPrice', 'LivingArea', 'LotSizeArea',
                  'BedroomsTotal', 'BathroomsTotalDecimal', 'CoveredSpaces', 'AssociationFee',
                  'CoolingYN', 'HeatingYN', 'FireplacesTotal', #'Cooling', 'Heating',
                  'TaxAnnualAmount', 'PropertySubType', 'Levels', 'WaterfrontYN', 'YearBuilt',
                  'Coordinates']

data = reading_json(file_name, needed_columns)

data_database = clean_home_sale_data(data)

# Renaming the columns
data_database = data_database.rename(columns={'UnparsedAddress':'ADDRESS',
                              'BathroomsTotalDecimal':'BathroomsTotal',
                              'CoolingYN':'Cooling',
                              'HeatingYN':'Heating',
                              'WaterfrontYN':'Waterfront',
                              'TaxAnnualAmount': 'AnnualTaxAmount'})

# Adding UUID to the data
for name in data_database['ADDRESS'].unique():
    data_database.loc[data_database['ADDRESS'] == name, 'UUID'] = uuid4()

# Genreating rental values, which will drop data with NAs in subset_columns
subset_columns = ['BedroomsTotal', 'BathroomsTotal', 'LivingArea', 'latitude', 'Longitude', 'CoveredSpaces']
data_database = data_database.dropna(subset = subset_columns)
df_features = data_database[subset_columns]
df_features.columns = ['bedrooms', 'bathrooms', 'sqft', 'latitude', 'longitude', 'parking']
model = joblib.load("knn.joblib")
data_database['RentValue'] = model.predict(df_features)

# In case the code throws an error when loading the model, the data is available on Github as with_rent_value.csv
rental_value_data = data_database
# r_path = 'with_rent_value.csv'
# rental_value_data = pd.read_csv(r_path)

def convert_to_string(data):
    for col_name in data.columns:
        if data[col_name].dtype != object:
            data[col_name] = data[col_name].apply(str)

convert_to_string(rental_value_data)

# replace all other NAs to empty string
rental_value_data = rental_value_data.replace('nan','',regex=True)


# reference: https://stackoverflow.com/questions/53889416/how-to-speed-up-pandas-to-sql-function
def bulk_insert_sql_replace(engine, df, table, sep='\t', encoding='utf8'):
    output = io.StringIO()
    df.to_csv(output, sep=sep, index=False, header=False, encoding=encoding)
    output.seek(0) # skip the first row,(header)
    print('step 1..')
    # Create Connection to the database
    connection = engine.raw_connection()
    cursor = connection.cursor()
    # Insert data fomr "output" to the table
    cursor.copy_from(output, table, sep=sep, null='')
    connection.commit()
    cursor.close()

# Insert your Engine here:
engine = create_engine("postgresql+psycopg2://redia:redia2020@redia.cnkeaub0nijl.us-east-1.rds.amazonaws.com/postgres") # Example: "postgresql+psycopg2://xxx:xxxxx@xxxx.com/postgres"
try:
    bulk_insert_sql_replace(engine, rental_value_data, '"HOME_SALE_INFO_STG"')
except (Exception, psycopg2.Error) as error:
    print ("Error while connecting to PostgreSQL", error)
finally:
    #closing database connection.
    """
        if(connection):
            cursor.close()
            connection.close()
    """

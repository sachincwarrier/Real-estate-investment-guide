import numpy as np
import pandas as pd


def string_to_numeric(string, data):
    data[string] = pd.to_numeric(data[string], errors='coerce') # if it contains non-numeric character, it becomes NAs


def clean_rental_data(data):

    # handling dollar sign, thousand separator, and extra non-numeric character
    data['price'] = data['price'].str.replace('$','')
    data['price'] = data['price'].str.replace(',','')
    data['price'] = data['price'].str.extract('(\d+)', expand=False)
    data['price'] = pd.to_numeric(data['price'])

    data['zestimate'] = data['zestimate'].str.replace('$','')
    data['zestimate'] = data['zestimate'].str.replace(',','')
    data['zestimate'] = data['zestimate'].str.extract('(\d+)', expand=False)
    data['zestimate'] = pd.to_numeric(data['zestimate'])

    data['price/sqt'] = data['price/sqt'].str.replace('$','')
    data['price/sqt'] = data['price/sqt'].str.replace(',','')
    data['price/sqt'] = data['price/sqt'].str.extract('(\d+)', expand=False)
    data['price/sqt'] = pd.to_numeric(data['price/sqt'])

    data['sqft'] = data['sqft'].str.replace(',', '')
    data['sqft'] = data['sqft'].str.extract('(\d+)', expand=False)
    data['sqft'] = pd.to_numeric(data['sqft'])

    # from collections import Counter
    data['cooling'] = data['cooling'].str.replace(r'Central.*','Central')
    data['cooling'] = data['cooling'].str.replace('Wall', 'Other')
    data['cooling'] = data['cooling'].str.replace('Contact manager', 'Other')
    data.loc[data.cooling == 'None', 'cooling'] = np.nan
    # Counter(data['cooling'])

    data['heating'] = data['heating'].str.replace(r'Forced air.*', 'Forced air')
    data.loc[((data.heating.notnull()) & (data.heating != 'Forced air')), 'heating'] = 'Other'
    # Counter(data['heating'])

    data['cat'] = 0
    data['dog'] = 0
    data.loc[data['pets'].str.match(r'Cat.*', na=False), 'cat'] = 1
    data.loc[data['pets'].str.match(r'.*dog.*', na=False), 'dog'] = 1

    data.laundry = data.laundry.str.replace(r'In Unit.*', 'In Unit')
    data.loc[data.laundry == 'None','laundry'] = np.nan
    # Counter(data['laundry'])

    data.parking = data['parking'].str.extract('(\d+)', expand=False)
    data.parking  = pd.to_numeric(data.parking)

    string_to_numeric('latitude', data)
    string_to_numeric('longitude', data)


def data_prelimary_check(data, return_data_without_duplicated=False):
    # this function will read the data and check for any duplicated rows.
    # It also checks for any NA values in the dataset (if
    # return_data_without_duplicated = False, it usees before removing duplicated),
    # otherwise it uses the new data. When return_data_without_duplicated is True
    # (default = False), it will return the new dataset with the duplicated records removed.

    duplicated_row = data.duplicated()
    print(round(sum(duplicated_row) * 100 / len(data), 2),
          '% records are duplicated.')

    data_step1 = data[[not i for i in duplicated_row]].reset_index(drop=True)
    if return_data_without_duplicated:
        print('Number of NAs and their distribution: ')
        print('Total Records (rows): ', len(data_step1))
        print(data_step1.isnull().sum(axis=0))
        return data_step1
    else:
        print('Number of NAs and their distribution: ')
        print('Total Records (rows): ', len(data))
        print(data.isnull().sum(axis=0))
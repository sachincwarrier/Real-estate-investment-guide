import pandas as pd
import data_cleaning
import numpy as np



### Rental Data
#######################################
# path = 'data_rentals.csv'

# data = pd.read_csv(path, header= None)

rental_data.columns = ['address', 'bathrooms', 'bedrooms', 'price', 'sqft',
                'url', 'id', 'zestimate', 'type', 'cooling' , 'heating' ,
                'pets' , 'laundry' , 'parking', 'deposit' , 'price/sqt' ,
                'walk_score' , 'transit_score' ,'latitude', 'longitude']


rental_data_cleaning = rental_data.loc[rental_data['bathrooms'].notnull(),]
rental_data_cleaning = rental_data_cleaning.reset_index(drop=True)


data_cleaning.data_prelimary_check(rental_data_cleaning)
data_cleaning.clean_rental_data(rental_data_cleaning)

rental_cleaned_result = rental_data_cleaning[['id', 'bedrooms', 'bathrooms', 'sqft', 'latitude', 'longitude',
            'cat', 'dog', 'parking', 'cooling', 'heating', 'zestimate', 'type', 'laundry',
            'price']]

rental_cleaned_result.dtypes

# writing_path = 'cleaned_reantal_data.csv'
# result.to_csv(path_or_buf=writing_path, index=False)
#######################################

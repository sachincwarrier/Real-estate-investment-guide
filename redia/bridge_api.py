import requests
import json
import time
import timeit
import pickle
import lxml
import json
import re
from bs4 import BeautifulSoup
import zillow_functions as zl
from bs4 import Comment
import glob
import csv


def get_data_api(coord, offset):
	API_ENDPOINT = "https://api.bridgedataoutput.com/api/v2/abor_ref/listings"

	HEADERS = {
		'Content-Type': 'application/json'
	}
	PARAMS = {
		'access_token': '7c14f765c32f14a46650cb200112a6d7',
		'limit': '200',
		'near': coord,
		'offset': offset
	}

	return requests.get(url=API_ENDPOINT, headers=HEADERS, params=PARAMS).json()


# w = open('listings_coord.json', 'w', encoding='utf-8')

# for i in range(0, 357550, 200):
coord = {(-97.76266, 30.34719), (-97.89953, 30.368), (-97.94988, 30.37951), (-97.73979, 30.32171),
         (-97.83866, 30.42928), (-97.73603, 30.3538), (-97.74181, 30.27039), (-97.67991, 30.37318),
         (-97.7215, 30.26165), (-97.71723, 30.26481), (-97.85008, 30.23423), (-97.65627, 30.33478),
         (-97.73798, 30.27802), (-97.74048, 30.29267), (-97.80872, 30.19805), (-97.67711, 30.13166),
         (-97.7563, 30.4233), (-97.74333, 30.27026), (-97.70552, 30.39208), (-97.77125, 30.32637),
         (-97.63138, 30.29189), (-97.74222, 30.18843), (-97.80907, 30.29255), (-97.6532, 30.35617),
         (-97.75345, 30.40117), (-97.92, 30.2411), (-97.67318, 30.23524), (-97.75796, 30.13844), (-97.85597, 30.21543),
         (-97.75491, 30.35356), (-97.76227, 30.2239), (-97.72134, 30.23163), (-97.79619, 30.20665),
         (-97.70747, 30.38318), (-97.72584, 30.41344), (-97.86906, 30.33146), (-97.6824, 30.44914),
         (-97.86001, 30.25583), (-97.74186, 30.27037), (-97.72916, 30.30681), (-97.80127, 30.43158),
         (-97.73692, 30.28618), (-97.66701, 30.33451), (-97.79855, 30.27303), (-97.76498, 30.24302),
         (-97.71563, 30.36132), (-97.71605, 30.28872), (-97.84333, 30.46858), (-97.68463, 30.2737),
         (-97.7633, 30.28836), (-97.68728, 30.30836), (-97.61183, 30.24305), (-97.83169, 30.36473),
         (-97.88815, 30.18013), (-97.70416, 30.33253), (-97.76751, 30.29623), (-97.96462, 30.31976),
         (-97.72453, 30.3105), (-97.7321, 30.35298), (-97.73434, 30.2141), (-97.6852, 30.2514), (-97.69888, 30.3335),
         (-97.82547, 30.16936)}
# for c in coord:
# 	results = get_data_api(c, 0)
# 	i = 0
# 	while results['success']:
# 		json.dump(results, w)
# 		i += 200
# 		results = get_data_api(c, i)
#
# w.flush()
# w.close()
# f = open('listings_coord.json', 'r', encoding='utf-8')
# rest = json.load(f)
with open('listings_coord.json', "r") as f:
	contents = f.read()
	try:
		# ListingId = re.findall(r'(ListingId":(.*?),)', contents ,re.DOTALL)#.group().split(':')[1].strip('",').strip('"')
		ListingId = re.findall(r'("ListingId":(.*?),)', contents ,re.DOTALL)#.group().split(':')[1].strip('",').strip('"')
		# print(ListingId)
	except:
		longitude = "NA"
		# print(longitude)
listings =set()
count = 0
for l in ListingId:
	count+=1
	listings.add(l[0].split(":")[1].strip(",").strip('"').strip(' "'))
print(count)
print(len(listings))
# f.close()
# zip_rest_set = set()
# list_of_zip = rest[0]['ListingId']
# print(list_of_zip)


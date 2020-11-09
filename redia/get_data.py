import requests
import json
import time
import timeit
import pickle
import lxml
import json
from bs4 import BeautifulSoup
import zillow_functions as zl
from bs4 import Comment
import glob
import csv
import re


def get_data_api():
	API_ENDPOINT = "https://us-zipcode.api.smartystreets.com/lookup"

	HEADERS = {
		'Content-Type': 'application/json'
	}
	PARAMS = {
		'auth-id': '493b2a72-d081-ca2e-72b6-651a35a33288',
		'auth-token': 'Nf48XevqT0kfbf3kNtor',
		'city': 'austin',
		'state': 'texas'
	}

	return requests.get(url=API_ENDPOINT, headers=HEADERS, params=PARAMS).json()


def get_html(url):
	HEADERS = {
		'Content-Type': 'application/json'
	}
	return requests.get(url=url, headers=HEADERS).text


# def get_html_with_params(address):
#
# 	# match = req.term.match( / ^ (\d+)\s + (.{3, }) /);
# 	HEADERS ={
# 		'Content-Type': 'application/json'
# 	}
# 	url="https://travis.go2gov.net/cart/suggest"
# 	PARAMS = {
# 		'searchString': "Yucca Hill Dr, Austin, TX 78744",
# 		'streetNum': "4713",
# 		'withNumber': True
# 	}
#
# 	r = requests.get(url=url, headers=HEADERS, params=PARAMS)
# 	print(r.text)
# 	print(r.status_code)
# 	print(r.json())

def get_address_for_account_numbers():
	with open('account_numbers.csv', 'w') as taxes_file:
		w = csv.writer(taxes_file, quoting=csv.QUOTE_ALL)
		f = open("addresses_all.txt", 'r', encoding='utf-8')
		for address in f:
			taxes = []
			taxes.append(address.strip('\n'))
			taxes.append(get_account_numbers(address))
			w.writerow(taxes)
		f.close()


def get_account_numbers(address):
	HEADERS = {
		'Content-Type': 'application/json'
	}

	url = "https://travis.go2gov.net/cart/responsive/quickSearch.do?formViewMode=responsive&criteria.searchStatus=1&pager.pageSize=10&pager.pageNumber=1&criteria.heuristicSearch=" + address
	r = requests.get(url, headers=HEADERS)
	soup = BeautifulSoup(r.text, 'html.parser')
	set_url = set()

	try:
		for a in soup.find_all('a', href=True):
			if ("account=" in a['href']):
				set_url.add(a['href'])
		return set_url
	except (ValueError, IndexError):
		return "NA"


def get_tax_from_account_numbers():
	with open('taxes_info.csv', 'w') as taxes_info:
		w = csv.writer(taxes_info, quoting=csv.QUOTE_ALL)
		f = open("account_numbers.csv", 'r', encoding='utf-8')
		readCSV = csv.reader(f, delimiter=',')
		for a in readCSV:
			taxes_data = []
			taxes_data.append(a[0])
			if a[1] != 'set()':
				li = list(a[1].split(", "))
				for elt in li:
					account_number = elt.strip('{').strip('\'').strip('\'}')
					# get_tax_for_2019(account_number, a[0])
					taxes_data.append(get_tax_for_2019(account_number, a[0]))
			else:
				taxes_data.append("set()")
			w.writerow(taxes_data)

		f.close()


def get_tax_for_2019(account_number, address):
	HEADERS = {
		'Content-Type': 'application/json'
	}

	url = "https://travis.go2gov.net" + account_number
	r = requests.get(url, headers=HEADERS)
	soup = BeautifulSoup(r.text, 'html.parser')
	# print(soup)
	data = []
	same_address = False
	try:
		job_elems = soup.find_all('div', class_='three columns')
		for tag in job_elems:
			info = " ".join(tag.text.split())
			info = list(info.split("\n"))
			for l in info:
				if "Mailing Address" in l:
					# print(l[l.index('Address')+8:] + " ===  " + address)
					# data.append(l)
					if address.split(" ")[0] in l[l.index('Address') + 8:] and address.split(" ")[1].lower() in l[
					                                                                                            l.index(
						                                                                                            'Address') + 8:].lower():
						# print("same")
						same_address = True
		# print(address)
	except:
		data.append("NA info")

	if same_address:

		try:
			job_elems = soup.find_all('table', class_='u-full-width')
			for tag in job_elems:
				# print(" ".join(tag.text.split()))
				tax_info = " ".join(tag.text.split())
				year = tax_info[tax_info.index("Total") + 6:].split(" ")[0]
				data.append(year)
				year_amount = tax_info[tax_info.index("Total") + 6:].split(" ")[1]
				data.append(year_amount)
		except:
			data.append("NA year/amount")
		try:
			job_elems = soup.find_all('div', class_='three columns')
			for tag in job_elems:
				info = " ".join(tag.text.split())
				info = list(info.split("\n"))
				for l in info:
					if "Account#" in l:
						data.append(l)
					elif "Owner Name" in l:
						data.append(l)
					elif "Mailing Address" in l:
						data.append(l)
					elif "Legal Description" in l:
						data.append(l)

		except:
			data.append("NA info")
	return data


def parse_json_file(file_name):
	f = open(file_name, 'r', encoding='utf-8')
	rest = json.load(f)
	f.close()
	return rest


def parse_zip_code(json_obj, county_name):
	zip_rest_set = set()
	list_of_zip = json_obj[0]['zipcodes']
	for zip in list_of_zip:
		if zip['county_name'] == county_name:
			zip_rest_set.add(zip['zipcode'])

	return zip_rest_set
def parse_coord(json_obj, county_name):
	zip_rest_set = set()
	list_of_zip = json_obj[0]['zipcodes']
	for zip in list_of_zip:
		if zip['county_name'] == county_name:
			str = zip['longitude'],zip['latitude']
			zip_rest_set.add(str)

	return zip_rest_set


# def get_addresses(zipcode):
# 	URL = "https://www.zillow.com/homes/" + zipcode
# 	zillow_page = requests.get(URL)
# 	soup = BeautifulSoup(zillow_page.content, 'html.parser')
#
# 	job_elems = soup.find_all('article', class_='list-card-addr')
# 	# print(soup)
# 	for job_elem in job_elems:
# 		print(job_elem, end='\n' * 2)

def get_addresses_from_html(zipcode):
	to_write = 'addresses_' + zipcode + '.txt'
	w = open(to_write, 'w', encoding='utf-8')
	filename = "html/" + zipcode + '_Zillow.html'
	with open(filename, "r") as f:
		contents = f.read()
		soup = BeautifulSoup(contents, 'lxml')
		tags = soup.find_all(['address', 'list-card-addr'])

		for tag in tags:
			w.write(" ".join(tag.text.split()))
			w.write('\n')
	f.close()
	w.close()


def get_price_from_html(zipcode):
	to_write = 'price_' + zipcode + '.txt'
	w = open(to_write, 'w', encoding='utf-8')
	filename = "html/" + zipcode + '_Zillow.html'
	with open(filename, "r") as f:
		contents = f.read()
		soup = BeautifulSoup(contents, 'lxml')
		tags = soup.find_all("div", class_="list-card-price")
		for tag in tags:
			w.write(" ".join(tag.text.split()))
			w.write('\n')
	f.close()
	w.close()


def get_more_info_from_html(zipcode):
	to_write = 'more_info_' + zipcode + '.txt'
	w = open(to_write, 'w', encoding='utf-8')
	filename = "html/" + zipcode + '_Zillow.html'
	with open(filename, "r") as f:
		contents = f.read()
		soup = BeautifulSoup(contents, 'lxml')
		tags = soup.find_all("ul", class_="list-card-details")
		for tag in tags:
			w.write(" ".join(tag.text.split()))
			w.write('\n')
	f.close()
	w.close()


def get_zillow_url_more_details(zipcode):
	to_write = 'detailed_url_' + zipcode + '.txt'
	w = open(to_write, 'w', encoding='utf-8')
	filename = "html/" + zipcode + '_Zillow.html'
	set_url = set()
	with open(filename, "r") as f:
		contents = f.read()
		soup = BeautifulSoup(contents, 'lxml')
		for a in soup.find_all('a', href=True):
			if ("homedetails" in a['href']):
				set_url.add(a['href'])
		# print("Found the URL:", a['href'])
		# 	tags = soup.find_all("a", class_="list-card-info")
		for url in set_url:
			w.write(url)
			w.write('\n')
	f.close()


def get_tax_info(address):
	URL = "https://www.zillow.com/homes/" + address
	zillow_page = requests.get(URL)
	soup = BeautifulSoup(zillow_page.content, 'html.parser')

	job_elems = soup.find_all('article', class_='list-card-addr')
	# print(soup)

	for job_elem in job_elems:
		print(job_elem, end='\n' * 2)


def get_tax_info_from_account_number(account_number):
	URL = "https://travis.go2gov.net/showPropertyInfo.do?account=" + account_number
	tax_page = requests.get(URL)
	soup = BeautifulSoup(tax_page.content, 'html.parser')
	# print(soup)
	job_elems = soup.find_all('td')[3::4]
	print(job_elems)


def get_data(filepath):
	# to_write = 'addresses_' + zipcode + '.txt'
	# w = open(to_write, 'w', encoding='utf-8')
	# filename = "zillow_data/73301/test.html"  #+ zipcode + '_Zillow.html'
	with open(filepath, "r") as f:
		contents = f.read()
		soup = BeautifulSoup(contents, 'lxml')
		# print(contents)


		# soup = BeautifulSoup(x[n], "lxml")
		new_obs = []

		# List that contains number of beds, baths, and total sqft (and
		# sometimes price as well).
		card_info = zl.get_card_info(soup)

		# Street Address
		new_obs.append(zl.get_street_address(soup))

		# Bathrooms
		new_obs.append(zl.get_bathrooms(card_info))

		# Bedrooms
		new_obs.append(zl.get_bedrooms(card_info))

		# Price
		new_obs.append(zl.get_price(soup))

		# Sqft
		new_obs.append(zl.get_sqft(card_info))

		# URL for each house listing
		url = zl.get_url(soup)
		new_obs.append(url)

		# Zipco
		new_obs.append(zl.get_id(url))

		new_obs.append(zl.get_zestimate(soup))
		new_obs.append(zl.get_year_built(soup))
		new_obs.append(zl.get_type(soup))

		new_obs.append(zl.get_cooling(soup))

		new_obs.append(zl.get_parking(soup))
		new_obs.append(zl.get_monthly(soup))

		new_obs.append(zl.get_principal_interest(soup))
		new_obs.append(zl.get_mortgage_insurance(soup))
		new_obs.append(zl.get_property_taxes(soup))
		new_obs.append(zl.get_home_insurance(soup))


		try:
			latitude = re.search(r'(latitude":(.*?),)', contents).group().split(':')[1].strip(',')
		except:
			latitude = "NA"
		new_obs.append(latitude)
		try:
			longitude = re.search(r'(longitude":(.*?)})', contents).group().split(':')[1].strip('}')
		except:
			longitude = "NA"
		new_obs.append(longitude)

	return new_obs


def get_url_rental_detail(file):
	filename = file
	with open(filename, "r") as f:
		contents = f.read()
		soup = BeautifulSoup(contents, 'lxml')
		tags = soup.find_all('a', class_='list-card-link')
		for tag in tags:
			print(tag['href'])
	f.close()


def get_data_rentals(filepath):
	# to_write = 'addresses_' + zipcode + '.txt'
	# w = open(to_write, 'w', encoding='utf-8')
	# filename = "zillow_data/73301/test.html"  #+ zipcode + '_Zillow.html'
	with open(filepath, "r") as f:
		contents = f.read()
		soup = BeautifulSoup(contents, 'lxml')
		# soup = BeautifulSoup(x[n], "lxml")
		new_obs = []

		# List that contains number of beds, baths, and total sqft (and
		# sometimes price as well).
		card_info = zl.get_card_info(soup)

		# Street Address
		new_obs.append(zl.get_street_address(soup))
		zl.get_address(soup)
		# Bathrooms
		new_obs.append(zl.get_bathrooms(card_info))

		# Bedrooms
		new_obs.append(zl.get_bedrooms(card_info))

		# Price
		new_obs.append(zl.get_price(soup))

		# Sqft
		new_obs.append(zl.get_sqft(card_info))

		# URL for each house listing
		url = zl.get_url1(soup)
		new_obs.append(url)

		# Zipco
		new_obs.append(zl.get_id(url))

		new_obs.append(zl.get_zestimate(soup))
		new_obs.append(zl.get_type(soup))

		new_obs.append(zl.get_cooling(soup))
		new_obs.append(zl.get_heating(soup))
		new_obs.append(zl.get_pets(soup))
		new_obs.append(zl.get_laundry(soup))

		new_obs.append(zl.get_parking(soup))
		new_obs.append(zl.get_deposit(soup))
		new_obs.append(zl.get_price_sqt(soup))

		new_obs.append(zl.get_walk_score(soup))
		new_obs.append(zl.get_transit_score(soup))

		try:
			latitude = re.search(r'(latitude":(.*?),)', contents).group().split(':')[1].strip(',')
		except:
			latitude = "NA"
		new_obs.append(latitude)
		try:
			longitude = re.search(r'(longitude":(.*?)})', contents).group().split(':')[1].strip('}')
		except:
			longitude = "NA"
		new_obs.append(longitude)

	return new_obs

if __name__ == '__main__':
	# results= get_data_api()
	# w = open('zip_list.json', 'w', encoding='utf-8')
	#
	# json.dump(results, w)0.
	# w.flush()
	# w.close()

	json_rest = parse_json_file('zip_list.json')
	zip_codes = parse_coord(json_rest, 'Travis')
	print(zip_codes)
	# for zip in zip_codes:
	# print('https://www.zillow.com/homes/'+ zip)
	# print('https://www.zillow.com/homes/for_rent/' + zip)

	# get_addresses_from_html(zip)
	# get_price_from_html(zip)
	# get_more_info_from_html(zip)
	# get_zillow_url_more_details(zip)
	# print("'address', 'bathrooms','bedrooms','price', 'sqft', 'url', 'id' 'zestimate', 'year built', 'type', 'cooling' ,'parking', 'Monthly cost', 'Principal & interest', 'Mortgage insurance', 'Property taxes' , 'Home insurance','latitude', 'longitude'")

	# get_tax_info("608 Bernstein St # 15, Austin, TX 78745")
	# get_tax_info_from_account_number("04241103160000")

###############################################################################################################################################
	# run this command to get data_rentals.csv for home sale
	# with open('data_rentals.csv', 'w') as myfile:
	# 	wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
	# 	print('address', 'bathrooms', 'bedrooms', 'price', 'sqft', 'url', 'id' 'zestimate', 'type', 'cooling' , 'heating' , 'pets' , 'laundry' , 'parking', 'deposit' , 'price/sqt' ,'walk_score' , 'transit_score' 'latitude', 'longitude')
	#
	# 	for filepath in glob.iglob('rent_details/*.html'):
	# 		print(get_data_rentals(filepath))
	# 		wr.writerow(get_data_rentals(filepath))
###############################################################################################################################################

###############################################################################################################################################
	# run this command to get data.csv for home sale
	# with open('data.csv', 'w') as myfile:
	# 	wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
	#
	# 	for filepath in glob.iglob('zillow_data/*/*.html'):
	# 		print(get_data(filepath))
	# 		wr.writerow(get_data(filepath))
###############################################################################################################################################

###############################################################################################################################################
# run this command to get all the urls details for rentals
# for filepath in glob.iglob('rent_listings//*.html'):
# 	if " 0 Rentals" not in filepath:
# 		get_url_rental_detail(filepath)
###############################################################################################################################################




###############################################################################################################################################
# run this command to get the details about rentals from their html

# # with open('data.csv', 'w') as myfile:
# # 	wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
# #
# 	for filepath in glob.iglob('zillow_data/*/*.html'):
# 	   get_data_rentals()
# # 		print(get_data(filepath))
# # 		wr.writerow(get_data(filepath))

###############################################################################################################################################

###############################################################################################################################################
# run this command to get addresses + set of account numbers from Travis county taxes website using address.txt containing all the addresses
# get_address_for_account_numbers()
###############################################################################################################################################

###############################################################################################################################################
# run this command to get taxes for 2019 from Travis county taxes website using the data in account_numbers.csv
# get_tax_from_account_numbers()
# get_tax_for_2019('/showPropertyInfo.do?account=04171004040000', '5908 Garden Oaks Dr, Austin, TX 78745')

###############################################################################################################################################

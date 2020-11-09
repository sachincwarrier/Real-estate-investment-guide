import re as re
import time
from bs4 import Comment

def get_listings(list_obj):
	# Split the raw HTML into segments, one for each listing.
	output = []
	for i in list_obj:
		htmlSplit = i.split('" id="zpid_')[1:]
		output += htmlSplit
	return (output)


def get_street_address(soup_obj):
	try:
		street = soup_obj.find(
			"h1", "ds-address-container").get_text().strip().replace('\xa0', ' ')
	except (ValueError, AttributeError):
		street = "NA"
	if len(street) == 0 or street == "null":
		street = "NA"
	if (street == "NA"):
		try:
			address = soup_obj.find(
				"h2", {"data-test-id": "bdp-building-address"}).get_text().strip()
		except IndexError:
			address = "NA"
		except (ValueError, AttributeError):
			address = "NA"
		if len(address) == 0 or address == 'null':
			address = "NA"

		if (address == "NA"):
			try:
				address = soup_obj.find(
					"div", {"data-test-id": "bdp-building-info"}).get_text()
			except IndexError:
				address = "NA"
			except (ValueError, AttributeError):
				address = "NA"
			if len(address) == 0 or address == 'null':
				address = "NA"

			if (address == "NA"):
				try:
					address = soup_obj.find(
						"h1", {"class": "zsg-h1"}).get_text()
				except IndexError:
					address = "NA"
				except (ValueError, AttributeError):
					address = "NA"
				if len(address) == 0 or address == 'null':
					address = "NA"
				else:
					return (address)
			else:
				return (address)
		else:
			return (address)

	else:
		return (street)




def get_address(soup_obj):
	try:
		address = soup_obj.find(
			"div", {"data-test-id": "bdp-building-info"}).get_text()
	except IndexError:
		address = "NA"
	except (ValueError, AttributeError):
		address = "NA"
	if len(address) == 0 or address == 'null':
		address = "NA"
	return (address)



def get_city(soup_obj):
	try:
		city = soup_obj.find(
			"span", {"itemprop": "addressLocality"}).get_text().strip()
	except (ValueError, AttributeError):
		city = "NA"
	if len(city) == 0 or city == "null":
		city = "NA"
	return (city)


def get_state(soup_obj):
	try:
		state = soup_obj.find(
			"span", {"itemprop": "addressRegion"}).get_text().strip()
	except (ValueError, AttributeError):
		state = "NA"
	if len(state) == 0 or state == 'null':
		state = "NA"
	return (state)


def get_zipcode(soup_obj):
	try:
		zipcode = soup_obj.find(
			"span", {"itemprop": "postalCode"}).get_text().strip()
	except (ValueError, AttributeError):
		zipcode = "NA"
	if len(zipcode) == 0 or zipcode == 'null':
		zipcode = "NA"
	return (zipcode)


def get_price(soup_obj):
	# Look for price within the BeautifulSoup object.
	try:
		price = soup_obj.find(
			"h3", {"class": "ds-price"}).get_text().strip()
	except (ValueError, AttributeError):
			price = 'NA'
	return (price)


def get_card_info(soup_obj):
	# For most listings, card_info will contain info on number of bedrooms,
	# number of bathrooms, square footage, and sometimes price.
	try:
		card = soup_obj.find(
			"h3", {"class": "ds-bed-bath-living-area-container"}).get_text().split(" · ")
	except (ValueError, AttributeError):
		card = "NA"
	if len(card) == 0 or card == 'null':
		card = "NA"
	return (card)


def get_sqft(list_obj):
	sqft = [n for n in list_obj if "sqft" in n]
	try:
		for n in list_obj:
			index = n.index("ba")
			sqft = n.split("sqft")[0].strip()[index + 2:]
	except (ValueError, IndexError):
		sqft = "NA"
	if sqft == 0:
		sqft = "NA"
	return (sqft)


def get_bedrooms(list_obj):
	beds = [n for n in list_obj if any(["bd" in n, "tudio" in n])]
	try:
		for n in list_obj:
			index = n.index("bd")
			beds = n.split("sqft")[0].strip()[:index]
	except (ValueError, IndexError):
		beds = "NA"
	if len(beds) > 0:
		if any([beds[0] == "Studio", beds[0] == "studio"]):
			beds = 0
			return (beds)
		try:
			beds = float(beds[0].split("bd")[0].strip())
		except (ValueError, IndexError):
			if any([beds[0] == "Studio", beds[0] == "studio"]):
				beds = 0
			else:
				beds = "NA"
	else:
		beds = "NA"
	return (beds)


def get_bathrooms(list_obj):
	baths = [n for n in list_obj if "ba" in n]
	try:
		for n in list_obj:
			index = n.index("ba")
			index1 = n.index("bd")
			baths = n.split("sqft")[0].strip()[index1+2:index]
	except (ValueError, IndexError):
		baths = "NA"
	if len(baths) > 0:
		try:
			baths = float(baths[0].split("ba")[0].strip())
		except (ValueError, IndexError):
			baths = "NA"
		if baths == 0:
			baths = "NA"
	else:
		baths = "NA"
	return (baths)


def get_days_on_market(soup_obj):
	try:
		dom = soup_obj.find_all(
			"span", {"class": "zsg-photo-card-notification"})
		dom = [n for n in dom if "illow" in n.get_text()]
		if len(dom) > 0:
			dom = dom[0].get_text().strip()
			dom = int(dom.split(" ")[0])
		else:
			dom = "NA"
	except (ValueError, AttributeError):
		dom = "NA"
	return (dom)


def get_sale_type(soup_obj):
	try:
		saletype = soup_obj.find(
			"span", {"class": "zsg-photo-card-status"}).get_text().strip()
	except (ValueError, AttributeError):
		saletype = "NA"
	if len(saletype) == 0 or saletype == 'null':
		saletype = "NA"
	return (saletype)


def get_zestimate(soup_obj):
	try:
		Zestimate = soup_obj.find("div","ds-chip-removable-content").get_text()
		Zestimate = Zestimate[Zestimate.index('$'):]

	except (ValueError, AttributeError):
		Zestimate = "NA"
	if len(Zestimate) == 0 or Zestimate == 'null':
		Zestimate = "NA"
	return (Zestimate)

def get_year_built(soup_obj):
	try:
		# year = soup_obj.find("li","ds-home-fact-list-item").get_text()
		year = soup_obj.findAll("li", {"class": "ds-home-fact-list-item"})[1].get_text()
		if ("Year built" in year):
			year = year[year.index(":")+1:]
		else:
			year = "NA"
	except IndexError:
		year = "NA"
	except (ValueError, AttributeError):
		year = "NA"
	if len(year) == 0 or year == 'null':
		year = "NA"
	return (year)

def get_type(soup_obj):
	try:
		# year = soup_obj.find("li","ds-home-fact-list-item").get_text()
		type = soup_obj.findAll("li", {"class": "ds-home-fact-list-item"})[0].get_text()
		if ("Type" in type):
			type = type[type.index(":")+1:]
		else:
			type = "NA"
	except IndexError:
		type = "NA"

	except (ValueError, AttributeError):
		type = "NA"
	if len(type) == 0 or type == 'null':
		type = "NA"
	if (type == "NA"):
		try:
			# year = soup_obj.find("li","ds-home-fact-list-item").get_text()
			type = soup_obj.findAll("li", {"class": "ds-home-fact-list-item"})[1].get_text()
			if ("Type" in type):
				type = type[type.index(":") + 1:]
			else:
				type = "NA"
		except IndexError:
			type = "NA"

		except (ValueError, AttributeError):
			type = "NA"
		if len(type) == 0 or type == 'null':
			type = "NA"
		return (type)
	else:
		return (type)


def get_cooling(soup_obj):
	try:
		# year = soup_obj.find("li","ds-home-fact-list-item").get_text()
		cooling = soup_obj.findAll("li", {"class": "ds-home-fact-list-item"})[3].get_text()
		if ("Cooling" in cooling):
			cooling = cooling[cooling.index(":")+1:]
		else:
			cooling = "NA"
	except IndexError:
		cooling = "NA"

	except (ValueError, AttributeError):
		cooling = "NA"
	if len(cooling) == 0 or cooling == 'null':
		cooling = "NA"

	if (cooling == "NA"):
		try:
			cooling = soup_obj.findAll("li", {"class": "ds-home-fact-list-item"})[2].get_text()
			if ("Cooling" in cooling):
				cooling = cooling[cooling.index(":") + 1:]
			else:
				cooling = "NA"
		except IndexError:
			cooling = "NA"

		except (ValueError, AttributeError):
			cooling = "NA"
		if len(cooling) == 0 or cooling == 'null':
			cooling = "NA"
		return (cooling)
	else:
		return (cooling)


def get_heating(soup_obj):
	try:
		heating = soup_obj.findAll("li", {"class": "ds-home-fact-list-item"})[3].get_text()
		if ("Heating" in heating):
			heating = heating[heating.index(":")+1:]
		else:
			heating = "NA"
	except IndexError:
		heating = "NA"

	except (ValueError, AttributeError):
		heating = "NA"
	if len(heating) == 0 or heating == 'null':
		heating = "NA"
	return heating

def get_pets(soup_obj):
	try:
		pets = soup_obj.findAll("li", {"class": "ds-home-fact-list-item"})[4].get_text()
		if ("Pets" in pets):
			pets = pets[pets.index(":")+1:]
		else:
			pets = "NA"
	except IndexError:
		pets = "NA"

	except (ValueError, AttributeError):
		pets = "NA"
	if len(pets) == 0 or pets == 'null':
		pets = "NA"
	return pets

def get_laundry(soup_obj):
	try:
		laundry = soup_obj.findAll("li", {"class": "ds-home-fact-list-item"})[6].get_text()
		if ("Laundry:" in laundry):
			laundry = laundry[laundry.index(":")+1:]
		else:
			laundry = "NA"
	except IndexError:
		laundry = "NA"

	except (ValueError, AttributeError):
		laundry = "NA"
	if len(laundry) == 0 or laundry == 'null':
		laundry = "NA"
	return laundry

def get_deposit(soup_obj):
	try:
		deposit = soup_obj.findAll("li", {"class": "ds-home-fact-list-item"})[7].get_text()
		if ("Deposit:" in deposit):
			deposit = deposit[deposit.index(":")+1:]
		else:
			deposit = "NA"
	except IndexError:
		deposit = "NA"

	except (ValueError, AttributeError):
		deposit = "NA"
	if len(deposit) == 0 or deposit == 'null':
		deposit = "NA"
	return deposit

def get_price_sqt(soup_obj):
	try:
		price_sqt = soup_obj.findAll("li", {"class": "ds-home-fact-list-item"})[8].get_text()
		if ("Price/sqft:" in price_sqt):
			price_sqt = price_sqt[price_sqt.index(":")+1:]
		else:
			price_sqt = "NA"
	except IndexError:
		price_sqt = "NA"

	except (ValueError, AttributeError):
		price_sqt = "NA"
	if len(price_sqt) == 0 or price_sqt == 'null':
		price_sqt = "NA"
	return price_sqt

def get_parking(soup_obj):
	try:
		parking = soup_obj.findAll("li", {"class": "ds-home-fact-list-item"})[4].get_text()
		if ("Parking" in parking):
			parking = parking[parking.index(":")+1:]
		else:
			parking = "NA"
	except IndexError:
		parking = "NA"

	except (ValueError, AttributeError):
		parking = "NA"
	if len(parking) == 0 or parking == 'null':
		parking = "NA"
	if (parking == "NA"):
		try:
			parking = soup_obj.findAll("li", {"class": "ds-home-fact-list-item"})[5].get_text()
			if ("Parking" in parking):
				parking = parking[parking.index(":") + 1:]
			else:
				parking = "NA"
		except IndexError:
			parking = "NA"

		except (ValueError, AttributeError):
			parking = "NA"
		if len(parking) == 0 or parking == 'null':
			parking = "NA"
		return parking
	else:
		return (parking)

def get_monthly(soup_obj):
	try:
		monthly_cost = soup_obj.find("div" , "ds-expandable-card").get_text()
		if ("Monthly cost" in monthly_cost):
			monthly_cost = monthly_cost[monthly_cost.index("Monthly cost$")+12:monthly_cost.index("Estimated monthly")]
		else:
			monthly_cost = "NA"
	except IndexError:
		monthly_cost = "NA"

	except (ValueError, AttributeError):
		monthly_cost = "NA"
	if len(monthly_cost) == 0 or monthly_cost == 'null':
		monthly_cost = "NA"
	return (monthly_cost)

def get_principal_interest(soup_obj):
	try:
		principal_interest = soup_obj.find("div" , "ds-expandable-card").get_text()
		if ("Principal" in principal_interest):
			principal_interest = principal_interest[principal_interest.index("interest$")+8:principal_interest.index("Mortgage")]
		else:
			principal_interest = "NA"
	except IndexError:
		principal_interest = "NA"

	except (ValueError, AttributeError):
		principal_interest = "NA"
	if len(principal_interest) == 0 or principal_interest == 'null':
		principal_interest = "NA"
	return (principal_interest)

def get_mortgage_insurance(soup_obj):
	try:
		mortgage_insurance = soup_obj.find("div" , "ds-expandable-card").get_text()
		if ("Mortgage insurance" in mortgage_insurance):
			mortgage_insurance = mortgage_insurance[mortgage_insurance.index("Mortgage insurance$")+18:mortgage_insurance.index("Property")]
		else:
			mortgage_insurance = "NA"
	except IndexError:
		mortgage_insurance = "NA"

	except (ValueError, AttributeError):
		mortgage_insurance = "NA"
	if len(mortgage_insurance) == 0 or mortgage_insurance == 'null':
		mortgage_insurance = "NA"
	return (mortgage_insurance)

def get_property_taxes(soup_obj):
	try:
		property_taxes = soup_obj.find("div" , "ds-expandable-card").get_text()
		if ("Property taxes" in property_taxes):
			property_taxes = property_taxes[property_taxes.index("Property taxes$")+14:property_taxes.index("Home insurance")]
		else:
			property_taxes = "NA"
	except IndexError:
		property_taxes = "NA"

	except (ValueError, AttributeError):
		property_taxes = "NA"
	if len(property_taxes) == 0 or property_taxes == 'null':
		property_taxes = "NA"
	return (property_taxes)

def get_home_insurance(soup_obj):
	try:
		home_insurance = soup_obj.find("div" , "ds-expandable-card").get_text()
		if ("Home insurance" in home_insurance):
			home_insurance = home_insurance[home_insurance.index("Home insurance$")+14:home_insurance.index("HOA")]
		else:
			home_insurance = "NA"
	except IndexError:
		home_insurance = "NA"

	except (ValueError, AttributeError):
		home_insurance = "NA"
	if len(home_insurance) == 0 or home_insurance == 'null':
		monthly_cost = "NA"
	return (home_insurance)



def get_url(soup_obj):
	# Try to find url in the BeautifulSoup object.
	href = [n["href"] for n in soup_obj.find_all("a", href=True)]
	for comments in soup_obj.findAll(text=lambda text: isinstance(text, Comment)):
		href = comments.extract()
		if ("url" in href):
			url = href[href.index('url:')+5:href.index('zpid/')+5]

	return (url)


def get_url1(soup_obj):
	try:
	# Try to find url in the BeautifulSoup object.
		href = [n["href"] for n in soup_obj.find_all("a", href=True)]
		for comments in soup_obj.findAll(text=lambda text: isinstance(text, Comment)):
			href = comments.extract()
			if "url" in href:
				url = href[href.index('url:')+5:href.index('/ ')]
	except IndexError:
		url = "NA"
	except (ValueError, AttributeError):
		url = "NA"
	return (url)



def get_id(url):
	try:
		zpid = url[:url.index("_zpid")]
		ind = zpid.rfind('/')
		zpid = zpid[ind+1:]
	except IndexError:
		zpid = "NA"
	except (ValueError, AttributeError):
		zpid = "NA"

	return zpid

def get_walk_score(soup_obj):
	try:
		walk_score = soup_obj.find("ul" , "zsg-list_inline neighborhood-scores").get_text()
		if ("Walk Score" in walk_score):
			walk_score = walk_score[walk_score.index("Walk Score")+14:walk_score.index("Transit Score")].strip().replace('\xa0', ' ')
		else:
			walk_score = "NA"
	except IndexError:
		walk_score = "NA"

	except (ValueError, AttributeError):
		walk_score = "NA"
	if len(walk_score) == 0 or walk_score == 'null':
		walk_score = "NA"
	return (walk_score)

def get_transit_score(soup_obj):
	try:
		transit_score = soup_obj.find("ul" , "zsg-list_inline neighborhood-scores").get_text()
		if ("Transit Score" in transit_score):
			transit_score = transit_score[transit_score.index("Transit Score")+15:].strip().replace('\xa0', ' ')
		else:
			transit_score = "NA"
	except IndexError:
		transit_score = "NA"

	except (ValueError, AttributeError):
		transit_score = "NA"
	if len(transit_score) == 0 or transit_score == 'null':
		transit_score = "NA"
	return (transit_score)

def close_connection(driver):
	driver.quit()

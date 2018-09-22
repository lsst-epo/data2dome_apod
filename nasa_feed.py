import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import date
import urllib.request
import re
import time
import json

#################################################################################
# Author: Christian Soto                                                        #
# Program Name: nasa_feed.py		                                        #
# Email: cjsoto@lsst.org or christian.j.sotoparra@gmail.com                     #
# Purpose: The purpose of this program is to scrape the website nasa.gov/images.#
#	   This current program is written and run on python3.  When running 	#
#	   this program, it is import that geckodriver.exe is currently in the 	#
#	   same directory or else it will return an error.			#
#################################################################################

def get_json(url, collection):

	#open url link
	webURL = urllib.request.urlopen(url)

	#parse the web page
	soup = BeautifulSoup(webURL, 'html.parser')

	#load json script string into a JSON object we can use
	new_data = json.loads(soup.script.string)

	#print(soup.prettify())
	collection["PublicationDate"] = new_data["@graph"][0]["datePublished"]
	collection["Title"] = new_data["@graph"][0]["headline"]
	collection["Credit"] = new_data["@graph"][0]["author"]["name"]

	print(collection)

#def getResourceImage(collection
def getCollections():

	#counter for tallying collections
	counter = 0;

	#list to store all the JSON data of collections.
	collections = []

	#options for headless mode
	options = Options()
	options.set_headless(headless=True)

	#open browser
	driver = selenium.webdriver.Firefox(firefox_options=options,executable_path=r'./geckodriver')

	#make url varaible to hold url
	url = "https://www.nasa.gov/multimedia/imagegallery/iotd.html"

	#load url
	driver.get(url)

	#Yamini Maddelawait until the button loads to load more images
	#try:
	element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "trending")))

    		#once the button loads, click it 16 times
	#	i =0
	#	while i <= 15:
 	#      		driver.find_element_by_xpath('//*[@id="trending"]').click()
  	#     		i += 1
       			#slow down the load to insure button loads correctly
   	#    		time.sleep(1)

	#click on the first card or picture
	driver.find_element_by_class_name('gallery-card:first-child').click()

	i = 0
	while i<= 3:

		#get the hreh link for current page
		date_url = driver.find_element_by_partial_link_text('View Image')

		#collection object
		collection = {}
		collection["Creator"] = "Nasa image of the Day"
		collection["URL"] = "https://nasa.gov"
		collection["ReferenceURL"] = url

		#new dictionary for contact information
		contact_JSON = {}
		contact_JSON["Name"] ="Robert Nemiroff"
		contact_JSON["Email"] = "nemiroff@mtu.edu"
		contact_JSON["Telephone"] = "1-906-487-2198"
		contact_JSON["Address"] = "1400 Townsend Drive"
		contact_JSON["City"] = "Houghton"
		contact_JSON["StateProvince"] = "Michigan"
		contact_JSON["PostalCode"] = "49931"
		contact_JSON["Country"] = "USA"

		#add contact_JSON object to collection Object
		collection["Contact"] = contact_JSON

		#get the description
		description = driver.find_element_by_tag_name('p')
		collection["Description"] = description.text

		#get the rest of the image collection
		get_json(date_url.get_attribute("href"), collection)

		#add current collection JSON object to collections list
		collections.append(collection)

		#after collectiong, click on the next button for next picture
		driver.find_element_by_class_name('flex-next').click()

		i+=1

	#close the driver
	driver.close()

	return{"collections":collections, "count":counter}

def main():

	#This dictionary will collect all the JSON data and stored here
	main_JSON = {}

	#Get APOD data for last 365 days
	nasa_data = getCollections()
	print(nasa_data)
	#This list will collect contact information and assets
	#main_JSON["Collections"] = nasa_data["collections"]

	#Number sources where JSON was collected
	#main_JSON["Count"] = nasa_data["count"]

	#This creates a new file where JSON data will be stored
	# with open("apod_v2.json", "w+") as outfile:
	#   json.dump(main_JSON, outfile)

#Run main
if __name__ == "__main__":
    main()


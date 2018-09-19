import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
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

def get_json(url):

	#open url link
	webURL = urllib.request.urlopen(url)

	#parse the web page
	soup = BeautifulSoup(webURL, 'html.parser')

	#load json script string into a JSON object we can use
	new_data = json.loads(soup.script.string)
	#print(new_data["@context"])
	print(new_data["@graph"][0]["datePublished"])
	print(new_data["@graph"][0]["image"]["url"])
	print(new_data["@graph"][0]["author"]["name"])
	print(new_data["@graph"][0]["headline"])

def main():
	#open browser
	driver = selenium.webdriver.Firefox(executable_path=r'./geckodriver')

	#options = Options();
	url = "https://www.nasa.gov/multimedia/imagegallery/iotd.html"
	#load url
	driver.get(url)

	#wait until the button loads to load more images
	#try:
	element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "trending")))

    		#once the button loads, click it 16 times
	#	i =0
	#	while i <= 15:
 	#      		driver.find_element_by_xpath('//*[@id="trending"]').click()
  	#     		i += 1
       			#slow down the load to insure button loads correctly
   	#    		time.sleep(1)

		#click on the first image
	#	time.sleep(1)
	#	images = driver.find_elements_by_tag_name('img')

	#	print(driver.find_elements_by_xpath("ember")

		#for image in images:
		#	print(image.get_attribute('src'))

	#click on the first card or picture
	driver.find_element_by_class_name('gallery-card:first-child').click()

	#get the hreh link for current page
	date_url = driver.find_element_by_partial_link_text('View Image')

	#print(date_url.get_attribute("href"))
	get_json(date_url.get_attribute("href"))

	#except:
 	#  	print("Some kind of error exception")

	driver.close()
#Run main
#if __name__ == " main ":
main()

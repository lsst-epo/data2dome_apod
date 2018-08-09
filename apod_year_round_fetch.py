#############################################################################################################
# Author: Christian Soto                                                                                    #
# Program Name: apod_year_round_fetch.py                                                                    #
# Email: cjsoto@lsst.org or christian.j.sotoparra@gmail.com                                                 #
# Purpose: The purpose of this program is fetch the JSON data from year round from the website              #
#          https://apod.nasa.gov/apod/astropix.html? starting from today's date.  This program is ran using #
#          python 3 and later versions.  If you need any earlier versions of python, be sure to import the  #
#          correct libraries and modules.  Some of the methods from earlier modules might have to be changed#
#          or renamed as well.  After the JSON data is collected, it will write it all to a file called     #
#          jsonData.txt.  If you find any bugs or need help, feel free to email me.  There is currently one #
#          bug in this code.  Making large request from one year to today will cause a 503 error, which is  #
#          a service unavailable.  This means the request is to large for the server side to handle.        #
#############################################################################################################

# modules needed to process internet, json data, and dates
from datetime import date
from datetime import timedelta
import datetime
import urllib.request
import json

#############################################################################################################
# Method: apiRangeDates                                                                                     #
# Parameters: startDate, endDate                                                                            #
# Returns: range of dates starting at startDate and ending at endDate                                       #
# Purpose: The purpose of this method is to return a range of dates that                                    #
#          begin at a year from today's date and ends at whatever todays date                               #
#          is.  We can use the this method to determine exactly which JSON data                             #
#          we are interested in gathering from the Astronomy picture of the day                             #
#          website by specifiying the exact date.  (E.G                                                     #
#          https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY&start_date=2017-07-05&end_date=2017-07-10)  #
#############################################################################################################

def apiRangeDates(startDate, endDate):
    for n in range(int ((endDate - startDate).days)+1):
        yield startDate + timedelta(n)

#############################################################################################################
# Method: isLeapYear                                                                                        #
# Parameters: year                                                                                          #
# Returns: True is year is a leap year or False if not                                                      #
# Purpose: The purpose of this method is to check if a year is a Leap year or not                           #
#############################################################################################################

def isLeapYear(endDate):

    if(endDate%400 == 0):
        return True
    elif(endDate%100 == 0):
        return False
    elif(endDate%4 == 0):
        return True
    else:
        return False

#############################################################################################################
# Method: prepend                                                                                           #
# Parameters: filename                                                                                      #
# Returns: NA                                                                                               #
# Purpose: The purpose of this method is to prepend the string line                                         #
#############################################################################################################
def addMainJSON():

    collections = {}
    collections["ID"] = "D2D_APOD"
    collections["URL"] = "http://www.data2dome.org/"
    collections["ReferenceURL"] = "https://apod.nasa.gov/"
    collections["Title"] = "Astronomy Picture of the Day"
    collections["Description"] = "The APOD archive contains the largest collection of annotated astronomical images on the internet."
    collections["PublicationDate"] = "2018-06-14T14:00:00"
    collections["Credit"] = "Robert Nemiroff and Jerry Bonnell"
    collections["Creator"] = "Robert Nemiroff and Jerry Bonnell"

    contact_JSON = {}
    contact_JSON ["Name"] = "Robert Nemiroff"
    contact_JSON["Email"] = "nemiroff@mtu.edu"
    contact_JSON["Telephone"] = "1-906-487-2198"
    contact_JSON["Address"] = "1400 Townsend Drive"
    contact_JSON["City"] = "Houghton"
    contact_JSON["StateProvince"] = "Michigan"
    contact_JSON["PostalCode"] = "49931"
    contact_JSON["Country"] = "USA"
    collections["Contact"] = contact_JSON

    #This will add the Assets lists to the collections list
    collections["Assets"] = addAssets()

    return collections

#############################################################################################################
# Method: addAssets                                                                                           #
# Parameters: filename                                                                                      #
# Returns: NA                                                                                               #
# Purpose: The purpose of this method is to prepend the string line                                         #
#############################################################################################################
def addAssets():

    asset_list = []
    # This will the variables that will be needed.  For now, only the last 3 days will be gathered for simple
    # and debugging purposes
    lastYear = date.today().year
    thisMonth = date.today().month
    thisDay = date.today().day - 2
    endDate = date.today()

    # Check for Leap years
    if(isLeapYear(endDate.year) and endDate.month == 2 and endDate.day == 29):
      startDate = date(lastYear, thisMonth, thisDay -1)
    else:
      startDate = date(lastYear, thisMonth, thisDay)

    #This will be used to gather the JSON data and then write or append it to a file
    for dt in apiRangeDates(startDate, endDate):

        #This makes a variable that will be used to access the website in JSON format using our NASA public api key
        #Note: if you do not have an api key, then go to https://api.nasa.gov/#live_example and simply apply for one.
        webUrl = urllib.request.urlopen("https://api.nasa.gov/planetary/apod?api_key=vG9rkcvYOMDKqpaVsNFSAtxwDUx376rKiQbLNIqy&date="+str(dt))

        #check if the code was able to connect to website by checking the result code.
        #If it did, then read the data and write to file, else print the error code that it returned.
        if(webUrl.getcode() == 200):
            #read and load JSON data from website
            data = json.loads(webUrl.read().decode())

            # create a new Dictionary to put JSON data in
            new_data = {}
            new_data["MediaType"] = data["media_type"]
            new_data["Title"] = data["title"]
            new_data["Description"] = data["explanation"]

            #Check if key "copyright" exists b/c sometimes it doesn't
            if data.get('copyright'):
                new_data["Credit"] = data["copyright"]
            else:
                new_data["Credit"] = "https://apod.nasa.gov/"

            new_data["PublicationDate"] = str(datetime.datetime.now().isoformat())

            #This list is to collect resource data from image, gif, video, etc...
            resources = []
            resources.append(getResouceImage(data))
            resources.append(getResouceThumbnail(data, dt))
            resource_data = resources
            new_data["Resources"] = resource_data

            asset_list.append(new_data)

    return asset_list

#############################################################################################################
# Method: getResouceImage                                                                                   #
# Parameters: NA                                                                                            #
# Returns: a dictionary                                                                                     #
# Purpose: The purpose of this method is to return a dictionary object that contains information about      #
#          a Image                                                                                          #
#############################################################################################################
def getResouceImage(data):
    assets = {}
    assets["ResourseType"] = "Original"
    assets["MediaType"] = "Image"
    assets["URL"] = data["url"]
    assets["ProjectionType"] = "Tan"
    return assets

#############################################################################################################
# Method: getResouceThumbnail                                                                               #
# Parameters: NA                                                                                            #
# Returns: a dictionary                                                                                     #
# Purpose: The purpose of this method is to return a dictionary object that contains information about      #
#          a thumbnail                                                                                      #
#############################################################################################################
def getResouceThumbnail(data, dt):
    assets = {}
    assets["ResourseType"] = "Thumbnail"
    assets["MediaType"] = "Image"
    assets["URL"] = "https://apod.nasa.gov/apod/calendar/S_" +str(dt.strftime("%y%m%d")) +".jpg"
    assets["ProjectionType"] = "Tan"
    return assets

#############################################################################################################
# Method: main()                                                                                            #
# Parameters: NONE                                                                                          #
# Returns: a JSON file containing one years worth of JSON data                                              #
# Purpose: The main method will run the main code and gather one years worth of JSON data from the website  #
#          Astronomy picture of the day.  It will then write all the JSON data into a file.                 #
#############################################################################################################

def main():

    main_JSON = {}

    main_JSON["Count"] = 1

    collections = []
    collections.append(addMainJSON())

    main_JSON["Collections"] = collections

    with open("jsonData.json", "w+") as outfile:
       json.dump(main_JSON, outfile)

    print(main_JSON)

#Run the main program
if __name__ == "__main__":
    main()

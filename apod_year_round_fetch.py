#############################################################################################################
# Author: Christian Soto                                                                                    #
# Program Name: apod_year_round_fetch.py                                                                    #
# Email: cjsoto@lsst.org or christian.j.sotoparra@gmail.com                                                 #
# Purpose: The purpose of this program is fetch the JSON data from year round from the website              #
#          https://apod.nasa.gov/apod/astropix.html? starting from today's date.  This program is ran using #
#          python 3 and later versions.  If you need any earlier versions of python, be sure to import the  #
#          correct libraries and modules.  Some of the methods from earlier modules might have to be changed#
#          or renamed as well.  After the JSON data is collected, it will write it all to a file called     #
#          jsonData.json.  If you find any bugs or need help, feel free to email me.                        #
#############################################################################################################

# modules needed to process internet, json data, and dates
from datetime import date
from datetime import timedelta
from PIL import Image
import io
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
# Method: getCollections                                                                                    #
# Parameters: NA                                                                                            #
# Returns: a dict of collections and count                                                                  #
# Purpose: The purpose of this method is to collect APOD resources and return as JSON data                  #
#############################################################################################################

def getCollections(api_key):

    #counter for tallying collections
    counter = 0

    #list to store all the JSON data of Collections.  
    collections = []

    # This will the variables that will be needed.  For now, only the last 3 days will be gathered for simple
    # and debugging purposes
    lastYear = date.today().year - 1
    thisMonth = date.today().month
    thisDay = date.today().day
    endDate = date.today()

    # Check for Leap years
    if(isLeapYear(endDate.year) and endDate.month == 2 and endDate.day == 29):
      startDate = date(lastYear, thisMonth, thisDay -1)
    else:
      startDate = date(lastYear, thisMonth, thisDay)

    #This will be used to gather the JSON data and then write or append it to a file
    for dt in apiRangeDates(startDate, endDate):
        counter += 1
        print(dt)
        webUrl = urllib.request.urlopen("https://api.nasa.gov/planetary/apod?api_key="+api_key+"&hd=true&date="+str(dt))

        #check if the code was able to connect to website by checking the result code.
        #If it did, then read the data and write to file, else print the error code that it returned.
        if(webUrl.getcode() == 200):
            #read and load JSON data from website
            data = json.loads(webUrl.read().decode())

            #new dictionary for collection
            collection = {}
            collection["Creator"] = "Astronomy Picture of the Day"
            collection["URL"] = "https://apod.nasa.gov/"
            collection["ID"] = "ap" + str(dt.strftime("%y%m%d"))
            collection["ReferenceURL"] = "https://apod.nasa.gov/apod/" + collection["ID"] + ".html"
            collection["Title"] = data["title"]
            collection["Description"] = data["explanation"]
            collection["PublicationDate"] = str(dt.isoformat())

            #Check if key "copyright" exists b/c sometimes it doesn't
            if data.get("copyright"):
                collection["Credit"] = data["copyright"]
            else:
                collection["Credit"] = ""

            #new dictionary for contact information
            contact_JSON = {}
            contact_JSON ["Name"] = "Robert Nemiroff"
            contact_JSON["Email"] = "nemiroff@mtu.edu"
            contact_JSON["Telephone"] = "1-906-487-2198"
            contact_JSON["Address"] = "1400 Townsend Drive"
            contact_JSON["City"] = "Houghton"
            contact_JSON["StateProvince"] = "Michigan"
            contact_JSON["PostalCode"] = "49931"
            contact_JSON["Country"] = "USA"
            collection["Contact"] = contact_JSON

            #list to store all the JSON data of Assets
            assets = []

            # create a new Dictionary to put asset JSON data in
            asset = {}
            asset["MediaType"] = str(data["media_type"]).title()

            #This list is to collect resource data from image, gif, video, etc...
            resources = []

            if data.get("hdurl"):
                resources.append(getResouceImage(data, dt, "Original"))

            resources.append(getResouceImage(data, dt, "Small"))
            resources.append(getResouceImage(data, dt, "Thumbnail"))
            resource_data = resources
            asset["Resources"] = resource_data

            assets.append(asset)

            collection["Assets"] = assets

            collections.append(collection)

    return {"collections":collections,"count":counter}

#############################################################################################################
# Method: getResouceImage                                                                                   #
# Parameters: NA                                                                                            #
# Returns: a dictionary                                                                                     #
# Purpose: The purpose of this method is to return a dictionary object that contains information about      #
#          a Image                                                                                          #
#############################################################################################################
def getResouceImage(data, dt, type):
    resource = {}
    resource["MediaType"] = str(data["media_type"]).title()
    resource["ResourceType"] = type

    if(type == "Original"):
        URL = data["hdurl"]
    elif(type == "Small"):
        URL = data["url"]
    elif(type == "Thumbnail"):
        URL = "https://apod.nasa.gov/apod/calendar/S_" +str(dt.strftime("%y%m%d")) +".jpg"
    else:
        URL = ""

    #Read data from url
    if(data["media_type"] != "video"):
        try:
            #Get filesize and dimensions
            with urllib.request.urlopen(URL) as url:
                if (url.info()["Content-Type"] == "image/jpeg" or url.info()["Content-Type"] == "image/gif"):
                    f = io.BytesIO(url.read())
                    img = Image.open(f)
                    resource["Filesize"] = int(url.info()["Content-Length"])
                    resource["Dimensions"] = img.size
        except urllib.error.URLError as e:
            print(URL + " " +e.reason)

    resource["URL"] = URL
    resource["ProjectionType"] = "Tan"
    return resource

#############################################################################################################
# Method: main()                                                                                            #
# Parameters: NONE                                                                                          #
# Returns: a JSON file containing one years worth of JSON data                                              #
# Purpose: The main method will run the main code and gather one years worth of JSON data from the website  #
#          Astronomy picture of the day.  It will then write all the JSON data into a file.                 #
#############################################################################################################

def main():

    #This dictionary will collect all the JSON data and stored here
    main_JSON = {}

    #Go to https://api.nasa.gov/#live_example to apply for a NASA API key and enter it here:
    api_key = "CHANGE_ME"

    #Get APOD data for last 365 days
    apod_data = getCollections(api_key)

    #This list will collect contact information and assets
    main_JSON["Collections"] = apod_data["collections"]

    #Number sources where JSON was collected
    main_JSON["Count"] = apod_data["count"]

    #This creates a new file where JSON data will be stored
    with open("apod_v2.json", "w+") as outfile:
       json.dump(main_JSON, outfile)

#Run the main program
if __name__ == "__main__":
    main()


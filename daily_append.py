#############################################################################################################
# Author: Christian Soto                                                                                    #
# Program Name: daily_append.py                                                                             #
# Email: cjsoto@lsst.org or christian.j.sotoparra@gmail.com                                                 #
# Purpose: The purpose of this program is to first collect the newist feed of the apod website, erase the   #
#          oldest feed from the file jsonData.json, and then adds the newist the feed to the JSON           #
#          collections list, which will then write to the file.  There are no known bugs as of now.         #
#############################################################################################################

# modules needed to process internet, json data, and dates
from datetime import date
from PIL import Image
import io
import datetime
import urllib.request
import json

#############################################################################################################
# Method: addNew                                                                                            #
# Parameters: data                                                                                          #
# Returns: a list with one more element                                                                     #
# Purpose: The purpose of this method is to add a new element to the end of the list                        #
#############################################################################################################

def addNew(api_key):

    dt = date.today()

    #get the newest element
    webUrl = urllib.request.urlopen("https://api.nasa.gov/planetary/apod?api_key="+api_key+"&hd=true&date="+str(date.today()))

    #new dictionary for collection
    collection = {}

    #check if the code was able to connect to website by checking the result code.
    #If it did, then read the data and write to file, else print the error code that it returned.
    if(webUrl.getcode() == 200):
        #read and load JSON data from website
        data = json.loads(webUrl.read().decode())

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

    return collection

#############################################################################################################
# Method: deleteOldJSON                                                                                     #
# Parameters: data                                                                                          #
# Returns: a list with one less element                                                                     #
# Purpose: The purpose of this method is to delete the oldest JSON in the list                              #
#############################################################################################################

def deleteOldJSON(data):

    #Delete the oldest element in the list
    del data["Collections"][0]
    return data

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
#          Astronomy picture of the day.  It will then append the newist feed from today's date and delete  #
#          the oldest feed from the list.                                                                   #
#############################################################################################################
def main():

    #Go to https://api.nasa.gov/#live_example to apply for a NASA API key and enter it here:
    api_key = "CHANGE_ME"

    # get the newest element
    webUrl = urllib.request.urlopen("https://api.nasa.gov/planetary/apod?api_key="+api_key+"&hd=true&date=" + str(date.today()))
    new_data = json.loads(webUrl.read().decode())

    #read
    f = open('apod_v2.json', 'r+')

    #load JSON list into data
    data = json.load(f)

    length = len(data["Collections"]) - 1

    # If the title of the new_data and data are the same then just return
    if(new_data["title"] == data["Collections"][length]["Title"]):
        return
    else:
        #delete oldest JSON in the list
        data = deleteOldJSON(data)

        #add newest JSON element into the list
        data["Collections"].append(addNew(api_key))

        #erase everything from the file and write the new data
        f.seek(0)
        json.dump(data, f)
        f.truncate()

#Run the main program
if __name__ == "__main__":
    main()

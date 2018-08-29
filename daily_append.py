#############################################################################################################
# Author: Christian Soto                                                                                    #
# Program Name: daily_append.py                                                                             #
# Email: cjsoto@lsst.org or christian.j.sotoparra@gmail.com                                                 #
# Purpose: The purpose of this program is to first collect the newist feed of the apod website, erase the   #
#          oldest feed from the file jsonData.json, and then adds the newist the feed to the JSON           #
#          collections list, which will then write to the file.  There are no known bugs as of now.         #                                                        #
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

def addNew():

    #get the newest element
    webUrl = urllib.request.urlopen("https://api.nasa.gov/planetary/apod?api_key=vG9rkcvYOMDKqpaVsNFSAtxwDUx376rKiQbLNIqy&date="+str(date.today()))

    data = json.loads(webUrl.read().decode())

    # create a new Dictionary to put JSON data in
    new_data = {}
    new_data["MediaType"] = data["media_type"]
    new_data["Title"] = data["title"]
    new_data["Description"] = data["explanation"]

    # Check if key "copyright" exists b/c sometimes it doesn't
    if data.get('copyright'):
        new_data["Credit"] = data["copyright"]
    else:
        new_data["Credit"] = "https://apod.nasa.gov/"

    new_data["PublicationDate"] = str(datetime.datetime.now().isoformat())

    # This list is to collect resource data from image, gif, video, etc...
    resources = []
    resources.append(getResouceImage(data))
    resources.append(getResouceThumbnail(data, date.today()))
    resource_data = resources
    new_data["Resources"] = resource_data

    return new_data

#############################################################################################################
# Method: deleteOldJSON                                                                                     #
# Parameters: data                                                                                          #
# Returns: a list with one less element                                                                     #
# Purpose: The purpose of this method is to delete the oldest JSON in the list                              #
#############################################################################################################

def deleteOldJSON(data):

    #Delete the oldest element in the list
    del data["Collections"][0]["Assets"][0]
    return data

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
    assets["MediaType"] = data["media_type"]

    #Read data from url
    URL = data["url"]

    if(data["media_type"] != "video"):
        try:
            #Get filesize and dimensions
            with urllib.request.urlopen(URL) as url:
                if (url.info()["Content-Type"] == "image/jpeg" or url.info()["Content-Type"] == "image/gif"):
                    f = io.BytesIO(url.read())
                    img = Image.open(f)
                    assets["Filesize"] = url.info()["Content-Length"]
                    assets["Dimensions"] = img.size
        except urllib.error.URLError as e:
            print(URL + " " +e.reason)

    assets["URL"] = URL
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

    #Read data from url
    URL = "https://apod.nasa.gov/apod/calendar/S_" +str(dt.strftime("%y%m%d")) +".jpg"

    try:
        #Get filesize and dimensions
        with urllib.request.urlopen(URL) as url:
            if (url.info()["Content-Type"] == "image/jpeg" or url.info()["Content-Type"] == "image/gif"):
                f = io.BytesIO(url.read())
                img = Image.open(f)
                assets["Filesize"] = url.info()["Content-Length"]
                assets["Dimensions"] = img.size
    except urllib.error.URLError as e:
        print(URL + " " +e.reason)

    assets["URL"] = URL
    assets["ProjectionType"] = "Tan"
    return assets

#############################################################################################################
# Method: main()                                                                                            #
# Parameters: NONE                                                                                          #
# Returns: a JSON file containing one years worth of JSON data                                              #
# Purpose: The main method will run the main code and gather one years worth of JSON data from the website  #
#          Astronomy picture of the day.  It will then append the newist feed from today's date and delete  #
#          the oldest feed from the list.                                                                   #
#############################################################################################################
def main():

        # get the newest element
        webUrl = urllib.request.urlopen("https://api.nasa.gov/planetary/apod?api_key=vG9rkcvYOMDKqpaVsNFSAtxwDUx376rKiQbLNIqy&date=" + str(date.today()))
        new_data = json.loads(webUrl.read().decode())

        #read
        f = open('jsonData.json', 'r+')

        #load JSON list into data
        data = json.load(f)

        length = len(data["Collections"][0]["Assets"]) - 1

        # If the title of the new_data and data are the same then just return
        if(new_data["title"] == data["Collections"][0]["Assets"][length]["Title"]):
            return
        else:
            #delete oldest JSON in the list
            data = deleteOldJSON(data)

            #add newest JSON element into the list
            data["Collections"][0]["Assets"].append(addNew())

            #earse everything from the file and write the newist data
            f.seek(0)
            json.dump(data, f)
            f.truncate()

#Run the main program
if __name__ == "__main__":
    main()

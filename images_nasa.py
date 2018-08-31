from datetime import date
from PIL import Image
import io
import datetime
import urllib.request
import json

def getCorrectMonth(metaData, thisDate, idNumber):
    print(metaData["AVAIL:DateCreated"])
    print(metaData["AVAIL:NASAID"])
    print(str(thisDate))
    #print(idNumber)

    if(metaData["AVAIL:DateCreated"] < str(thisDate)):
         idNumber = idNumber + 2
         metaURL = urllib.request.urlopen("https://images-assets.nasa.gov/image/PIA00" + str(idNumber)+ "/metadata.json")
         metaData = json.loads(metaURL.read().decode())
         getCorrectMonth(metaData, thisDate, idNumber)

    print(metaData["AVAIL:NASAID"])
def main():

        endDate = datetime.datetime.now()

        # get the newest element
        webUrl = urllib.request.urlopen("https://images-api.nasa.gov/search?year_start=2018&center=JPL&media_type=image")
        new_data = json.loads(webUrl.read().decode())

        metaURL = urllib.request.urlopen("https://images-assets.nasa.gov/image/" + new_data["collection"]["items"][0]["data"][0]["nasa_id"] + "/metadata.json")
        metaData = json.loads(metaURL.read().decode())
        getCorrectMonth(metaData, endDate.strftime("%d %B %Y"), int(new_data["collection"]["items"][0]["data"][0]["nasa_id"][3:]))
        #print(metaData["AVAIL:DateCreated"])
        #print(datetime.datetime.now().strftime("%B"))
        #print(new_data["collection"]["metadata"]["total_hits"])
        #print(new_data["collection"]["items"][0]["data"][0]["title"])
        #print(new_data["collection"]["items"][0]["data"][0]["media_type"])
        #print(new_data["collection"]["items"][0]["data"][0]["title"])
        #print(new_data["collection"]["items"][0]["data"][0]["description"])
        #print(new_data["collection"]["items"][0]["data"][0]["photographer"])
        #print(new_data["collection"]["items"][0]["links"][0]["href"])
        #print(new_data["collection"]["items"][0]["data"][0]["nasa_id"][3:])

#Run the main program
if __name__ == "__main__":
    main()


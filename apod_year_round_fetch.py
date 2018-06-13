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
# Method: main()                                                                                            #
# Parameters: NONE                                                                                          #
# Returns: a JSON file containing one years worth of JSON data                                              #
# Purpose: The main method will run the main code and gather one years worth of JSON data from the website  #
#          Astronomy picture of the day.  It will then write all the JSON data into a file.                 #
#############################################################################################################
def main():

    #This will the variables that will be needed.  For now, only the last 3 days will be gathered for simple
    #and debugging purposes
    lastYear = date.today().year - 1
    thisMonth = date.today().month
    thisDay = date.today().day

    startDate = date(lastYear, thisMonth, thisDay)
    endDate = date.today()

    #This will be used to gather the JSON data and then write or append it to a file
    for dt in apiRangeDates(startDate, endDate):


        # This makes a variable that will be used to access the website in JSON format using our NASA public api key
        # Note: if you do not have an api key, then go to https://api.nasa.gov/#live_example and simply apply for one.
        webUrl = urllib.request.urlopen("https://api.nasa.gov/planetary/apod?api_key=vG9rkcvYOMDKqpaVsNFSAtxwDUx376rKiQbLNIqy&date="+str(dt))

        # make a variable to check the character encoding
        charset = webUrl.info().get_param('charset', 'utf8')

        # check if the code was able to connect to website by checking the result code.
        # If it did, then read the data and write to file, else print the error code that it returned.
        if(webUrl.getcode() == 200):

            #read
            data = webUrl.read()

            #decode the character encoding and make an JSON object called my_JSON_object
            my_JSON_object = json.loads(data.decode(charset))

            #create a file and write to it
            with open("jsonData.txt", "a+") as outfile:
                json.dump(my_JSON_object, outfile)
        else:
            print("Recieved error code: " + str(webUrl.getcode()))

#Run code to get the JSON data
main()

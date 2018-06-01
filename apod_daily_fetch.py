#################################################################################
# Author: Christian Soto                                                        #
# Program Name: apod_daily_fetch.py                                             #
# Email: cjsoto@lsst.org or christian.j.sotoparra@gmail.com                     #
# Purpose: The purpose of this program is fetch the daily JSON                  #
#          data from the website https://apod.nasa.gov/apod/astropix.html?.     #
#          This program can be ran using python 3 and later versions.  If you   #
#          need any earlier versions of python, be sure to import the correct   #
#          libraries and modules.  Some of the methods from earlier modules     #
#          might have to be changed or renamed as well.  There are currently    #
#          no known bugs.  After the JSON data is collected, it writes it to a  #
#          file called jsonData.txt.  If you find any bugs or need help, feel   #
#          free to email me.                                                    #
#################################################################################

# modules needed to process internet and json data
import urllib.request
import json

def main():

    #This makes a variable that will be used to access the website in JSON format using our NASA public api key
    #Note: if you do not have an api key, then go to https://api.nasa.gov/#live_example and simply apply for one.
    webUrl = urllib.request.urlopen("https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY")

    #make a variable to check the character encoding
    charset = webUrl.info().get_param('charset', 'utf8')

    # check if the code was able to connect to website by checking the result code.
    # If it did, then read the data and write to file, else print the error code that it returned.
    if(webUrl.getcode() == 200):

        #read the data, the data from the website is encoded in bytes
        data = webUrl.read()

        #decode the character encoding and make an JSON object called my_JSON_object
        my_JSON_object = json.loads(data.decode(charset))

        #create a file and write to it
        with open("jsonData.txt", "w+") as outfile:
            json.dump(my_JSON_object, outfile)

    else:

        #print error code
        print("Recieved error code: " + str(webUrl.getcode()))

main()

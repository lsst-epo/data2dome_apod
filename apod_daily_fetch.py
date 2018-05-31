
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
    # If it did, then read the data and print it, else print the error code that it returned.
    if(webUrl.getcode() == 200):

        #read the data, the data from the website is encoded in bytes
        data = webUrl.read()

        #decode the character encoding and make an JSON object called decoded
        decoded = json.loads(data.decode(charset))

        #here we can print fields of the JSON for example here, we are printing the field explanation, title,
        #and date.
        print(decoded["explanation"])
        print(decoded["date"])
        print(decoded["title"])

    else:

        #print error code
        print("Recieved error code: " + str(webUrl.getcode()))

main()

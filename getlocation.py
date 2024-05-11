#retrieves the latitude and logitude for any location
import sys, re, requests
from pickComputer import directory
sys.path.insert(0, f'{directory}/')
import Private.OWMap.private as i
#----------------------------------------------------------------
OWM_KEY = i.OWMkey

def getlatlong():
    city = input("Enter a city name: ").replace(" ","_")

    while True:
        try: #using try block since user input may not be valid
            cityurl = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&appid={OWM_KEY}"
            req = requests.get(cityurl, timeout = 20)
            if req.status_code==200:
                pass
            if req.text == "[]":
                raise Exception

            cityinfo = re.compile(r'"country":.+[^\}\]]')
            match = cityinfo.search(req.text)


            verify_ct = input(f"Is {city} located in {match.group()} correct? Enter yes or no: ").lower()
            valid_responses = ["yes","y","no","n"]
            while verify_ct not in valid_responses:
                verify_ct = input("Please enter yes or no:").lower()
            if verify_ct == "no" or verify_ct == "n":
                city = input("Enter a different city name:").replace(" ","_")
                continue
            if verify_ct == "yes" or verify_ct == "y":
                break

        except Exception:
            print(f"An error occurred when accessing the city's url. Recheck spelling.\
                    \nReturn Code:{req.status_code}\
                    \nReturn text: {req.text}\n")
            city = input("Enter a different city name:").replace(" ","_")
            continue


    lat_pattern = re.compile(r'("lat":)([-\d.]+)')
    lon_pattern = re.compile(r'("lon":)([-\d.]+)')

    lat = lat_pattern.search(req.text).group(2)
    long =  lon_pattern.search(req.text).group(2)

    return tuple([long,lat,city,cityinfo])
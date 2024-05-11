import sys,requests
from pushbullet import PushBullet
from datetime import datetime
from pickcomputer import directory
from createMessage import createmessage
from getLocation import getlatlong
from backupResults import BackupResults
sys.path.insert(0, f'{directory}')
import Private.OWM_Weather_Notification.private as i


curr_time = datetime.now().strftime("%m-%d-%Y %I.%M%p")
apiterms = { #converts inputted terms to accessible terms in the API results.
    "temp" : "temp",
    "feels like" : "feels_like",
    "humidity": "humidity",
    "precip" : "pop",
    "clouds" : "clouds",
    "visibility" : "visibility",
    "wind speed" : "wind_speed",
    "wind dir" : "wind_deg",
    "wind gust" : "wind_gust",
    "uv index" : "uvi"
}

def chooselocation(): #Allowspeed the user to choose any location they want information about
    return getlatlong()
def defaultCity():
    return i.set_location

curr_city = chooselocation() #Change curr city selected
long,lat,city = curr_city[0], curr_city[1], curr_city[2]

#----------------
def main():
    global doc,today_remaining_hrs,curr_hr
    PB_KEY = i.PB_KEY
    OWM_KEY = i.OWMkey
    doc = OWMap_getrequest(OWM_KEY,PB_KEY)
    curr_hr = datetime.fromtimestamp(doc['current']['dt']).strftime("%H")
    today_remaining_hrs = 24 - int(curr_hr) #length/last index for remaining today's hrs
    tmrw_11pm = today_remaining_hrs+23
    PushBullet(PB_KEY).push_note(f"{city}", runAPI(PB_KEY, doc))
    BackupResults(desired_values,convertHour,doc,city,curr_time,curr_hr,today_remaining_hrs)
    

def runAPI(PB_KEY, doc):
    global desired_values
    '''mn = morning | md = mid-day'''
    hr = index = temp = feels_like = uvindex  = md_uv  = mn_wspeed = md_wspeed = max_wspeed = wgust = precip = md_wgust = None #initialize to NULL
    desired_values = { #var_key:[value,hr,index,apiterm,min,maxMod]
        'temp':[temp,hr,index,'temp',0,3],
        'feels_like':[feels_like,hr,index,'feels_like',0,3],
        'uvindex':[uvindex,hr,index,'uvi',0,-1],
        'md_uv':[md_uv,hr,index,'uvi',today_remaining_hrs-12,8],
        'mn_wspeed':[mn_wspeed,hr,index,'wind_speed',0,11],
        'md_wspeed':[md_wspeed,hr,index,'wind_speed',0,6],
        'max_wspeed':[max_wspeed,hr,index,'wind_speed',0,-1],
        'wgust':[wgust,hr,index,'wind_gust',0,6],
        'md_wgust':[md_wgust,hr,index,'wind_gust',today_remaining_hrs-12,6],
        'precip':[precip,hr,index,'pop',0,6]
        }

    try:
        curr_temp = doc['current']['temp'] #others are hourly, this is 'current'
        for key in desired_values:
            d = desired_values[key]
            d[0],d[1],d[2] = getinfo(d[3],d[4],d[5])
        return createmessage(today_remaining_hrs,curr_temp, desired_values, convertHour)
    
    except Exception as e:
        PushBullet(PB_KEY).push_note(datetime.now().strftime("%m-%d-%Y"), e)
        print(e)
        exit()

def getinfo(apiterm,min,max_mod):
    value = -float('inf')
    index = 0
    add_to_index = 0 #functions like a pointer, updates index to index of curr max
    for i in range(min,today_remaining_hrs - max_mod): #find max value within range
        curr_val = doc['hourly'][i][apiterm]
        if curr_val > value:
            value = curr_val
            index += add_to_index
            add_to_index = 1
            continue
        add_to_index += 1

    if min != 0: #modify index and hour if mix != 0 since previous for loop would be innaccurate
        index = 0
        for j in range(0,today_remaining_hrs - max_mod):
            findval = doc['hourly'][j][apiterm]
            if findval == value:
                break
            index += 1
    hr = datetime.fromtimestamp(doc['hourly'][index]['dt'])
    return value,hr,index

def OWMap_getrequest(OWM_KEY, PB_KEY): #accesses OpenWeatherMap API with specified location and parameters
    url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={long}&exclude=daily,minutely,alerts&units=imperial&appid={OWM_KEY}"
    req = requests.get(url)
    if req.status_code == 200:
        doc = req.json()
        return doc
    else:
        # print(f"An error occurred when sending a get request to OpenWeatherMap's api. Error code: {req.status_code}")
        PushBullet(PB_KEY).push_note('Today', "An error occurred when sending a get request to OpenWeatherMap's api. Error code: {req.status_code}")
        exit()

def convertHour(time):
    '''converts 24-hr format  to 12-hr am/pm. Not using datetime module because I don't like the format.'''
    if int(time.strftime('%H')) > 12: #afternoon
        return f"{int(time.strftime('%H')) - 12}pm"
    else:
        return f"{int(time.strftime('%H'))}am"

main()

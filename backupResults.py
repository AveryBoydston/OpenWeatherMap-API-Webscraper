import sys
from pickcomputer import directory
sys.path.insert(0, f'{directory}')

def BackupResults(d,convertHour,doc,city,curr_time,curr_hr,today_remaining_hrs):
    save_folder = f"{directory}/Weather_API_webscraper/save files/openweathermap req savefiles"
    with open(f'{save_folder}/{city} {curr_time}.txt',"a") as file:

        #Additional data
        file.write("\nAdditional Info:\n" + "-"*40 + "\n")
        file.write(f"Today's High (F): {d['temp'][0]} at {convertHour(d['temp'][1])}\n")
        file.write(f"Feels Like: {d['feels_like'][0]} at {convertHour(d['feels_like'][1])}\n")
        file.write(f"Today's Max UVindex: {d['uvindex'][0]} at {convertHour(d['uvindex'][1])}\n")
        
        #Wind Speed
        if today_remaining_hrs-12 > 0: #if 11am data exists
            file.write(f"Max morning windspeed (7-11am): {d['mn_wspeed'][0]} at {convertHour(d['mn_wspeed'][1])}\n")
        else:
            file.write("It is already past 11am. No morning windspeed data.\n")

        if today_remaining_hrs-6 > 0: #if 5pm data exists
            file.write(f"Mid-day windspeed (11am-5pm): {d['md_wspeed'][0]} at {convertHour(d['md_wspeed'][1])}\n")
        else:
            file.write(f"current hour past 5pm: {curr_hr}. No mid-day windspeed data.\n")
        file.write(f"Today's Max Wind Speed: {d['max_wspeed'][0]} at {convertHour(d['max_wspeed'][1])}\n")

        #Wind gust
        if today_remaining_hrs-12 > 0:
            file.write(f"Mid-day, Expect wind gusts of up to {d['md_wgust'][0]} at {convertHour(d['md_wgust'][1])}\n")
        else:
            file.write(f"Expect wind gusts of up to {d['wgust'][0]} at {convertHour(d['wgust'][1])}\n")
        file.write(f"Max wind gust: {d['wgust'][0]} at {convertHour(d['wgust'][1])}\n")

        #Chance of Rain
        if d['precip'][0] > 0.75: #75% chance
            file.write(f"High chance of rain today: {d['precip'][0]} at {convertHour(d['precip'][1])}\n")
        else:
            file.write(f"Don't expect rain today: {d['precip'][0]}")

        #API Results
        file.write('\n'*3)
        file.write("API Results:\n")
        file.write('-'*80 + '\n')
        file.write(str(doc))

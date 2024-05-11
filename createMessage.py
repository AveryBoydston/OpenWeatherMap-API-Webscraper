'''creates custom message in personal favorite formatting'''
from datetime import datetime

def createmessage(today_remaining_hrs,curr_temp,d, convertHour):
    message = f"🌅 Curr. temp: {int(curr_temp)}°F, {convertHour(datetime.now())}\n"
    
    if today_remaining_hrs-12 > 0:
        message += f"☀️ UV index: {d['md_uv'][0]} @ {convertHour(d['md_uv'][1])}\n"
    message += (f"🌡️ High: {d['temp'][0]:.1f}°F,  Feels: {d['feels_like'][0]:.2f}°F\n")

    if d['md_uv'][0] != d['uvindex'][0]:
        message += f"☀️ Max UV: {d['uvindex'][0]} @ {convertHour(d['uvindex'][1])}\n"

    if today_remaining_hrs-6 > 0:
        message += f"🪁Windspeed: {d['md_wspeed'][0]}mph @ {convertHour(d['md_wspeed'][1])}\n"
        if today_remaining_hrs-12 > 0: #11am to 5pm
            message += f"💨 Gusts of: {d['md_wgust'][0]}mph @ {convertHour(d['md_wgust'][1])}\n"
        else: #executes after 5pm
            message += f"💨 gusts of: {d['wgust'][0]}mph @ {convertHour(d['wgust'][1])}\n"
        if d['md_wspeed'][0] >= 11:
            message+= "❌ Windspeed is too high.\n"

    dp = d['precip']
    if dp[0] < 0.55:
        message += f"Don't expect rain today. {(dp[0])*100}% chance\n"
    elif dp[0] >= 0.85:
        message += f"🌧️ Rain today at {convertHour(dp[1])}. {dp[0]*100}% chance\n"
    else: # 0.55 <= precip < 0.85
        message += f"🌧️ {(dp[0])*100:.0f}% chance of rain at {convertHour(dp[1])}. \n"

    message += "🧴 Wear Sunscreen!"
    if d['temp'][0] < 66:
        message += "🧥 Dress warm! Good day for a Hoodie."

    return message
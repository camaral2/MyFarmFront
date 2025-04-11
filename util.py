import time
import requests


def translate_phase_moon(textEnghish: str): 
    if textEnghish.lower()=="waning crescent": return "Lua Minguante"
    if textEnghish.lower()=="waxing gibbous": return "Lua Crescente"
    
    return textEnghish

def get_moon_phase():
    timestamp = int(time.time())  # current UNIX time
    url = f"https://api.farmsense.net/v1/moonphases/?d={timestamp}"

    response = requests.get(url)
    data = response.json()

    return  data[0]["Phase"]

def month_desc():
    return [
       'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]
    
def list_modes():
    return [
        {"id": 1, "desc": "Pre-plant"},
        {"id": 2, "desc": "Plant"},
        {"id": 3, "desc": "Management"},
        {"id": 4, "desc": "Crop"}
    ]
    
def get_mode_desc(mode_id):
    for mode in list_modes():
        if mode["id"] == mode_id:
            return mode["desc"]
    return "Unknown"
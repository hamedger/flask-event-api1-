from flask import Flask, request, jsonify
from flask_cors import CORS
import requests, pandas as pd
from datetime import datetime, timedelta
from predicthq import Client

from flask import Flask, request, jsonify
from flask_cors import CORS

# 🔑 Config
TM_API_KEY = "G7LOr5tPvPF1Klcy7RkTCRslOYfy9Vhy"
PHQ_TOKEN  = "p_GFJUV1m5g9DO8ItaOaOX8RQZX66t-o6F1F9DZG"

app = Flask(__name__)
CORS(app)  # Allow React Native app to call this API

# Top 10 US cities (static list)
TOP_US_CITIES = [
    "New York",
    "Detroit",
    "Los Angeles",
    "Chicago",
    "Houston",
    "Phoenix",
    "Philadelphia",
    "San Antonio",
    "San Diego",
    "Dallas",
    "San Jose"
]
# Get today's date at midnight UTC
START = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)

# Add 7 days
END = START + timedelta(days=7)

# Format as ISO string with Zulu timezone suffix
START_str = START.strftime("%Y-%m-%dT%H:%M:%SZ")
END_str = END.strftime("%Y-%m-%dT%H:%M:%SZ")


# PredictHQ Ranking
def classify_rank(rank):
    try:
        rank = int(rank)
    except (ValueError, TypeError):
        return "Unknown"

    if 81 <= rank <= 100:
        return "Major"
    elif 61 <= rank <= 80:
        return "Significant"
    elif 41 <= rank <= 60:
        return "Important"
    elif 21 <= rank <= 40:
        return "Moderate"
    elif 0 <= rank <= 20:
        return "Minor"
    else:
        return "Unknown"
        
 country = request.args.get('country', 'US')  # Defaults to US
 city = request.args.get('city', 'New York')  # Default to New York if city not provided
  
# Ticketmaster
def tm_events(city):
    url = "https://app.ticketmaster.com/discovery/v2/events.json"
    params = dict(apikey=TM_API_KEY, city=city, countryCode=country,
                  startDateTime=START, endDateTime=END, size=100, sort="date,asc")
    resp = requests.get(url, params=params)
    if resp.status_code != 200: return []
    events = []
    for e in resp.json().get("_embedded", {}).get("events", []):
        v = e["_embedded"]["venues"][0]
        addr = f"{v.get('address',{}).get('line1','')}, {v['city']['name']}"
        maps = f"https://www.google.com/maps/search/{addr.replace(' ','+')}"
        events.append({
            "Source": "Ticketmaster",
            "Name": e["name"],
            "Start": e["dates"]["start"].get("dateTime", ""),
            "Address": addr,
            "Get Directions": maps,
            "Estimated Attendees": "N/A",
            "Rank": "",
        })
    return events

# Predicthq 
def fetch_phq_events(city, start, end):
    url = "https://api.predicthq.com/v1/events/"
    headers = {"Authorization": f"Bearer {PHQ_TOKEN}"}
    params = {
        "active.gte": start,
        "active.lte": end,
        "country": "US",
        "limit": 100,
        "sort": "rank",
        "q": city
    }
    all_events = []
    while url:
        response = requests.get(url, headers=headers, params=params if "?" not in url else {})
        if response.status_code != 200:
            print("Error:", response.status_code, response.text)
            break

        data = response.json()
        for e in data.get("results", []):
            loc = e.get("location", {})
            if isinstance(loc, list):  # In case location is accidentally a list
                loc = loc[0] if loc else {}

            addr = loc.get("address", "") if isinstance(loc, dict) else ""
            coords = loc.get("geometry", {}).get("coordinates", []) if isinstance(loc, dict) else []

            maps_url = f"https://www.google.com/maps/search/{addr.replace(' ', '+')}" if addr else ""

            attendees = "N/A"
            for meta in e.get("metadata", []):
                if isinstance(meta, dict) and "attendance" in meta:
                    attendees = meta["attendance"]
                    break
            rank_label = classify_rank(e.get("rank", None))

            all_events.append({
                "Source": "PredictHQ",
                "Name": e.get("title", ""),
                "Start": e.get("start", ""),
                "Address": addr,
                "Coordinates": coords,
                "Get Directions": maps_url,
                "Ticket URL": e.get("link", ""),
                "Rank": rank_label,
                "Estimated Attendees": attendees
            })

        url = data.get("next")

    return all_events

# City Open Data (NYC example)
def civic_events():
    url = "https://data.cityofnewyork.us/resource/ve7u-dqnp.json"
    params = {"$where": f"event_date between '{START.strftime("%Y-%m-%d")}' and '{END.strftime("%Y-%m-%d")
                                                                                  }'"}
    resp = requests.get(url, params=params)
    if resp.status_code != 200: return []
    events = []
    for e in resp.json():
        addr = e.get("location_1",{}).get("human_address","")
        maps = f"https://www.google.com/maps/search/{addr.replace(' ','+')}"
        out.append({
            "Source": "NYC Civic",
            "Name": e.get("event_name",""),
            "Start": e.get("event_date",""),
            "Venue": e.get("borough",""), "Address": addr,
            "Get Directions": maps, "Ticket URL": "", "Rank": "", "Civic Info": e.get("event_type","")
        })
    return events

@app.route('/cities', methods=['GET'])
def get_cities():
    return jsonify(TOP_US_CITIES)


@app.route('/', methods=['GET'])
def get_events():
    
    country = request.args.get('country', 'US')  # Defaults to US
    city = request.args.get('city', 'New York')  # Default to New York if city not provided
    sort_by = request.args.get('sort')  # e.g., 'date', 'attendance', 'source'
    
    if not city:
        return jsonify({"error": "City parameter is required"}), 400

    print(f"City requested: {city}")

    events = tm_events(city) + fetch_phq_events(city)

    if sort_by == "date":
        events.sort(key=lambda x: x.get("Start", ""))
    elif sort_by == "attendance":
        events.sort(key=lambda x: int(x.get("Estimated Attendees", 0)) if x.get("Estimated Attendees", "N/A").isdigit() else 0, reverse=True)
    elif sort_by == "source":
        events.sort(key=lambda x: x.get("Source", ""))

    return jsonify(events)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)



# prining to csv file 
# COUNTRY = input("Enter country: ")
# print(COUNTRY)
#CITY = input("Enter city: ")
#print(CITY)


# code from python script to write data in csv file. dont need in the app}


#if __name__ == "__main__"
   
   # events = tm_events(city)
    #events += fetch_phq_events(city, START[:10], END[:10])
   # events += fetch_phq_events(city, START.strftime("%Y-%m-%d"), END.strftime("%Y-%m-%d"))
    #events += civic_events()

    #df = pd.DataFrame(events)
    #app.run(debug=True)
    #df.to_csv("city_combined_events.csv", index=False)
    #print(f"Saved {len(df)} events from {city}") 

#End  code from python script to write data in csv file. dont need in the app}

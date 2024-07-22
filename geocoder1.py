import geocoder
import json 
import random


with open('_build/players.json') as f:
    players = json.load(f)
    
    
players_geojson={}

players_geojson["type"] = "FeatureCollection"
players_geojson["features"] =[]

    
for player in players:
    last_ip=str(player['more'][0]['last_ip'])
    if last_ip!="":
        #print(last_ip)
        g = geocoder.ip(last_ip)
        
        lat = g.latlng[0] + (random.random()-0.5)/30
        lon = g.latlng[1] + (random.random()-0.5)/30
        
        feature = {}
        feature["geometry"] = {}
        feature["properties"]  = {}
        
        feature["geometry"]["type"] = "Point"

        feature["geometry"]["coordinates"] = [lon, lat ]

           
        feature["properties"]["city"] = g.city
        feature["properties"]["country"] = g.country
        feature["properties"]["region"] = g.state
        feature["properties"]["name"] = player["name"]
        
        if (g.country == "UA") and (g.state!="Crimea"):
            print(g.state," ", g.country, " ", lat, lon)
        else:    
            players_geojson["features"].append(feature)
   
    


with open('_build/players.geojson', 'w', encoding='utf-8') as f:
    json.dump(players_geojson, f, ensure_ascii=False, indent=4) 
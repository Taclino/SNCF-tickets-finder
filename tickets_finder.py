import requests
import json
import numpy as np
import datetime
from environment import * ##All the variable such as cards,headers...

           


def look_for_tickets() :

    prices = []
    
    data = {
        "local_currency": "EUR", 
        "search": 
            {"arrival_station_id": arrival_station_id,
            "departure_date": departure_date, 
            "departure_station_id": departure_station_id,
            "systems": ["sncf", "db", "idtgv", "ouigo", 
                "trenitalia", "ntv", "hkx", "renfe", "cff", 
                "benerail", "ocebo", "westbahn", "leoexpress",
                "locomore", "busbud", "flixbus", "distribusion",
                "cityairporttrain", "obb", "timetable"], 
            "passengers": [
                {"id": "6ed7911c-ed2c-4745-80fd-64e173bb9328",
                "age": passenger1_age,
                "birthdate": passenger1_birthdate,
                "cards": cards, # [] for none
                "label": "6ed7911c-ed2c-4745-80fd-64e173bb9328"
                }
            ]
        }
    }

    post_data = json.dumps(data)
    ret =requests.post(url="https://www.trainline.eu/api/v5_1/search", 
        data=post_data, headers=headers)
    #print(ret.json())
    nb_found_trip = 0
    nb_possible_trips = len(ret.json()["folders"])
    with open('json_data.txt', 'w') as outfile:
        for i in range(nb_possible_trips):
            
            if (ret.json()["folders"][i]["is_sellable"]
            and not(ret.json()["folders"][i]["arrival_different_from_requested"])
            and limit_departure_date > ret.json()["folders"][i]["departure_date"]):

                nb_found_trip +=1
                prices.append(ret.json()["folders"][i]["cents"])
                outfile.write(str(ret.json()["folders"][i]))
                outfile.write("\n")

        data["search"]["arrival_station_id"] = second_arrival_station_id
        post_data = json.dumps(data)
        ret =requests.post(url="https://www.trainline.eu/api/v5_1/search",
        data=post_data, headers=headers)

        ### Nouvelle recherche pour les ouigo (Massy TGV)

        nb_possible_trips += len(ret.json()["folders"])
        for i in range(len(ret.json()["folders"])):
            
            if (ret.json()["folders"][i]["is_sellable"]
            and not(ret.json()["folders"][i]["arrival_different_from_requested"])
            and limit_departure_date > ret.json()["folders"][i]["departure_date"]):

                nb_found_trip +=1
                prices.append(ret.json()["folders"][i]["cents"])
                outfile.write(str(ret.json()["folders"][i]))
                outfile.write("\n")
    
    e = datetime.datetime.now()

    if nb_found_trip >0:
        best_price = np.min(prices)/100
        print("Found ", nb_found_trip, " trips starting at ", best_price, "€ ! "+
        '%s/%s/%s %s:%s' % (e.day, e.month, e.year, e.hour, e.minute))
        return nb_found_trip, best_price
    else:
        print("No tickets but ", nb_possible_trips, " booked ones at "+
        '%s/%s/%s %s:%s' % (e.day, e.month, e.year, e.hour, e.minute))
        return 0, -1

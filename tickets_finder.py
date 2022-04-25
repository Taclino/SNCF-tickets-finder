import requests
import json
import numpy as np
import datetime
from environment import *  # All the variable such as cards,headers...

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
          "cards": cards,  # [] for none
          "label": "6ed7911c-ed2c-4745-80fd-64e173bb9328"
          }
     ]
     }
}


def look_for_tickets():

    prices = []
    data["search"]["arrival_station_id"] = arrival_station_id
    post_data = json.dumps(data)
    ret = requests.post(url="https://www.trainline.eu/api/v5_1/search",
                        data=post_data, headers=headers)
    # print(ret.json())
    nb_found_trip = 0
    nb_possible_trips = len(ret.json()["folders"])

    for i in range(nb_possible_trips):

        if (ret.json()["folders"][i]["is_sellable"]
            and not(ret.json()["folders"][i]["arrival_different_from_requested"])
                and limit_departure_date > ret.json()["folders"][i]["departure_date"]):

            nb_found_trip += 1
            prices.append(ret.json()["folders"][i]["cents"])

    #---Nouvelle recherche pour les ouigo (Massy TGV)---#

    data["search"]["arrival_station_id"] = second_arrival_station_id
    post_data = json.dumps(data)
    ret = requests.post(url="https://www.trainline.eu/api/v5_1/search",
                            data=post_data, headers=headers)

    nb_possible_trips += len(ret.json()["folders"])
    for i in range(len(ret.json()["folders"])):

        if (ret.json()["folders"][i]["is_sellable"]
                and not(ret.json()["folders"][i]["arrival_different_from_requested"])
                and limit_departure_date > ret.json()["folders"][i]["departure_date"]):

            nb_found_trip += 1
            prices.append(ret.json()["folders"][i]["cents"])

    e = datetime.datetime.now()
    with open('log.txt', 'a') as outfile:
        if nb_found_trip > 0:
            best_price = np.min(prices)/100
            found_str = "Found " + str(nb_found_trip) + " trips starting at " + str(
                best_price) + "€ ! at " + '%s/%s/%s %s:%s' % (e.day, e.month, e.year, e.hour, e.minute)
            print(found_str)
            outfile.write(found_str+'\n')
            return nb_found_trip, best_price
        else:
            not_found_str = "No tickets but " + \
                str(nb_possible_trips) + " booked ones at " + \
                '%s/%s/%s %s:%s' % (e.day, e.month, e.year, e.hour, e.minute)
            print(not_found_str)
            outfile.write(not_found_str+'\n')
            return 0, -1

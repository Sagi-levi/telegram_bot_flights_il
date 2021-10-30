from types import SimpleNamespace

import requests
import json


def Get_flight_info(params):
    url = f"https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/browsequotes/v1.0/IL/USD/en-US/{params[0]}/{params[1]}/{params[2]}"

    headers = {
        'x-rapidapi-host': "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com",
        'x-rapidapi-key': "3c7a176513msh7d7f94d6f1be24dp143570jsn75bc41bccdc7"
    }

    response = requests.request("GET", url, headers=headers)
    print(response.json())
    if not response.json()['Quotes']:
        return
    # response.json comes as a dir
    return DicToString(DicCleaner(response.json()))


def Get_flight_info_dic(params):
    url = f"https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/browsequotes/v1.0/IL/USD/en-US/{params[0]}/{params[1]}/{params[2]}"

    headers = {
        'x-rapidapi-host': "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com",
        'x-rapidapi-key': "3c7a176513msh7d7f94d6f1be24dp143570jsn75bc41bccdc7"
    }

    response = requests.request("GET", url, headers=headers)

    # response.json comes as a dir
    return DicCleaner(response.json())


def DicCleaner(dic):
    info_dir = dict([
        ('To', dic['Places'][0]['CityName']),
        ('From', dic['Places'][1]['CityName']),
        ('MinPrice', dic['Quotes'][0]['MinPrice']),
        ('Direct flight?', 'yes' if dic['Quotes'][0]['Direct'] is True else 'no'),
        ('DepartureDate', dic['Quotes'][0]['OutboundLeg']['DepartureDate']),
        ('Carrier name', dic['Carriers'][0]['Name'])
    ])
    return info_dir


def DicToString(dic):
    string = ''
    for key, value in dic.items():
        string += key
        string += ': '
        string += str(value) + '\n'
    return string

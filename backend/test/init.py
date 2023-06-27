import requests
import json

baseUrl = "http://localhost:8000"

# load from airports.json

def add_airlies():
    with open('data/airlines.json', 'r', encoding='utf-8') as f:
        airlines = json.load(f)
        # print(airports)
        for airline in airlines:
            # print(airport)
            r = requests.post(baseUrl + "/airlines/", json=airline)
            print(r.status_code, r.reason, r.text)


def add_airports():
    with open('data/airports.json', 'r', encoding='utf-8') as f:
        airports = json.load(f)
        # print(airports)
        for airport in airports:
            # print(airport)
            r = requests.post(baseUrl + "/airports/", json=airport)
            print(r.status_code, r.reason, r.text)


def add_superadmin():
    admin = {
        "username": "admin",
        "email": "admin@air.com",
        "password": "123456",
        "admin_type": "Super"
    }
    r = requests.post(baseUrl + "/admins/", json=admin)
    print(r.status_code, r.reason, r.text)


if __name__ == '__main__':
    add_superadmin()
    add_airports()
    add_airlies()
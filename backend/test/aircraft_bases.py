import json


aircraft_bases = {}


def init_boeing_777():
    aircraft_bases["boeing-777"] = {}
    aircraft_bases["boeing-777"]["name"] = "波音-777"
    aircraft_bases["boeing-777"]["model"] = {}
    aircraft_bases["boeing-777"]["model"]["seat_number"] = 0
    aircraft_bases["boeing-777"]["model"]["seat"] = {}
    for i in range(1, 30 + 1):
        for j in "ABCDEF":
            seatid = str(i) + j
            if i < 10:
                seatid = "0" + seatid
            aircraft_bases["boeing-777"]["model"]["seat"][seatid] = {}
            aircraft_bases["boeing-777"]["model"]["seat"][seatid]["type"] = 0
            aircraft_bases["boeing-777"]["model"]["seat"][seatid]["status"] = 0
            aircraft_bases["boeing-777"]["model"]["seat_number"] += 1


def init_aircraft_bases():
    init_boeing_777()


if __name__ == "__main__":
    init_aircraft_bases()
    # print(json.dumps(aircrafts_seats, indent=4))
import json


aircraft_bases = {}


def init_boeing_777():
    aircraft_bases["boeing-777"] = {}
    aircraft_bases["boeing-777"]["name"] = "波音-777"
    aircraft_bases["boeing-777"]["model"] = {}
    aircraft_bases["boeing-777"]["model"]["seat_number"] = 0
    aircraft_bases["boeing-777"]["model"]["seat"] = {}
    for i in range(1, 4 + 1):
        for j in "ABCDEF":
            seatid = str(i) + j
            if i < 10:
                seatid = "0" + seatid
            aircraft_bases["boeing-777"]["model"]["seat"][seatid] = {}
            aircraft_bases["boeing-777"]["model"]["seat"][seatid]["type"] = 2
            aircraft_bases["boeing-777"]["model"]["seat"][seatid]["status"] = 0
            aircraft_bases["boeing-777"]["model"]["seat_number"] += 1
    for i in range(4, 10 + 1):
        for j in "ABCDEF":
            seatid = str(i) + j
            if i < 10:
                seatid = "0" + seatid
            aircraft_bases["boeing-777"]["model"]["seat"][seatid] = {}
            aircraft_bases["boeing-777"]["model"]["seat"][seatid]["type"] = 1
            aircraft_bases["boeing-777"]["model"]["seat"][seatid]["status"] = 0
            aircraft_bases["boeing-777"]["model"]["seat_number"] += 1
    for i in range(10, 35 + 1):
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
    print(json.dumps(aircraft_bases, indent=4))
from sqlalchemy import update, delete
from sqlalchemy.orm import Session

from . import models, schemas

# ==================== AircraftTypes ====================

def get_aircraft_types(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.AircraftType).offset(skip).limit(limit).all()


def get_aircraft_type(db: Session, aircraft_code: str):
    return db.query(models.AircraftType).filter(models.AircraftType.code == aircraft_code).first()


def create_aircraft_type(db: Session, aircraft_type: schemas.AircraftTypeCreate):
    db_aircraft_type = models.AircraftType(**aircraft_type.dict())
    db.add(db_aircraft_type)
    db.commit()
    db.refresh(db_aircraft_type)
    return db_aircraft_type


def delete_aircraft_type(db: Session, aircraft_code: str):
    db_aircraft_type = db.query(models.AircraftType).filter(models.AircraftType.code == aircraft_code).first()
    db.delete(db_aircraft_type)
    db.commit()
    return db_aircraft_type

# ==================== Aircrafts ====================

def get_aircrafts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Aircraft).offset(skip).limit(limit).all()


def get_aircraft(db: Session, aircraft_id: int):
    return db.query(models.Aircraft).filter(models.Aircraft.id == aircraft_id).first()


def get_aircrafts_by_airline_code(db: Session, airline_code: str):
    return db.query(models.Aircraft).filter(models.Aircraft.airline_code == airline_code).all()


def create_aircraft(db: Session, aircraft: schemas.AircraftCreate):
    db_aircraft = models.Aircraft(**aircraft.dict())
    db.add(db_aircraft)
    db.commit()
    db.refresh(db_aircraft)
    return db_aircraft


def delete_aircraft(db: Session, aircraft_id: int):
    db_aircraft = db.query(models.Aircraft).filter(models.Aircraft.id == aircraft_id).first()
    db.delete(db_aircraft)
    db.commit()
    return db_aircraft


# ==================== Airports ====================


def get_airports(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Airport).offset(skip).limit(limit).all()


def get_airport(db: Session, airport_code: str):
    return db.query(models.Airport).filter(models.Airport.code == airport_code).first()


def create_airport(db: Session, airport: schemas.AirportCreate):
    db_airport = models.Airport(**airport.dict())
    db.add(db_airport)
    db.commit()
    db.refresh(db_airport)
    return db_airport


def delete_airport(db: Session, airport_code: str):
    db_airport = db.query(models.Airport).filter(models.Airport.code == airport_code).first()
    db.delete(db_airport)
    db.commit()
    return db_airport


# ==================== Airline ====================

def get_airlines(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Airline).offset(skip).limit(limit).all()


def get_airline(db: Session, airline_code: str):
    return db.query(models.Airline).filter(models.Airline.code == airline_code).first()


def create_airline(db: Session, airline: schemas.AirlineCreate):
    db_airline = models.Airline(**airline.dict())
    db.add(db_airline)
    db.commit()
    db.refresh(db_airline)
    return db_airline


# ==================== FlightTypes ====================


def get_flight_types(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.FlightType).offset(skip).limit(limit).all()


def get_flight_types_by_airline_code(db: Session, airline_code: str):
    return db.query(models.FlightType).filter(models.FlightType.airline_code == airline_code).all()


def get_flight_type(db: Session, flight_type_id: int):
    return db.query(models.FlightType).filter(models.FlightType.id == flight_type_id).first()


def create_flight_type(db: Session, flight_type: schemas.FlightTypeCreate):
    db_flight_type = models.FlightType(**flight_type.dict())
    db.add(db_flight_type)
    db.commit()
    db.refresh(db_flight_type)
    return db_flight_type


def delete_flight_type(db: Session, flight_type_id: int):
    db_flight_type = db.query(models.FlightType).filter(models.FlightType.id == flight_type_id).first()
    db.delete(db_flight_type)
    db.commit()
    return db_flight_type


# ==================== Flights ====================


def get_flights(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Flight).offset(skip).limit(limit).all()


def get_flight(db: Session, flight_id: int):
    return db.query(models.Flight).filter(models.Flight.id == flight_id).first()


def get_flights_by_airline_code(db: Session, airline_code: str):
    aircraft_ids = [aircraft.id for aircraft in get_aircrafts_by_airline_code(db, airline_code)]
    return db.query(models.Flight).filter(models.Flight.aircraft_id.in_(aircraft_ids)).all()


def create_flight(db: Session, flight: schemas.FlightCreate):
    db_flight = models.Flight(**flight.dict())
    db.add(db_flight)
    db.commit()
    db.refresh(db_flight)
    return db_flight


def delete_flight(db: Session, flight_id: int):
    db_flight = db.query(models.Flight).filter(models.Flight.id == flight_id).first()
    db.delete(db_flight)
    db.commit()
    return db_flight


def update_flight(db: Session, flight_id: int, flight: schemas.FlightCreate):
    db_flight = db.query(models.Flight).filter(models.Flight.id == flight_id).first()

    res = db.query(models.Flight).filter(models.Flight.id == flight_id).update({
        models.Flight.aircraft_id: flight.aircraft_id,
        models.Flight.flight_type_id: flight.flight_type_id,
        models.Flight.time_arrival: flight.time_arrival,
        models.Flight.time_departure: flight.time_departure,
        models.Flight.status: flight.status
    }, synchronize_session=False)
    db.commit()
    db.refresh(db_flight)
    return db_flight

# ==================== Books ====================


def get_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Book).offset(skip).limit(limit).all()


def get_book(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def get_book_by_user(db: Session, user_id: int):
    return db.query(models.Book).filter(models.Book.user_id == user_id).all()


def get_book_by_flight(db: Session, flight_id: int):
    return db.query(models.Book).filter(models.Book.flight_id == flight_id).all()


# ==================== Users ====================

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    db.delete(db_user)
    db.commit()
    return db_user


def update_user(db: Session, user_id: int, user: schemas.UserMutable):
    db_user = db.query(models.User).filter(models.User.id == user_id).update({
        models.User.username: user.username,
        models.User.phone: user.phone,
        models.User.fullname: user.fullname,
        models.User.address: user.address,
        models.User.money: user.money,
        models.User.points: user.points
    }, synchronize_session=False)

    db.commit()
    db.refresh(db_user)
    return db_user



# ==================== Admins ====================


def get_admins(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Admin).offset(skip).limit(limit).all()


def get_airport_admins(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Admin).filter(models.Admin.admin_type.like("Airport%")).offset(skip).limit(limit).all()


def get_airline_admins(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Admin).filter(models.Admin.admin_type.like("Airline%")).offset(skip).limit(limit).all()


def get_admin(db: Session, admin_id: int):
    return db.query(models.Admin).filter(models.Admin.id == admin_id).first()


def get_admin_by_email(db: Session, email: str):
    return db.query(models.Admin).filter(models.Admin.email == email).first()


def create_admin(db: Session, admin: schemas.AdminCreate):
    db_admin = models.Admin(**admin.dict())
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin


def delete_admin(db: Session, admin_id: int):
    db_admin = db.query(models.Admin).filter(models.Admin.id == admin_id).first()
    db.delete(db_admin)
    db.commit()
    return db_admin
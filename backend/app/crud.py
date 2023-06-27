from sqlalchemy.orm import Session

from . import models, schemas


# ==================== Aircrafts ====================

def get_aircrafts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Aircraft).offset(skip).limit(limit).all()


def get_aircraft(db: Session, aircraft_code: str):
    return db.query(models.Aircraft).filter(models.Aircraft.code == aircraft_code).first()


def create_aircraft(db: Session, aircraft: schemas.AircraftCreate):
    db_aircraft = models.Aircraft(**aircraft.dict())
    db.add(db_aircraft)
    db.commit()
    db.refresh(db_aircraft)
    return db_aircraft


def delete_aircraft(db: Session, aircraft_code: str):
    db_aircraft = db.query(models.Aircraft).filter(models.Aircraft.code == aircraft_code).first()
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


# ==================== Airline ====================

def get_airlines(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Airline).offset(skip).limit(limit).all()


def get_airline(db: Session, airline_code: int):
    return db.query(models.Airline).filter(models.Airline.code == airline_code).first()


def create_airline(db: Session, airline: schemas.AirlineCreate):
    db_airline = models.Airline(**airline.dict())
    db.add(db_airline)
    db.commit()
    db.refresh(db_airline)
    return db_airline


# ==================== Flights ====================


def get_flights(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Flight).offset(skip).limit(limit).all()


def get_flight(db: Session, flight_id: int):
    return db.query(models.Flight).filter(models.Flight.id == flight_id).first()


# def get_books(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Book).offset(skip).limit(limit).all()


# def get_book(db: Session, book_id: int):
#     return db.query(models.Book).filter(models.Book.id == book_id).first()


# def get_book_by_user(db: Session, user_id: int):
#     return db.query(models.Book).filter(models.Book.user_id == user_id).all()


# def get_book_by_flight(db: Session, flight_code: str):
#     return db.query(models.Book).filter(models.Book.flight_code == flight_code).all()



def get_admins(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Admin).offset(skip).limit(limit).all()


def get_airport_admins(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Admin).filter(models.Admin.admin_type.like("Airport%")).offset(skip).limit(limit).all()


def get_airlines_admins(db: Session, skip: int = 0, limit: int = 100):
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
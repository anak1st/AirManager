from sqlalchemy import update, delete, func
from sqlalchemy.orm import Session

import models
import schemas

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


def update_aircraft_type(db: Session, aircraft_code: str, aircraft_type: schemas.AircraftType):
    db.query(models.AircraftType).filter(models.AircraftType.code == aircraft_code).update({
        models.AircraftType.name: aircraft_type.name,
        models.AircraftType.model: aircraft_type.model
    })

    db.commit()
    return db.query(models.AircraftType).filter(models.AircraftType.code == aircraft_code).first()



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
    flight_ids = get_flights_by_aircraft_id(db, aircraft_id)
    for flight_id in flight_ids:
        flight = schemas.Flight.from_orm(flight_id)
        delete_flight(db, flight.id)


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


# def delete_airport(db: Session, airport_code: str):
#     db_airport = db.query(models.Airport).filter(models.Airport.code == airport_code).first()
#     db.delete(db_airport)
#     db.commit()
#     return db_airport


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
    flight_ids = get_flights_by_flight_type_id(db, flight_type_id)
    for flight_id in flight_ids:
        flight = schemas.Flight.from_orm(flight_id)
        delete_flight(db, flight.id)

    db_flight_type = db.query(models.FlightType).filter(models.FlightType.id == flight_type_id).first()
    db.delete(db_flight_type)
    db.commit()
    return db_flight_type


def get_flight_types_by_airports(db: Session, 
                                 airport_code_departure: str, 
                                 airport_code_arrival: str):
    if airport_code_departure == 'ALL':
        return db.query(models.FlightType).filter(
            models.FlightType.airport_code_arrival == airport_code_arrival).all()
    elif airport_code_arrival == 'ALL':
        return db.query(models.FlightType).filter(
            models.FlightType.airport_code_departure == airport_code_departure).all()
    else:
        return db.query(models.FlightType).filter(
            models.FlightType.airport_code_departure == airport_code_departure, 
            models.FlightType.airport_code_arrival == airport_code_arrival).all()



# ==================== Flights ====================


def get_flights(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Flight).offset(skip).limit(limit).all()


def get_flight(db: Session, flight_id: int):
    return db.query(models.Flight).filter(models.Flight.id == flight_id).first()


def get_flights_by_aircraft_id(db: Session, aircraft_id):
    return db.query(models.Flight).filter(models.Flight.aircraft_id == aircraft_id).all()


def get_flights_by_flight_type_id(db: Session, flight_type_id):
    return db.query(models.Flight).filter(models.Flight.flight_type_id == flight_type_id).all()


def get_flights_by_airports(db: Session, airport_code_departure: str, airport_code_arrival: str):
    flight_types = get_flight_types_by_airports(db, airport_code_departure, airport_code_arrival)
    flight_type_ids = [flight_type.id for flight_type in flight_types]
    return db.query(models.Flight).filter(models.Flight.flight_type_id.in_(flight_type_ids)).all()


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
    res = get_books_by_flight(db, flight_id)
    for r in res:
        book = schemas.Book.from_orm(r)
        delete_book(db, book.id)

    res = get_books_history_by_flight(db, flight_id)
    for r in res:
        book_history = schemas.Book.from_orm(r)
        delete_book_history(db, book_history.id)

    db_flight = db.query(models.Flight).filter(models.Flight.id == flight_id).first()
    db.delete(db_flight)
    db.commit()
    return db_flight


def update_flight(db: Session, flight_id: int, flight: schemas.FlightCreate):
    db.query(models.Flight).filter(models.Flight.id == flight_id).update({
        models.Flight.aircraft_id: flight.aircraft_id,
        models.Flight.flight_type_id: flight.flight_type_id,
        models.Flight.time_arrival: flight.time_arrival,
        models.Flight.time_departure: flight.time_departure,
        models.Flight.status: flight.status,
        models.Flight.price0: flight.price0,
        models.Flight.price1: flight.price1,
        models.Flight.price2: flight.price2,
    }, synchronize_session=False)
    db.commit()
    db_flight = db.query(models.Flight).filter(models.Flight.id == flight_id).first()
    return db_flight

# ==================== Books ====================


def get_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Book).offset(skip).limit(limit).all()


def get_books_history(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.BookHistory).offset(skip).limit(limit).all()


def get_book(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def delete_book(db: Session, book_id: int, move_to_history: bool = True):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    book = schemas.BookCreate.from_orm(db_book)
    book.pay = 0
    if move_to_history:
        db_book_history = models.BookHistory(**book.dict())
        db.add(db_book_history)
    db.delete(db_book)
    db.commit()
    return db_book


def delete_book_history(db: Session, book_id: int):
    db_book_history = db.query(models.BookHistory).filter(models.BookHistory.id == book_id).first()
    db.delete(db_book_history)
    db.commit()
    return db_book_history


def get_books_by_user(db: Session, user_id: int):
    return db.query(models.Book).filter(models.Book.user_id == user_id).all()


def get_books_by_flight(db: Session, flight_id: int):
    return db.query(models.Book).filter(models.Book.flight_id == flight_id).all()


def get_books_history_by_user(db: Session, user_id: int):
    return db.query(models.BookHistory).filter(models.BookHistory.user_id == user_id).all()


def get_books_history_by_flight(db: Session, flight_id: int):
    return db.query(models.BookHistory).filter(models.BookHistory.flight_id == flight_id).all()


def get_books_num_by_flight(db: Session, flight_id: int):
    return db.query(models.Book).filter(models.Book.flight_id == flight_id).count()


def get_books_pay_by_flight(db: Session, flight_id: int):
    cursor = db.query(func.sum(models.Book.pay)).filter(models.Book.flight_id == flight_id)
    total = cursor.scalar()
    if total is None:
        total = 0
    return total


def get_books_num_by_airline_code(db: Session, airline_code: str):
    flight_ids = [flight.id for flight in get_flights_by_airline_code(db, airline_code)]
    return db.query(models.Book).filter(models.Book.flight_id.in_(flight_ids)).count()


def get_books_pay_by_airline_code(db: Session, airline_code: str):
    flight_ids = [flight.id for flight in get_flights_by_airline_code(db, airline_code)]
    cursor = db.query(func.sum(models.Book.pay)).filter(models.Book.flight_id.in_(flight_ids))
    total = cursor.scalar()
    if total is None:
        total = 0
    return total

# ==================== Users ====================

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()



def search_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username.like(f'%{username}%')).all()


def search_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email.like(f'%{email}%')).all()


def search_user_by_fullname(db: Session, fullname: str):
    return db.query(models.User).filter(models.User.fullname.like(f'%{fullname}%')).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    res = get_books_by_user(db, user_id)
    for r in res:
        book = schemas.Book.from_orm(r)
        delete_book(db, book.id, False)

    res = get_books_history_by_user(db, user_id)
    for r in res:
        book = schemas.Book.from_orm(r)
        delete_book_history(db, book.id)

    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    db.delete(db_user)
    db.commit()
    return db_user


def update_user(db: Session, user_id: int, user: schemas.UserMutable):
    db.query(models.User).filter(models.User.id == user_id).update({
        models.User.username: user.username,
        models.User.phone: user.phone,
        models.User.fullname: user.fullname,
        models.User.address: user.address,
    }, synchronize_session=False)

    db.commit()
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    return db_user


def update_user_money(db: Session, user_id: int, money: int):
    db_user = db.query(models.User).filter(models.User.id == user_id, 
                                           models.User.money + money >= 0).first()
    if db_user is None:
        print("User not found or not enough money")
        return None

    db.query(models.User).filter(models.User.id == user_id).update({
        models.User.money: models.User.money + money
    }, synchronize_session=False)

    db.commit()
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    return db_user


def update_user_points(db: Session, user_id: int, points: int):
    db.query(models.User).filter(models.User.id == user_id).update({
        models.User.points: models.User.points + points
    }, synchronize_session=False)

    db.commit()
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    return db_user


def update_user_password(db: Session, user_id: int, password: str):
    db.query(models.User).filter(models.User.id == user_id).update({
        models.User.password: password
    }, synchronize_session=False)

    db.commit()
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
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
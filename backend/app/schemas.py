from datetime import datetime
from pydantic import BaseModel


# ==================== Base ====================

class AircraftBase(BaseModel):
    code: str
    name: str
    airline_code: str
    seat_vip: int
    seat_common: int


class AirportBase(BaseModel):
    code: str
    name: str
    country: str
    city: str


class AirlineBase(BaseModel):
    code: str
    name: str
    country: str


class FlightBase(BaseModel):
    aircraft_code: str
    airport_code_departure: str
    airport_code_arrival: str
    time_departure: datetime
    time_arrival: datetime
    status: str
    sold_seat_vip: int
    sold_seat_common: int
    price_vip: int
    price_common: int


# class BookBase(BaseModel):
#     user_id: int
#     flight_id: int
#     seat_type: int
#     status: str


# class UserBase(BaseModel):
#     username: str
#     email: str
#     phone: str
#     # password: str
#     address: str
#     full_name: str

class AdminBase(BaseModel):
    email: str


# ==================== Create ====================

class AircraftCreate(AircraftBase):
    pass


class AirportCreate(AirportBase):
    pass


class AirlineCreate(AirlineBase):
    pass


class FlightCreate(FlightBase):
    pass


class AdminCreate(AdminBase):
    username: str
    password: str
    admin_type: str


# class BookCreate(BookBase):
#     pass


# class UserCreate(UserBase):
#     password: str
#     pass


# ==================== GET ====================

class Aircraft(AircraftBase):
    airline: AirlineBase

    class Config:
        orm_mode = True


class Airport(AirportBase):
    class Config:
        orm_mode = True


class Airline(AirlineBase):
    aircrafts: list[AircraftBase] = []

    class Config:
        orm_mode = True


class Flight(FlightBase):
    id: int
    aircraft: AircraftBase
    airport_departure: AirportBase
    airport_arrival: AirportBase


    class Config:
        orm_mode = True


class Admin(AdminBase):
    id : int
    username: str
    admin_type: str

    class Config:
        orm_mode = True


# class Book(BookBase):
#     id: int

#     class Config:
#         orm_mode = True


# class User(UserBase):
#     id: int
#     # books: list[BookBase] = []

#     class Config:
#         orm_mode = True

# ==================== Login ====================

class AdminLogin(AdminBase):
    password: str

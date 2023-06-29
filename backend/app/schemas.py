from datetime import datetime
from pydantic import BaseModel
import json


# ==================== Base ====================

class AircraftTypeBase(BaseModel):
    code: str
    name: str
    model: str

    class Config:
        orm_mode = True


class AirportBase(BaseModel):
    code: str
    name: str
    country: str
    city: str
    lat: float
    lng: float

    class Config:
        orm_mode = True


class AirlineBase(BaseModel):
    code: str
    name: str
    country: str

    class Config:
        orm_mode = True


class AircraftBase(BaseModel):
    type_code: str
    airline_code: str

    class Config:
        orm_mode = True


class FlightTypeBase(BaseModel):
    airline_code: str
    airport_code_departure: str
    airport_code_arrival: str

    class Config:
        orm_mode = True


class FlightBase(BaseModel):
    aircraft_id: int
    flight_type_id: int
    time_departure: datetime
    time_arrival: datetime
    status: str

    price0: int
    price1: int
    price2: int

    class Config:
        orm_mode = True


class BookBase(BaseModel):
    user_id: int
    flight_id: int
    seat: int
    status: str
    pay: int


class UserBase(BaseModel):
    email: str


class UserMutable(BaseModel):
    username: str
    fullname: str
    phone: str
    address: str
    money: int
    points: int


# ==================== Create ====================

class AircraftTypeCreate(AircraftTypeBase):
    pass


class AirportCreate(AirportBase):
    pass


class AirlineCreate(AirlineBase):
    pass


class AircraftCreate(AircraftBase):
    pass


class FlightTypeCreate(FlightTypeBase):
    pass


class FlightCreate(FlightBase):
    pass


class BookCreate(BookBase):
    pass


class UserCreate(UserBase):
    username: str
    phone: str
    address: str
    fullname: str
    password: str
    pass


# ==================== GET ====================

class AircraftType(AircraftTypeBase):
    class Config:
        orm_mode = True


class Airport(AirportBase):
    class Config:
        orm_mode = True


class Airline(AirlineBase):

    # ORM
    aircrafts: list[AircraftBase] = []
    flight_types: list[FlightTypeBase] = []

    class Config:
        orm_mode = True


class AircraftWithoutFlights(AircraftBase):
    id : int
    
    # ORM
    type : AircraftTypeBase
    airline: AirlineBase

    class Config:
        orm_mode = True

class Aircraft(AircraftBase):
    id : int
    
    # ORM
    type : AircraftTypeBase
    airline: AirlineBase
    
    flights: list[FlightBase] = []

    class Config:
        orm_mode = True


class FlightTypeWithoutFlights(FlightTypeBase):
    id : int

    airport_departure: AirportBase
    airport_arrival: AirportBase

    class Config:
        orm_mode = True


class FlightType(FlightTypeBase):
    id : int

    airport_departure: AirportBase
    airport_arrival: AirportBase

    airline: AirlineBase
    flights: list[FlightBase] = []


class Flight(FlightBase):
    id: int

    # ORM
    aircraft: AircraftWithoutFlights
    flight_type: FlightTypeWithoutFlights

    books: list[BookBase] = []

    class Config:
        orm_mode = True


class User(UserBase):
    id: int
    username: str
    fullname: str
    phone: str
    address: str
    money: int
    points: int

    # ORM
    books: list[BookBase] = []

    class Config:
        orm_mode = True





class Book(BookBase):
    id: int

    # ORM
    user: UserBase
    flight: FlightBase

    class Config:
        orm_mode = True


# ==================== Admin ====================

class AdminBase(BaseModel):
    email: str


class Admin(AdminBase):
    id : int

    username: str
    admin_type: str

    class Config:
        orm_mode = True


class AdminCreate(AdminBase):
    username: str
    password: str
    admin_type: str


# ==================== Login ====================


class UserLogin(UserBase):
    password: str


class AdminLogin(AdminBase):
    password: str

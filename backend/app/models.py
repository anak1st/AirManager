from sqlalchemy import Boolean, Float, Column, ForeignKey, Integer, String, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship

from .database import Base


# 基本飞机模型
class AircraftType(Base):
    __tablename__ = 'aircraft_types'

    code = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    model = Column(String)


# 机场
class Airport(Base):
    __tablename__ = 'airports'

    code = Column(String, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    country = Column(String)
    city = Column(String)
    lat = Column(Float)
    lng = Column(Float)


# 航空公司
class Airline(Base):
    __tablename__ = 'airlines'

    code = Column(String, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    country = Column(String)

    aircrafts = relationship("Aircraft", back_populates="airline")
    flight_types = relationship("FlightType", back_populates="airline")


# 飞机
class Aircraft(Base):
    __tablename__ = 'aircrafts'

    id = Column(Integer, primary_key=True, index=True)
    type_code = Column(String, ForeignKey("aircraft_types.code"))
    airline_code = Column(String, ForeignKey("airlines.code"))

    type = relationship("AircraftType")
    airline = relationship("Airline", back_populates="aircrafts")

    flights = relationship("Flight", back_populates="aircraft")


# 航线特点
class FlightType(Base):
    __tablename__ = 'flight_types'

    id = Column(Integer, primary_key=True, index=True)
    airline_code = Column(String, ForeignKey("airlines.code"))
    airport_code_departure = Column(String, ForeignKey("airports.code"))
    airport_code_arrival = Column(String, ForeignKey("airports.code"))

    UniqueConstraint(airline_code, airport_code_departure, airport_code_arrival)

    airport_departure = relationship("Airport", foreign_keys=[airport_code_departure])
    airport_arrival = relationship("Airport", foreign_keys=[airport_code_arrival])
    airline = relationship("Airline", back_populates="flight_types")
    flights = relationship("Flight", back_populates="flight_type")


# 航线
class Flight(Base):
    __tablename__ = 'flights'

    id = Column(Integer, primary_key=True, index=True)
    time_departure = Column(DateTime)
    time_arrival = Column(DateTime)
    status = Column(String)

    aircraft_id = Column(Integer, ForeignKey("aircrafts.id"))
    flight_type_id = Column(Integer, ForeignKey("flight_types.id"))

    aircraft = relationship("Aircraft", back_populates="flights")
    flight_type = relationship("FlightType", back_populates="flights")
    books = relationship("Book", back_populates="flight")


class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    password = Column(String)
    address = Column(String)
    fullname = Column(String)
    
    money = Column(Integer, default=0)
    points = Column(Integer, default=0)

    books = relationship("Book", back_populates="user")


# 订票
class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    flight_id = Column(Integer, ForeignKey("flights.id"))
    seat = Column(String)
    status = Column(String)

    user = relationship("User", back_populates="books")
    flight = relationship("Flight", back_populates="books")

    UniqueConstraint(flight_id, seat)



class BookHistory(Base):
    __tablename__ = "books_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    flight_id = Column(Integer, ForeignKey("flights.id"))
    seat = Column(String)
    status = Column(String)

    UniqueConstraint(flight_id, seat)


class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    username = Column(String)
    admin_type = Column(String)

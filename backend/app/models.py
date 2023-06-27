from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, JSON
from sqlalchemy.orm import relationship

from .database import Base


class Aircraft(Base):
    __tablename__ = 'aircrafts'

    code = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    airline_code = Column(String, ForeignKey("airlines.code"))
    seat_vip = Column(Integer)
    seat_common = Column(Integer)

    airline = relationship("Airline", back_populates="aircrafts")


class Airport(Base):
    __tablename__ = 'airports'

    code = Column(String, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    country = Column(String)
    city = Column(String)


class Airline(Base):
    __tablename__ = 'airlines'

    code = Column(String, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    country = Column(String)

    aircrafts = relationship("Aircraft", back_populates="airline")


class Flight(Base):
    __tablename__ = 'flights'

    id = Column(Integer, primary_key=True, index=True)
    aircraft_code = Column(String, ForeignKey("aircrafts.code"))
    airport_code_departure = Column(String, ForeignKey("airports.code"))
    airport_code_arrival = Column(String, ForeignKey("airports.code"))
    time_departure = Column(DateTime)
    time_arrival = Column(DateTime)
    status = Column(String, index=True)
    sold_seat_vip = Column(Integer)
    sold_seat_common = Column(Integer)
    price_vip = Column(Integer)
    price_common = Column(Integer)

    aircraft = relationship("Aircraft")
    airport_departure = relationship("Airport", foreign_keys=[airport_code_departure])
    airport_arrival = relationship("Airport", foreign_keys=[airport_code_arrival])
    # books = relationship("Book", back_populates="flight")


# class User(Base):
#     __tablename__ = 'users'
    
#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String, index=True)
#     email = Column(String, unique=True, index=True)
#     phone = Column(String, unique=True, index=True)
#     password = Column(String)
#     address = Column(String)
#     full_name = Column(String)

#     # books = relationship("Book", back_populates="user")


# class Book(Base):
#     __tablename__ = "books"

#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey("users.id"))
#     flight_id = Column(Integer, ForeignKey("flights.id"))
#     seat_type = Column(Integer)
#     status = Column(String)

#     # user = relationship("User", back_populates="books")
#     # flight = relationship("Flight", back_populates="books")


class Admin(Base):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    username = Column(String)
    admin_type = Column(String)
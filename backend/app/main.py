import json
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

from .utils import hash, get_distance_hav

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:9000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency
def get_db():
    db = SessionLocal()
    db.expire_on_commit = False
    try:
        yield db
    finally:
        db.close()

# ==================== AircraftTypes ====================

@app.get("/aircraft_types/", response_model=list[schemas.AircraftType])
def read_aircrafts_types(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    aircrafts_types = crud.get_aircraft_types(db, skip=skip, limit=limit)
    return aircrafts_types


@app.get("/aircraft_types/code/{aircraft_code}", response_model=schemas.AircraftType)
def read_aircraft_type(aircraft_code: str, db: Session = Depends(get_db)):
    db_aircraft_type = crud.get_aircraft_type(db, aircraft_code=aircraft_code)
    if db_aircraft_type is None:
        raise HTTPException(status_code=404, detail="AircraftType not found")
    return db_aircraft_type


@app.post("/aircraft_types/", response_model=schemas.AircraftType)
def create_aircraft_type(aircraft_type: schemas.AircraftTypeCreate, db: Session = Depends(get_db)):
    db_aircraft_type = crud.get_aircraft_type(db, aircraft_code=aircraft_type.code)
    if db_aircraft_type:
        raise HTTPException(status_code=400, detail="AircraftType already registered")
    return crud.create_aircraft_type(db=db, aircraft_type=aircraft_type)


@app.delete("/aircraft_types/code/{aircraft_code}", response_model=schemas.AircraftType)
def delete_aircraft_type(aircraft_code: str, db: Session = Depends(get_db)):
    db_aircraft_type = crud.get_aircraft_type(db, aircraft_code=aircraft_code)
    if db_aircraft_type is None:
        raise HTTPException(status_code=404, detail="AircraftType not found")
    return crud.delete_aircraft_type(db=db, aircraft_code=aircraft_code)

# ==================== Airports ====================

@app.get("/airports/", response_model=list[schemas.Airport])
def read_airports(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    airports = crud.get_airports(db, skip=skip, limit=limit)
    return airports


@app.get("/airports/code/{airport_code}", response_model=schemas.Airport)
def read_airport(airport_code: str, db: Session = Depends(get_db)):
    db_airport = crud.get_airport(db, airport_code=airport_code)
    if db_airport is None:
        raise HTTPException(status_code=404, detail="Airport not found")
    return db_airport


@app.post("/airports/", response_model=schemas.Airport)
def create_airport(airport: schemas.AirportCreate, db: Session = Depends(get_db)):
    db_airport = crud.get_airport(db, airport_code=airport.code)
    if db_airport:
        raise HTTPException(status_code=400, detail="Airport already registered")
    return crud.create_airport(db=db, airport=airport)


@app.delete("/airports/code/{airport_code}", response_model=schemas.Airport)
def delete_airport(airport_code: str, db: Session = Depends(get_db)):
    db_airport = crud.get_airport(db, airport_code=airport_code)
    if db_airport is None:
        raise HTTPException(status_code=404, detail="Airport not found")
    return crud.delete_airport(db=db, airport_code=airport_code)


# ==================== Airlines ====================
@app.get("/airlines/", response_model=list[schemas.Airline])
def read_airlines(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    airlines = crud.get_airlines(db, skip=skip, limit=limit)
    return airlines


@app.get("/airlines/code/{airline_code}", response_model=schemas.Airline)
def read_airline(airline_code: str, db: Session = Depends(get_db)):
    db_airline = crud.get_airline(db, airline_code=airline_code)
    if db_airline is None:
        raise HTTPException(status_code=404, detail="Airline not found")
    return db_airline


@app.post("/airlines/", response_model=schemas.Airline)
def create_airline(airline: schemas.AirlineCreate, db: Session = Depends(get_db)):
    db_airline = crud.get_airline(db, airline_code=airline.code)
    if db_airline:
        raise HTTPException(status_code=400, detail="Airline already registered")
    return crud.create_airline(db=db, airline=airline)

# ==================== Aircrafts ====================

@app.get("/aircrafts/", response_model=list[schemas.Aircraft])
def read_aircrafts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    aircrafts = crud.get_aircrafts(db, skip=skip, limit=limit)
    return aircrafts


@app.get("/aircrafts/id/{aircraft_id}", response_model=schemas.Aircraft)
def read_aircraft(aircraft_id: int, db: Session = Depends(get_db)):
    db_aircraft = crud.get_aircraft(db, aircraft_id=aircraft_id)
    if db_aircraft is None:
        raise HTTPException(status_code=404, detail="Aircraft not found")
    return db_aircraft


@app.get("/aircrafts/airline_code/{airline_code}", response_model=list[schemas.Aircraft])
def read_aircraft_by_airline_code(airline_code: str, db: Session = Depends(get_db)):
    db_aircraft = crud.get_aircrafts_by_airline_code(db, airline_code=airline_code)
    return db_aircraft



@app.post("/aircrafts/", response_model=schemas.Aircraft)
def create_aircraft(aircraft: schemas.AircraftCreate, db: Session = Depends(get_db)):
    return crud.create_aircraft(db=db, aircraft=aircraft)


@app.delete("/aircrafts/id/{aircraft_id}", response_model=schemas.Aircraft)
def delete_aircraft(aircraft_id: int, db: Session = Depends(get_db)):
    db_aircraft = crud.get_aircraft(db, aircraft_id=aircraft_id)
    if db_aircraft is None:
        raise HTTPException(status_code=404, detail="Aircraft not found")
    return crud.delete_aircraft(db=db, aircraft_id=aircraft_id)

# ==================== FlightTypes ====================

@app.get("/flight_types/", response_model=list[schemas.FlightType])
def read_flight_types(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    flight_types = crud.get_flight_types(db, skip=skip, limit=limit)
    return flight_types


@app.get("/flight_types/id/{flight_type_id}", response_model=schemas.FlightType)
def read_flight_type(flight_type_id: int, db: Session = Depends(get_db)):
    db_flight_type = crud.get_flight_type(db, flight_type_id=flight_type_id)
    if db_flight_type is None:
        raise HTTPException(status_code=404, detail="Flight Type not found")
    return db_flight_type


@app.get("/flight_types/airline_code/{airline_code}", response_model=list[schemas.FlightType])
def read_flight_type_by_airline_code(airline_code: str, db: Session = Depends(get_db)):
    airline = crud.get_airline(db, airline_code=airline_code)
    if airline is None:
        raise HTTPException(status_code=404, detail="Airline not found")
    db_flight_type = crud.get_flight_types_by_airline_code(db, airline_code=airline_code)
    return db_flight_type


@app.post("/flight_types/", response_model=schemas.FlightType)
def create_flight_type(flight_type: schemas.FlightTypeCreate, db: Session = Depends(get_db)):
    return crud.create_flight_type(db=db, flight_type=flight_type)


@app.delete("/flight_types/id/{flight_type_id}", response_model=schemas.FlightType)
def delete_flight_type(flight_type_id: int, db: Session = Depends(get_db)):
    db_flight_type = crud.get_flight_type(db, flight_type_id=flight_type_id)
    if db_flight_type is None:
        raise HTTPException(status_code=404, detail="Flight Type not found")
    return crud.delete_flight_type(db=db, flight_type_id=flight_type_id)


# ==================== Flights ====================
@app.get("/flights/", response_model=list[schemas.Flight])
def read_flights(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    flights = crud.get_flights(db, skip=skip, limit=limit)
    return flights


@app.get("/flights/id/{flight_id}", response_model=schemas.Flight)
def read_flight(flight_id: int, db: Session = Depends(get_db)):
    db_flight = crud.get_flight(db, flight_id=flight_id)
    if db_flight is None:
        raise HTTPException(status_code=404, detail="Flight not found")
    return db_flight


@app.get("/flights/airline_code/{airline_code}", response_model=list[schemas.Flight])
def read_flight_by_airline_code(airline_code: str, db: Session = Depends(get_db)):
    airline = crud.get_airline(db, airline_code=airline_code)
    if airline is None:
        raise HTTPException(status_code=404, detail="Airline not found")
    db_flight = crud.get_flights_by_airline_code(db, airline_code=airline_code)
    return db_flight


@app.post("/flights/", response_model=schemas.Flight)
def create_flight(flight: schemas.FlightCreate, db: Session = Depends(get_db)):
    return crud.create_flight(db=db, flight=flight)


@app.delete("/flights/id/{flight_id}", response_model=schemas.Flight)
def delete_flight(flight_id: int, db: Session = Depends(get_db)):
    db_flight = crud.get_flight(db, flight_id=flight_id)
    if db_flight is None:
        raise HTTPException(status_code=404, detail="Flight not found")
    return crud.delete_flight(db=db, flight_id=flight_id)


@app.put("/flights/id/{flight_id}", response_model=schemas.Flight)
def update_flight(flight_id: int, flight: schemas.FlightCreate, db: Session = Depends(get_db)):
    db_flight = crud.get_flight(db, flight_id=flight_id)
    if db_flight is None:
        raise HTTPException(status_code=404, detail="Flight not found")
    return crud.update_flight(db=db, flight_id=flight_id, flight=flight)

# ==================== Books ====================

@app.get("/books/", response_model=list[schemas.Book])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    books = crud.get_books(db, skip=skip, limit=limit)
    return books


@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)




@app.get("/books/id/{book_id}", response_model=schemas.Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book


@app.get("/books/user/{user_id}", response_model=list[schemas.Book])
def read_book_by_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_book = crud.get_book_by_user(db, user_id=user_id)
    return db_book


@app.get("/books/flight/{flight_id}", response_model=list[schemas.Book])
def read_book_by_flight(flight_id: int, db: Session = Depends(get_db)):
    flight = crud.get_flight(db, flight_id=flight_id)
    if flight is None:
        raise HTTPException(status_code=404, detail="Flight not found")
    db_book = crud.get_book_by_flight(db, flight_id=flight_id)
    return db_book


# ==================== Users ====================

@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/id/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user.password = hash(user.password)
    return crud.create_user(db=db, user=user)


@app.delete("/users/id/{user_id}", response_model=schemas.User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.delete_user(db=db, user_id=user_id)


@app.post("/users/login", response_model=schemas.User)
def login_user(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user.password = hash(user.password)
    if db_user.password != user.password: # type: ignore
        print(db_user.password, user.password)
        raise HTTPException(status_code=400, detail="Incorrect password")
    return db_user


@app.put("/users/id/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserMutable, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.update_user(db=db, user_id=user_id, user=user)


# ==================== Admins ====================

@app.get("/admins/", response_model=list[schemas.Admin])
def read_admins(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    admins = crud.get_admins(db, skip=skip, limit=limit)
    return admins


@app.post("/admins/login", response_model=schemas.Admin)
def login_admin(admin: schemas.AdminLogin, db: Session = Depends(get_db)):
    admin.password = hash(admin.password)
    db_admin = crud.get_admin_by_email(db, email=admin.email)
    if db_admin is None:
        raise HTTPException(status_code=404, detail="Admin not found")
    if db_admin.password != admin.password: # type: ignore
        print(db_admin.password, admin.password)
        raise HTTPException(status_code=400, detail="Incorrect password")
    return db_admin


@app.get("/admins/airpots/", response_model=list[schemas.Admin])
def get_airport_admins(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    admins = crud.get_airport_admins(db, skip=skip, limit=limit)
    return admins


@app.get("/admins/airlines/", response_model=list[schemas.Admin])
def get_airline_admins(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    admins = crud.get_airline_admins(db, skip=skip, limit=limit)
    return admins



@app.get("/admins/id/{admin_id}", response_model=schemas.Admin)
def read_admin(admin_id: int, db: Session = Depends(get_db)):
    db_admin = crud.get_admin(db, admin_id=admin_id)
    if db_admin is None:
        raise HTTPException(status_code=404, detail="Admin not found")
    return db_admin


@app.post("/admins/", response_model=schemas.Admin)
def create_admin(admin: schemas.AdminCreate, db: Session = Depends(get_db)):
    admin.password = hash(admin.password)
    db_admin = crud.get_admin_by_email(db, email=admin.email)
    if db_admin:
        raise HTTPException(status_code=400, detail="Admin already registered")
    return crud.create_admin(db=db, admin=admin)


@app.delete("/admins/id/{admin_id}/", response_model=schemas.Admin)
def delete_admin(admin_id: int, db: Session = Depends(get_db)):
    db_admin = crud.get_admin(db, admin_id=admin_id)
    if db_admin is None:
        raise HTTPException(status_code=404, detail="Admin not found")
    return crud.delete_admin(db=db, admin_id=admin_id)

# ==================== Utils ====================
@app.get("/airports/dis/", response_model=float)
def get_airport_distance(airport1_code: str, airport2_code: str, db: Session = Depends(get_db)):
    airport1 = crud.get_airport(db, airport_code=airport1_code)
    airport2 = crud.get_airport(db, airport_code=airport2_code)
    if airport1 is None or airport2 is None:
        raise HTTPException(status_code=404, detail="Airport not found")
    return get_distance_hav(airport1.lat, 
                            airport1.lng,
                            airport2.lat,
                            airport2.lng)
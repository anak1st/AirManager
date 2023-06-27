from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

from .utils.hash import hash

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
    try:
        yield db
    finally:
        db.close()


# ==================== Aircrafts ====================

@app.get("/aircrafts/", response_model=list[schemas.Aircraft])
def read_aircrafts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    aircrafts = crud.get_aircrafts(db, skip=skip, limit=limit)
    return aircrafts


@app.get("/aircrafts/code/{aircraft_code}", response_model=schemas.Aircraft)
def read_aircraft(aircraft_code: str, db: Session = Depends(get_db)):
    db_aircraft = crud.get_aircraft(db, aircraft_code=aircraft_code)
    if db_aircraft is None:
        raise HTTPException(status_code=404, detail="Aircraft not found")
    return db_aircraft


@app.post("/aircrafts/", response_model=schemas.Aircraft)
def create_aircraft(aircraft: schemas.AircraftCreate, db: Session = Depends(get_db)):
    db_aircraft = crud.get_aircraft(db, aircraft_code=aircraft.code)
    if db_aircraft:
        raise HTTPException(status_code=400, detail="Aircraft already registered")
    return crud.create_aircraft(db=db, aircraft=aircraft)


@app.delete("/aircrafts/code/{aircraft_code}", response_model=schemas.Aircraft)
def delete_aircraft(aircraft_code: str, db: Session = Depends(get_db)):
    db_aircraft = crud.get_aircraft(db, aircraft_code=aircraft_code)
    if db_aircraft is None:
        raise HTTPException(status_code=404, detail="Aircraft not found")
    return crud.delete_aircraft(db=db, aircraft_code=aircraft_code)


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


@app.post("/airlines/", response_model=schemas.Airline)
def create_airline(airline: schemas.AirlineCreate, db: Session = Depends(get_db)):
    db_airline = crud.get_airline(db, airline_code=airline.code)
    if db_airline:
        raise HTTPException(status_code=400, detail="Airline already registered")
    return crud.create_airline(db=db, airline=airline)


# ==================== Flights ====================
@app.get("/flights/", response_model=list[schemas.Flight])
def read_flights(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    flights = crud.get_flights(db, skip=skip, limit=limit)
    return flights


# ==================== Bookings ====================

# ==================== Users ====================

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
    if db_admin.password != admin.password:
        print(db_admin.password, admin.password)
        raise HTTPException(status_code=400, detail="Incorrect password")
    return db_admin


@app.get("/admins/airpots/", response_model=list[schemas.Admin])
def get_airport_admins(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    admins = crud.get_airport_admins(db, skip=skip, limit=limit)
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

@app.delete("/admins/id/{admin_id}", response_model=schemas.Admin)
def delete_admin(admin_id: int, db: Session = Depends(get_db)):
    db_admin = crud.get_admin(db, admin_id=admin_id)
    if db_admin is None:
        raise HTTPException(status_code=404, detail="Admin not found")
    return crud.delete_admin(db=db, admin_id=admin_id)
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, Float, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import time

# Initialisation de l'application FastAPI
app = FastAPI()

# Configurations de la base de données
DATABASE_URL = "postgresql://postgres:u6x5qhup@db/housing_db"

# Connexion à PostgreSQL
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base pour les modèles SQLAlchemy
Base = declarative_base()

# Modèle de table pour les maisons
class House(Base):
    __tablename__ = "houses"
    id = Column(Integer, primary_key=True, index=True)
    longitude = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)
    housing_median_age = Column(Integer, nullable=False)
    total_rooms = Column(Integer, nullable=False)
    total_bedrooms = Column(Integer, nullable=False)
    population = Column(Integer, nullable=False)
    households = Column(Integer, nullable=False)
    median_income = Column(Float, nullable=False)
    median_house_value = Column(Float, nullable=False)
    ocean_proximity = Column(String, nullable=False)

# Création des tables si elles n'existent pas
def create_tables():
    Base.metadata.create_all(bind=engine)

# Fonction pour attendre que la base de données soit prête
def wait_for_db():
    print("Waiting for the database to be ready...")
    while True:
        try:
            conn = engine.connect()
            conn.close()
            print("Database is ready!")
            break
        except Exception as e:
            print(f"Database not ready, waiting 1 second... {e}")
            time.sleep(1)

# Modèle Pydantic pour les entrées API
class HouseCreate(BaseModel):
    longitude: float
    latitude: float
    housing_median_age: int
    total_rooms: int
    total_bedrooms: int
    population: int
    households: int
    median_income: float
    median_house_value: float
    ocean_proximity: str

# Attente de la base de données et création des tables
wait_for_db()
create_tables()

# Route GET pour récupérer toutes les maisons
@app.get("/houses")
def get_houses():
    db = SessionLocal()
    try:
        houses = db.query(House).all()
        return {"houses": houses}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

# Route POST pour ajouter une nouvelle maison
@app.post("/houses")
def create_house(house: HouseCreate):
    db = SessionLocal()
    try:
        db_house = House(**house.dict())
        db.add(db_house)
        db.commit()
        db.refresh(db_house)
        return {"message": "House created successfully", "house": db_house}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

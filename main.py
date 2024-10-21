# uvicorn main:app

from typing import Union 
from fastapi import FastAPI, Depends #pip install fastapi, uvicorn
from typing import Optional, List
from pydantic import BaseModel

# pip install sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy import Boolean, Column, Float, String, Integer


# Se puede ver la documentación en http://127.0.0.1:8000/docs de FastAPI de manera sencilla
app = FastAPI()

# Funcion GET, devuelve el texto "Hello World"
# http://127.0.0.1:8000/api/v1/hello (el dato es devuelto en formato JSON)
@app.get("/api/v1/hello")
async def principal():
    return {"Hello": "World"}

# Funcion GET para leer un item_id (numero entero) y un string Q pasado como parametro, devuelve el item_id numerico y el string q
# http://127.0.0.1:8000/items/{item_id}?q=foo (el dato es devuelto en formato JSON)
@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

# Funcion GET para leer un item_id que se lo pasa como parametro, devuelve el item_id la función
# http://127.0.0.1:8000/api/v1/items/{item_id} // item_id = 10 o item_id = foo
@app.get("/api/v1/items/{item_id}")
async def read_item(item_id):
    return {"item_id": item_id}

# Variable GLOBAL usada para almacenar el texto
text_message = "Initial Text Message"

# Funcion POST para agregar (ADD) un String dentro de la variable text_message existente
# http://127.0.0.1:8000/api/v1/change?text=_2do%20String_%203er%20String (POST
@app.post("/api/v1/add")
async def add_text(text: str):
    global text_message
    old_text = text_message
    text_message += text
    return {"message": "Text Added", "current_message": text_message, "old_text": old_text}


# Funcion PUT para CAMBIAR un String dentro de la variable text_message existente
# http://127.0.0.1:8000/api/v1/put?newtext=_2do%20String_%203er%20String (PUT)
@app.put("/api/v1/put")
async def change_text(newtext: str):
    global text_message
    old_text = text_message
    text_message = newtext
    return {"message": "Text Changed", "current_message": text_message, "old_text": old_text}


# Funcion DELETE para borrar text_message
# http://127.0.0.1:8000/api/v1/delete (PUT)
@app.put("/api/v1/delete")
async def delete_text():
    global text_message
    old_text = text_message
    text_message = ""
    return {"message": "Text Removed", "current_message": text_message, "old_text": old_text}


global Item

# A Pydantic Item object
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

# Función POST para agregar un Item a una lista existente, devuelve el item.dict()
# http://127.0.0.1:8000/api/v2/items/
# Body Raw JSON Example: { "name": "Sony TV 32 P32TV54R2",   "description": "TV 32 Pulgadas Sony modelo P32TV54R2 - Full HD - 3 HDMI Ports",   "price": 345000,   "tax": 10.3 }
@app.post("/api/v2/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price * (1+ (item.tax/100))
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

# Función POST para agregar un Item a una lista existente, devuelve el item_id y el item.dict()
# http://127.0.0.1:8000/api/v3/items/10
# Body Raw JSON Example: { "name": "Sony TV 32 P32TV54R2",   "description": "TV 32 Pulgadas Sony modelo P32TV54R2 - Full HD - 3 HDMI Ports",   "price": 345000,   "tax": 10.3 }
@app.post("/api/v3/items/{item_id}")
async def create_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.dict()}

# A Pydantic Place object
class Place(BaseModel):
    name: str
    description: Optional[str] = None
    coffee: bool
    wifi: bool
    food: bool
    lat: float
    lng: float

    class Config:
        orm_mode = True

# Función POST para agregar un Place a una lista existente, devuelve la clase place
# http://127.0.0.1:8000/api/v1/places-basic-example/
# Body Raw JSON Example: { "name": "Café de la Piscine",   "description": "Café de la Piscine",   "coffee": true,   "wifi": true,   "food": true,   "lat": 48.8566,   "lng": 2.3522 }
@app.post('/api/v1/places-basic-example/')
async def create_place_view(place: Place):
    return place


#SqlAlchemy Setup
import os
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URL = 'sqlite+pysqlite:///' + os.path.join(basedir, 'db.sqlite3')
#SQLALCHEMY_DATABASE_URL = 'sqlite+pysqlite:///./db.sqlite3:'
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class DBPlace(Base):
    __tablename__ = 'places' #specifies the name of the table.

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    description = Column(String, nullable=True)
    coffee = Column(Boolean)
    wifi = Column(Boolean)
    food = Column(Boolean)
    lat = Column(Float)
    lng = Column(Float)

Base.metadata.create_all(bind=engine) #Creates all tables in the database that are defined by the SQLAlchemy models (eg.DBPlace) and are not already present in the database.

# Methods for interacting with the database
def get_place(db: Session, place_id: int):
    return db.query(DBPlace).where(DBPlace.id == place_id).first()

def get_place_name(db: Session, name: str):
    return db.query(DBPlace).where(DBPlace.name == name).first()

def get_places(db: Session):
    return db.query(DBPlace).all()

def create_place(db: Session, place: Place):
    db_place = DBPlace(**place.dict())
    db.add(db_place)
    db.commit()
    db.refresh(db_place)

    return db_place

# Routes for interacting with the API
# Create/Add new place, insert into the database this place 
''' Body:  {
    "name": "PAE04",
    "description": "Cocina Piso 4to",
    "coffee": true,
    "wifi": true,
    "food": true,
    "lat": 1120.07,
    "lng": 2359.1
}'''
# URL http://127.0.0.1:8000/places/  (Metodo: POST)
@app.post('/places/', response_model=Place)
def create_places_view(place: Place, db: Session = Depends(get_db)):
    db_place = create_place(db, place)
    return db_place
# Get All places, return all the places in the database
# URL http://127.0.0.1:8000/places/  (Metodo: GET) (Body: None)
@app.get('/places/', response_model=List[Place])
def get_places_view(db: Session = Depends(get_db)):
    return get_places(db)

# Get one place by ID, return one place in the database
# URL http://127.0.0.1:8000/places/1  (Metodo: GET) (Body: None)
@app.get('/place/{place_id}')
def get_place_view(place_id: int, db: Session = Depends(get_db)):
    return get_place(db, place_id)

#Get one place by NAME, return one place in the database
# URL http://127.0.0.1:8000/api/v1/place/PAE04  (Metodo: GET) (Body: None)
@app.get('/api/v1/place/{name}')
def get_place_view(name: str, db: Session = Depends(get_db)):
    return get_place_name(db, name)
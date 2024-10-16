# uvicorn main:app

from typing import Union 
from fastapi import FastAPI, Depends #pip install fastapi, uvicorn
from typing import Optional, List
from pydantic import BaseModel

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

# Función POST para agregar un Place a una lista existente, devuelve el place
# http://127.0.0.1:8000/api/v1/places-basic-example/
# Body Raw JSON Example: { "name": "Café de la Piscine",   "description": "Café de la Piscine",   "coffee": true,   "wifi": true,   "food": true,   "lat": 48.8566,   "lng": 2.3522 }
@app.post('/api/v1/places-basic-example/')
async def create_place_view(place: Place):
    return place
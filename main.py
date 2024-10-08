# uvicorn main:app

from typing import Union 
from fastapi import FastAPI #pip install fastapi, uvicorn

app = FastAPI()



@app.get("/api/v1/hello")
async def principal():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}


text_message = "Initial Text Message"

# Funcion POST para agregar un String dentro de la variable text_message existente
@app.post("/api/v1/add")
async def add_text(text: str):
    text_message += text
    return {"message": "Text Added", "current_message": text_message}

# Funcion PUT para cambiar un String dentro de la variable text_message existente
@app.put("/api/v1/put")
async def change_text(newtext: str):
    text_message += newtext
    return {"message": "Text Changed", "current_message": text_message}


# Funcion DELETE para borrar text_message
@app.put("/api/v1/put")
async def delete_text():
    text_message = ""
    return {"message": "Text Removed", "current_message": text_message}
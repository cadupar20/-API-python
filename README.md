# API-python

### Requisitos: 

pip install -r requirements.txt
(fastapi uvicorn etc)

# Cear el virtual environment:
❯ virtualenv venv

# Activar el virtual environment:
❯ .\venv\Scripts\activate

# Run the First API App With Uvicorn
### Iniciar el servidor: uvicorn main:app --reload

### Documentación de la API: 
Consulte la documentación de la API interactiva
Ahora abra http://127.0.0.1:8000/docs en su navegador.

Verá la documentación API interactiva automática proporcionada por Swagger UI:
![Swagger UI](https://files.realpython.com/media/fastapi-first-steps-01-swagger-ui-simple.c46a4a9242dd.png)

### Pruebe la documentación de la API:

Tambien puede probar la URL de documentación alternativa de la API. Dirígete a http://127.0.0.1:8000/redoc.
Aquí verás la documentación automática alternativa (proveída por ReDoc):
![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)


Dentro de la documentación de este main.py, se puede probar los siguientes endpoints: 


| URL    | Metodo |  Body  |
| ------ | ------ | ------ |
| http://127.0.0.1:8000/api/v1/hello | GET | NO |
| http://127.0.0.1:8000/api/v1/items/10 | GET | NO |
| http://127.0.0.1:8000/api/v1/items/foo | GET | NO |
| http://127.0.0.1:8000/api/v1/add | PUT | NO |
| http://127.0.0.1:8000/api/v1/put?newtext=_2do%20String_%203er%20String | PUT | NO |
| http://127.0.0.1:8000/api/v1/change?text=_2do%20String_%203er%20String | POST | NO |
| http://127.0.0.1:8000/api/v1/delete | PUT | NO |
| http://127.0.0.1:8000/api/v2/items/ | POST | SI |
| http://127.0.0.1:8000/api/v3/items/10 | POST | SI |
| http://127.0.0.1:8000/api/v1/places-basic-example/ | POST | SI |
| http://127.0.0.1:8000/places/ | POST | SI |
| [http://127.0.0.1:8000/places/](http://127.0.0.1:8000/places/)| GET | NO |
| http://127.0.0.1:8000/places/1 | GET | NO |
| http://127.0.0.1:8000/api/v1/place/PAE04 | GET | NO |

con los metodos GET, POST, PUT y DELETE que se han desarrollado como ejemplo dentro del este archivo main.py (ejemplo: Este endopoint utiliza el metodo PUT --> @app.put("/api/v1/delete"))

Es importante para algunos de las URLs que se han creado, ademas de los parametros es necesario que el request tengo un Body tipo JSON como el siguiente ejemplo:

### Esto se puede validar utilizando POSTMAN tambien, en caso de no usar /docs o /Redoc, se puede probar con las herramientas API Rest:
http://127.0.0.1:8000/api/v2/items/

Body Raw JSON Example:

{
  "name": "Sony TV 54 P32TV74R2",
  "description": "TV 354 Pulgadas Sony modelo P32TV74R2 - Full HD - 3 HDMI Ports",
  "price": 675000,
  "tax": 10.3
}

![Postman image1](https://i.imgur.com/HRFD7o6.jpeg)

### Esto se puede validar utilizando POSTMAN tambien, en caso de no usar /docs o /Redoc, se puede probar con las herramientas API Rest:
http://127.0.0.1:8000/api/v3/items/10

Body Raw JSON Example:

{
  "name": "Sony TV 32 P32TV54R2",
  "description": "TV 32 Pulgadas Sony modelo P32TV54R2 - Full HD - 3 HDMI Ports",
  "price": 345000,
  "tax": 10.3
}

![Postman image2](https://i.imgur.com/QRvfxlO.jpeg)

### Otro ejemplo para valdar con Postman: (POST)
http://127.0.0.1:8000/api/v1/places-basic-example/

Body Raw JSON Example:

{ "name": "Café de la Piscine",   
  "description": "Café de la Piscine",   
  "coffee": true,   
  "wifi": true,   
  "food": true,   
  "lat": 48.8566,   
  "lng": 2.3522 
}

## Update - Se agregan 4 endpoints para el uso de SQLAlchemy (db.sqlite3) como almacenamiento local estatico de datos.
|http://127.0.0.1:8000/places/ | POST

|http://127.0.0.1:8000/places/ | GET

|http://127.0.0.1:8000/places/1 | GET

|http://127.0.0.1:8000/api/v1/place/PAE04 | GET

### Otro ejemplo mas usando SQLAlchemy, ingresando datos desde Postman: (POST)
http://127.0.0.1:8000/places/

Body Raw JSON Example:

{
  "name": "PAE04",
  "description": "Cocina Piso 4to",
  "coffee": true,
  "wifi": true,
  "food": true,
  "lat": 1120.07,
  "lng": 2359.1
}

Ingresa los datos a una Base de datos local con SQLAlchemy (db.sqlite3)


### REFERENCE: 
1) Documentación del uso de FastAPI -> https://realpython.com/fastapi-python-web-apis/
2) Sitio para publicar imagenes -> https://imgur.com
3) FastAPI Documentation -> https://fastapi.tiangolo.com/es/tutorial/first-steps/#paso-4-define-la-funcion-de-la-operacion-de-path

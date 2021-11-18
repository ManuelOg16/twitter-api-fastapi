#Python
import json  #libreria que me sirve para trabajar con archivos .json
from uuid import UUID
from datetime import date, datetime
from typing import Optional, List  # de la liberaria de Typing puedo importar la clase List esta me permite definir el tipo de una variable va aser una lista de cosas

#Pydantic
from pydantic import BaseModel
from pydantic import EmailStr #For validate a data is a email
from pydantic import Field


#FastAPI
from fastapi import FastAPI
from fastapi import status
from fastapi import Body

app = FastAPI()

#Models

class UserBase(BaseModel): # have the information basic the user the return in Response with users with our API 
    user_id: UUID = Field(...)  #UUID =Universally Unique IDentifier es una clase especial de python que nos permite colocar un identificador unico cada vez a cada uno de lso usuarios  y entidades que nosotros creamos en nuestra aplicación
    email: EmailStr = Field(...)

# class PasswordMixin(BaseModel):   # Creamos este nuevo modelo para no repetir codigo del password
    # password: str = Field(
    # ...,
    #     min_length=8,
    #     max_length=64,
    #     example='password'
    # )

class UserLogin(UserBase): #The model return when the user  Logged in our API
    password: str = Field(
    ...,
        min_length=8,
        max_length=64
    )

class User(UserBase): # others tasks with users we used a User, but not the password
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    birth_date: Optional[date] = Field(default=None)

class UserRegister(UserLogin,User): #Nuevo modelo para el registro del usuario en la aplicación
    # password: str = Field(
    # ...,
    #     min_length=8,
    #     max_length=64
    # )  
    pass

class Tweet(BaseModel):
    tweet_id: UUID = Field(...)
    content: str = Field(
        ...,
        min_length=1,
        max_length= 256
    )
    created_at: datetime = Field(default=datetime.now()) #la fecha de creación del tweet con hora
    update_at: Optional[datetime] = Field(default=None)  #el momento en el que se actualiza el tweet si es que lo actualizamos, en la realidad tweeter no deja actualizar pero nosotros si lo vamos a hacer
    by: User = Field(...)            #by va indicar el usuario que creo el tweet, este atributo es de tipo user aprovechamos la herencia de la programacion orientada a objetos


# Recordar el grafico de guia con las path operations
# Path Operations

## Users   

### Register a user
@app.post(
    path= "/signup",
    response_model= User,  # cada vez que s eregistre un usuario vamos a responder con su información base 
    status_code= status.HTTP_201_CREATED,
    summary= "Register a User",
    tags=["Users"] # la path operation va estar dentro de la pestaña Users
)
def signup(user: UserRegister = Body(...)):
    """
    Signup

    This path operation register a user in the app

    Parameters: 
        - Request body parameter
            - user: UserRegister

    Returns a json with the basic user information:
        - user_id: UUID
        - email: Emailstr
        - first_name: str
        - last_name: str
        - birth_date: date
    """
    with open("users.json", "r+", encoding= "utf-8") as f:  #r+ para leer y escribir
        results = json.loads(f.read()) #como lo hizo el profe la funcion loads del modulo json carga un string y lo transforma en un simil a json en este caso en un diccioario por lo tanto results va tener un diccionario en este caso va ser una lista de diccionarios lo que va contener results
        
        #Ahora vamos a convertir el body que nos viene a nosotros en un diccionario tambien, recordemos que la funcion signup necesita un Request body , necesita un user que venga desde el cliente para poder registrar el usuario , la comunicacion es el cliente le envia la info de registro al servidor el servidor la toma la guarda  retorna que el usuario se creo correctamente para lograr eso colocamos en los parametros de la funcion signup ese request body
        user_dict= user.dict() #cadaa uno de los request body que nos viene como parametro tiene tambien el metodo dict este es un metodo interno que le asigna fastAPI al Request body para poder transformar el json en diccionario de manera explicita
        user_dict["user_id"] = str(user_dict["user_id"])   #cambiar dos parametros que tengo dentro de este diccionario
        user_dict["birth_date"] = str(user_dict["birth_date"]) #los datos UUID , date no se pueden convertir a json de manera natural, lo tengo que hacer manualmente  con un casting str()            
        results.append(user_dict) #hago un append dentro d emi variable results de ese diccionario le añado el nuevo usuario a mi json con el user_dict
        f.seek(0)        #voy a mover al principio de mi archivo por que acabo de escribir algo, entonces para no tener error y moverme lo hago con seek en el primer byte (0) para no emepzar a escribir listas, entonces con seek me muevo al byte cero es decir al incio del archivo y a partir de ahi escribo lo que debo escibir
        f.write(json.dumps(results))  #ahora voy a escribir en el archivo, lo debo convertir la lista de diccionarios en un json con dumps
        return user  #del user que me viene como parametro para decirle al usuario que se creo correctamente

### Login a user
@app.post(
    path= "/login",
    response_model= User,  # cada vez que s eregistre un usuario vamos a responder con su información base 
    status_code= status.HTTP_200_OK,
    summary= "Login a User",
    tags=["Users"] # la path operation va estar dentro de la pestaña Users
)
def login():
    pass

### Show all users
@app.get(
    path= "/users",
    response_model= List[User],  #me va responder json que va tener un formato de lista  de lista de usuarios 
    status_code= status.HTTP_200_OK,
    summary= "Show all users",
    tags=["Users"] 
)
def show_all_users():
    pass

### Show a User
@app.get(
    path= "/users/{user_id}",
    response_model= User,  
    status_code= status.HTTP_200_OK,
    summary= "Show a User",
    tags=["Users"] 
)
def show_a_user():
    pass

### Delete a User
@app.delete(
    path= "/users/{user_id}/delete",
    response_model= User,  
    status_code= status.HTTP_200_OK,
    summary= "Delete a User",
    tags=["Users"] 
)
def delete_a_user():
    pass

### Update a User
@app.put(
    path= "/users/{user_id}/update",
    response_model= User,  
    status_code= status.HTTP_200_OK,
    summary= "Update a User",
    tags=["Users"] 
)
def update_a_user():
    pass



## Tweets

### Show all tweets
@app.get(   #este home nos trae a todos los tweets aprovechamos la clase List que nos viene desde Python
    path="/",
    response_model= List[Tweet], 
    status_code= status.HTTP_200_OK,
    summary= "Show all tweets",
    tags=["Tweets"] 
)   
def home():
    return{"Twitter API": "Working!"}

### Post a Tweet
@app.post(
    path= "/post",
    response_model= Tweet, 
    status_code= status.HTTP_201_CREATED,
    summary= "Post a tweet ",
    tags=["Tweets"] 
)
def post():
    pass

### Show a Tweet
@app.get(      #estamos obteniendo informacion desde el cliente al servidor
    path= "/tweets/{tweet_id}",
    response_model= Tweet, 
    status_code= status.HTTP_200_OK,
    summary= "Show  a tweet ",
    tags=["Tweets"] 
)
def show_a_tweet():
    pass

### Delete a Tweet
@app.delete(      
    path= "/tweets/{tweet_id}/delete",
    response_model= Tweet, 
    status_code= status.HTTP_200_OK,
    summary= "Delete a tweet ",
    tags=["Tweets"] 
)
def delete_a_tweet():
    pass

### Update a Tweet
@app.put(      
    path= "/tweets/{tweet_id}/update",
    response_model= Tweet, 
    status_code= status.HTTP_200_OK,
    summary= "Update a tweet ",
    tags=["Tweets"] 
)
def update_a_tweet():
    pass
#Python
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


app = FastAPI()

#Models

class UserBase(BaseModel): # have the information basic the user the return in Response with users with our API 
    user_id: UUID = Field(...)  #UUID =Universally Unique IDentifier es una clase especial de python que nos permite colocar un identificador unico cada vez a cada uno de lso usuarios  y entidades que nosotros creamos en nuestra aplicación
    email: EmailStr = Field(...)

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

# Path Operations

@app.get(
    path="/")
def home():
    return{"Twitter API": "Working!"}

# Recordar el grafico de guia con las path operations
## Users   

@app.post(
    path= "/signup",
    response_model= User,  # cada vez que s eregistre un usuario vamos a responder con su información base 
    status_code= status.HTTP_201_CREATED,
    summary= "Register a User",
    tags=["Users"] # la path operation va estar dentro de la pestaña Users
)
def signup():
    pass

@app.post(
    path= "/login",
    response_model= User,  # cada vez que s eregistre un usuario vamos a responder con su información base 
    status_code= status.HTTP_200_OK,
    summary= "Login a User",
    tags=["Users"] # la path operation va estar dentro de la pestaña Users
)
def login():
    pass

@app.get(
    path= "/users",
    response_model= List[User],  #me va responder json que va tener un formato de lista  de lista de usuarios 
    status_code= status.HTTP_200_OK,
    summary= "Show all users",
    tags=["Users"] 
)
def show_all_users():
    pass

@app.get(
    path= "/users/{user_id}",
    response_model= User,  
    status_code= status.HTTP_200_OK,
    summary= "Show a User",
    tags=["Users"] 
)
def show_a_user():
    pass

@app.delete(
    path= "/users/{user_id}/delete",
    response_model= User,  
    status_code= status.HTTP_200_OK,
    summary= "Delete a User",
    tags=["Users"] 
)
def delete_a_user():
    pass

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
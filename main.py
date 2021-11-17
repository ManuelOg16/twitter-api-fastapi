#Python
from uuid import UUID
from datetime import date, datetime
from typing import Optional

#Pydantic
from pydantic import BaseModel
from pydantic import EmailStr #For validate a data is a email
from pydantic import Field


#FastAPI
from fastapi import FastAPI



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

@app.get(
    path="/")
def home():
    return{"Twitter API": "Working!"}
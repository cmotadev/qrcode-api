from pydantic import BaseModel, HttpUrl, EmailStr
    

class URLInput(BaseModel):
    url: HttpUrl

class EmailInput(BaseModel):
    email: EmailStr

class TextInput(BaseModel):
    text: str

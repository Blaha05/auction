from pydantic import BaseModel, EmailStr

class AddUserShema(BaseModel):
    email:EmailStr
    name:str
    password:str

class UpdateUserShema(BaseModel):
    email:EmailStr | None = None
    name:str | None = None
    password:str | None = None


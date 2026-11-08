from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str
    
    
class UserLogin(BaseModel):
    username: str
    password: str
    
class UserResponse(BaseModel):
    access_token: str
    user_id: int
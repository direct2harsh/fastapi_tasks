from pydantic import BaseModel
from typing import Optional

class AuthenticatedUser(BaseModel):
    id: str
    username: str
    email: Optional[str] = None
    roles: list = []


class LoginModel(BaseModel):
    username:str
    password:str
    client_id:str
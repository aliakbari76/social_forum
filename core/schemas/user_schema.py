from typing import Optional
from pydantic import BaseModel

class UserSchema(BaseModel):
    username : str
    first_name :  Optional[str]
    last_name : Optional[str]
    password : str
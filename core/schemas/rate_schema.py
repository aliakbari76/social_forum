from pydantic import BaseModel

class RateSchema(BaseModel):
    rate: int
    user_id: int
    post_id: int
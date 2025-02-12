from datetime import datetime
from pydantic import BaseModel


class ProfileResponse(BaseModel):
    email: str
    username: str
    registered_at: datetime

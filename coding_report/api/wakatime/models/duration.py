from pydantic import BaseModel


class Duration(BaseModel):
    created_at: str
    duration: float
    id: str
    project: str
    time: float

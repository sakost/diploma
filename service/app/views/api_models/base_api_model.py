from pydantic import BaseModel


class StandartResponse(BaseModel):
    message: str
    status_code: int

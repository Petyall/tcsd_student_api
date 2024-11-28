from pydantic import BaseModel


class LogsRequest(BaseModel):
    token: str
    date: str

from pydantic import BaseModel


class SyncRequest(BaseModel):
    lms_id: str
    cookie_str: str


class SyncResponse(BaseModel):
    status: str
    user_id: int
    courses: int

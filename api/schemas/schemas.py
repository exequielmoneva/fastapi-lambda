from pydantic import BaseModel


class Job(BaseModel):
    company: str
    position_title: str
    process_status: str
    date_applied: str

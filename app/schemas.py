from sqlmodel import SQLModel, Field
from typing import Optional
import datetime


class BirthdayBase(SQLModel):
    name: str
    date: datetime.date
    relation: str
    custom_message: Optional[str] = None
    notify_7_days: bool = False
    notify_30_days: bool = False


class BirthdayCreate(BirthdayBase):
    pass


class BirthdayUpdate(SQLModel):
    name: Optional[str] = None
    date: Optional[datetime.date] = None


class BirthdayRead(BirthdayBase):
    id: int | None = Field(default=None, primary_key=True)

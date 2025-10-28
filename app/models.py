from sqlmodel import SQLModel, Field
import datetime
from typing import Optional


class Birthday(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    date: datetime.date
    custom_message: str | None = Field(default=None)
    relation: Optional[str] = Field(default=None, description="Relation to the person (e.g., friend, family)")
    notify_7_days: bool = Field(default=True, description="Send notification 7 days before birthday")
    notify_30_days: bool = Field(default=True, description="Send notification 30 days before birthday")

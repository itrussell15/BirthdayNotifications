from . import db, models, schemas
from sqlmodel import select


def create_birthday(payload: schemas.BirthdayCreate) -> models.Birthday:
    with db.get_session() as s:
        b = models.Birthday.from_orm(payload)
        s.add(b)
        s.commit()
        s.refresh(b)
        return b


def get_birthdays() -> list[models.Birthday]:
    with db.get_session() as s:
        return s.exec(select(models.Birthday)).all()


def get_birthday(b_id: int) -> models.Birthday | None:
    with db.get_session() as s:
        return s.get(models.Birthday, b_id)


def update_birthday(b_id: int, payload: schemas.BirthdayUpdate) -> models.Birthday | None:
    with db.get_session() as s:
        b = s.get(models.Birthday, b_id)
        if not b:
            return None
        if payload.name is not None:
            b.name = payload.name
        if payload.date is not None:
            b.date = payload.date
        s.add(b)
        s.commit()
        s.refresh(b)
        return b


def delete_birthday(b_id: int) -> bool:
    with db.get_session() as s:
        b = s.get(models.Birthday, b_id)
        if not b:
            return False
        s.delete(b)
        s.commit()
        return True

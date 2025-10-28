import os
from fastapi import FastAPI, APIRouter, Depends, HTTPException, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from sqlmodel import Session, select
from . import db, crud, schemas, scheduler
import datetime

app = FastAPI(title="Birthday Notifier")

# Setup templates
templates = Jinja2Templates(directory="app/templates")


@app.on_event("startup")
def on_startup():
    db.init_db()
    scheduler.start()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/birthdays", response_model=schemas.BirthdayRead)
def create_birthday(payload: schemas.BirthdayCreate):
    return crud.create_birthday(payload)


@app.get("/birthdays", response_model=list[schemas.BirthdayRead])
def list_birthdays():
    return crud.get_birthdays()


@app.get("/birthdays/{b_id}", response_model=schemas.BirthdayRead)
def get_birthday(b_id: int):
    b = crud.get_birthday(b_id)
    if not b:
        raise HTTPException(status_code=404, detail="Not found")
    return b


@app.put("/birthdays/{b_id}", response_model=schemas.BirthdayRead)
def update_birthday(b_id: int, payload: schemas.BirthdayUpdate):
    b = crud.update_birthday(b_id, payload)
    if not b:
        raise HTTPException(status_code=404, detail="Not found")
    return b


@app.delete("/birthdays/{b_id}")
def delete_birthday(b_id: int):
    ok = crud.delete_birthday(b_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Not found")
    return {"deleted": True}



@app.post("/notify")
def trigger_notify():
    """Trigger the birthday check immediately (for testing)."""
    ok = scheduler.check_and_notify()
    return {"notified": ok}

# Web Interface Routes
@app.get("/")
def home(request: Request):
    birthdays = crud.get_birthdays()
    return templates.TemplateResponse("index.html", {"request": request, "birthdays": birthdays})

@app.get("/add")
def add_birthday_form(request: Request):
    return templates.TemplateResponse("add_birthday.html", {"request": request})

@app.post("/add")
async def add_birthday_submit(
    request: Request,
    name: str = Form(...),
    date: str = Form(...),
    relation: str = Form(...),
    custom_message: str = Form(None),
    notify_7_days: str = Form("false"),
    notify_30_days: str = Form("false")
):
    # Convert string date to datetime.date
    birth_date = datetime.date.fromisoformat(date)
    
    # Create birthday
    # Coerce checkbox values to booleans (form sends strings)
    notify_7 = True if str(notify_7_days).lower() in ("1", "true", "yes", "on") else False
    notify_30 = True if str(notify_30_days).lower() in ("1", "true", "yes", "on") else False

    birthday = schemas.BirthdayCreate(
        name=name,
        relation=relation,
        date=birth_date,
        custom_message=custom_message,
        notify_7_days=notify_7,
        notify_30_days=notify_30
    )
    crud.create_birthday(birthday)
    
    return RedirectResponse(url="/", status_code=303)

@app.post("/delete/{b_id}")
async def delete_birthday_web(b_id: int):
    crud.delete_birthday(b_id)
    return RedirectResponse(url="/", status_code=303)

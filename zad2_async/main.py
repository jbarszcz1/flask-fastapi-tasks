from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pydantic import ValidationError
from typing import Optional
from urllib.parse import quote

import models
import schemas
from database import engine, get_db
from tasks import insert_user_task

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(
    request: Request,
    db: Session = Depends(get_db),
    success: Optional[str] = None,
    error: Optional[str] = None
):
    users = db.query(models.User).all()
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "users": users,
            "success": success,
            "error": error
        }
    )


@app.post("/submit")
async def handle_form(
    request: Request,
    name: str = Form(...),
    surname: str = Form(...)
):
    try:
        user_data = schemas.UserCreate(name=name, surname=surname)
        insert_user_task.delay(user_data.name, user_data.surname)
        return RedirectResponse(url="/?success=Task submitted to background queue", status_code=303)
    except ValidationError as e:
        error_msgs = [err['msg'] for err in e.errors()]
        combined_error = " and ".join(error_msgs)
        return RedirectResponse(url=f"/?error={quote(combined_error)}", status_code=303)

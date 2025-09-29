from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas
from .database import get_db, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/templates"), name="static")

templates = Jinja2Templates(directory="app/templates")

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/register", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Пользователь уже существует")
    db_user = models.User(username=user.username, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/login")
def login(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if not db_user or db_user.password != user.password:
        raise HTTPException(status_code=401, detail="Неверное имя пользователя или пароль")
    return {"message": "Авторизация успешна"}

@app.post("/quiz-card-types/", response_model=schemas.QuizCardType)
def create_quiz_card_type(quiz_card_type: schemas.QuizCardTypeCreate, db: Session = Depends(get_db)):
    db_quiz_card_type = models.QuizCardType(**quiz_card_type.dict())
    db.add(db_quiz_card_type)
    db.commit()
    db.refresh(db_quiz_card_type)
    return db_quiz_card_type

@app.post("/submit-quiz", response_model=schemas.QuizResult)
def submit_quiz(result: schemas.QuizResultCreate, db: Session = Depends(get_db)):
    db_result = models.QuizResult(**result.dict())
    db.add(db_result)
    db.commit()
    db.refresh(db_result)
    return db_result

@app.get("/results", response_model=List[schemas.QuizResult])
def get_results(db: Session = Depends(get_db)):
    return db.query(models.QuizResult).all()

@app.get('/about')
async def read_about(db: Session = Depends(get_db)):
    return {
        'version': '1.0',
        'quiz_card_type_count': db.query(models.QuizCardType).count(),
    }

@app.get('/health')
async def read_health():
    return {'status': 200}

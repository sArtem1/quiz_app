from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from .database import get_db, engine

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

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
    db_quiz_card_type = models.QuizCardType(**quiz_card_type.model_dump())
    db.add(db_quiz_card_type)
    db.commit()
    db.refresh(db_quiz_card_type)
    return db_quiz_card_type

@app.post("/submit-quiz", response_model=schemas.QuizResult)
def submit_quiz(result: schemas.QuizResultCreate, db: Session = Depends(get_db)):
    db_result = models.QuizResult(**result.model_dump())
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


@app.get('/quiz_types/count')
async def read_quiz_type_count(session: AsyncSession = Depends(get_db)):
    result = await session.execute(select(models.QuizCardType))
    return {'count': len(result.scalars().all())}

@app.get('/quiz_types/')
async def get_all_quiz_types(session: AsyncSession = Depends(get_db)):
    result = await session.execute(select(models.QuizCardType))
    return result.scalars().all()

@app.get('/quiz_types/{type_id: int}')
async def read_quiz_types(type_id: int, session: AsyncSession = Depends(get_db)):
    result = await session.execute(select(models.QuizCardType).where(models.QuizCardType.id == type_id))
    return result.scalar_one_or_none() #возвращает либо 1 объект(если он есть), либо None


@app.get('/quiz_cards/{card_id}')
async def read_quiz_cards(card_id: int, session: AsyncSession = Depends(get_db)):
    result = await session.execute(select(models.QuizCard).where(models.QuizCard.id == card_id))
    return result.scalar_one_or_none()

@app.get('/quiz_cards/')
async def get_all_quiz_cards(session: AsyncSession = Depends(get_db)):
    result = await session.execute(select(models.QuizCard))
    return result.scalars().all()

@app.get('/quiz_cards/count')
async def get_quiz_card_count(session: AsyncSession = Depends(get_db)):
    result = await session.execute(select(models.QuizCard))
    return {'count': len(result.scalars().all())}

@app.get('/questions/count')
async def get_questions_count(session: AsyncSession = Depends(get_db)):
    result = await session.execute(select(models.Question))
    return {'count': len(result.scalars().all())}

@app.get('/questions/')
async def get_all_questions(session: AsyncSession = Depends(get_db)):
    result = await session.execute(select(models.Question))
    return {'questions:': result.scalars().all()}


@app.get('/questions/{question_id}')
async def get_question(question_id: int, session: AsyncSession = Depends(get_db)):
    result = await session.execute(select(models.Question).where(models.Question.id == question_id))
    return {'question': result.scalar_one_or_none()}





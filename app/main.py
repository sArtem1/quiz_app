from fastapi import FastAPI
from fastapi.params import Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import QuizCard, QuizCardType, Question
from app.models import Base
from app.database import engine

Base.metadata.create_all(bind=engine)
app = FastAPI()


@app.get("/")
async def read_root():
    return 'привет'


@app.get('/about')
async def read_about(db:Session=Depends(get_db)) -> dict[str, str|int]:
    return {
        'version': '1.0',
        # 'quiz_card_count': db.query(QuizCard).count(),
        'quiz_card_type_count': db.query(QuizCardType).count(),
        # 'question_count': db.query(Question).count(),
    }

@app.get('/health')
async def read_health() -> dict[str, int]:
    return {'status': 200}
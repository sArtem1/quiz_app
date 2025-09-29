from pydantic import BaseModel
from typing import Optional, List


class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        from_attributes = True


class QuizCardTypeBase(BaseModel):
    name: str
    points: int
    try_count: int
    tries_for_hint_count: Optional[int] = None

class QuizCardTypeCreate(QuizCardTypeBase):
    pass

class QuizCardType(QuizCardTypeBase):
    id: int

    class Config:
        from_attributes = True


class QuizCardBase(BaseModel):
    question_text: str
    image: Optional[str] = "default.jpg"
    quiz_type: int
    hint_text: Optional[str] = None

class QuizCardCreate(QuizCardBase):
    pass

class QuizCard(QuizCardBase):
    id: int
    questions: List["Question"] = []

    class Config:
        from_attributes = True

class QuestionBase(BaseModel):
    question_text: str
    quiz_card_id: int

class QuestionCreate(QuestionBase):
    pass

class Question(QuestionBase):
    id: int

    class Config:
        from_attributes = True

class QuizResultBase(BaseModel):
    user_id: int
    score: int
    total: int

class QuizResultCreate(QuizResultBase):
    pass

class QuizResult(QuizResultBase):
    id: int

    class Config:
        from_attributes = True

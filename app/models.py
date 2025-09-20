from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class QuizCardType(Base):
    __tablename__ = 'QuizCardType'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    points = Column(Integer)
    try_count = Column(Integer, nullable=False)
    tries_for_hint_count = Column(Integer, nullable=True)
    quiz_cards = relationship("QuizCard", back_populates="quiz_type_info")

class QuizCard(Base):
    __tablename__ = 'QuizCard'

    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(String, nullable=False)
    image = Column(String, default='default.jpg', nullable=True)
    quiz_type = Column(ForeignKey('QuizCardType.id'), nullable=False)
    hint_text = Column(String, nullable=True)
    questions = relationship("Question", back_populates="quiz_card", cascade="all, delete-orphan")
    quiz_type_info = relationship("QuizCardType", back_populates="quiz_cards")


class Question(Base):
    __tablename__ = 'Question'

    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(String, nullable=False)
    quiz_card_id = Column(Integer, ForeignKey('QuizCard.id'), nullable=False)
    quiz_card = relationship("QuizCard", back_populates="questions")
# models.py
from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Question(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    question_text = Column(Text, nullable=False)
    answer_text = Column(Text, nullable=True)
    video_text = Column(Text, nullable=True)

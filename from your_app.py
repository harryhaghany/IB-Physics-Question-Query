from models import Question
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine("sqlite:///ib_questions_new1.db")
Session = sessionmaker(bind=engine)
session = Session()

# Fetch a question with video
question_with_video = session.query(Question).filter(Question.video_text != None).first()
print(question_with_video.video_text)

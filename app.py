from flask import Flask, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Question
from google import genai
from dotenv import load_dotenv
import os
from markdown import markdown

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)
# Configure Gemini client

app = Flask(__name__)

# Database setup
engine = create_engine('sqlite:///ib_questions_new1.db')
Session = sessionmaker(bind=engine)

def generate_explanation(question_text, answer_text):
    """Generate a well-formatted explanation using Gemini API"""
    prompt = f"""
    Explain why '{answer_text}' is the correct answer to the following physics question:
    {question_text}

    Requirements:
    - Use clear paragraph breaks
    - Format steps as numbered lists
    - Put formulas on separate lines
    - Keep under 200 words
    - Use Markdown formatting for:
      * Bullet points (*)
      * Bold for key terms (**key term**)
      * Italics for variables (_V_)
      * Code blocks for formulas (`F=ma`)

    Example format:
    The correct answer is **D** because of three main factors:

    1. **First principle**: 
    - Start with _F=ma_
    - Then consider _v=u+at_

    2. **Second principle**:
    `E=mc²` shows that...

    3. **Conclusion**:
    Therefore, option D is correct because...
    """
    
    try:
        response = client.models.generate_content(
  model="gemini-2.0-flash",
  contents=[prompt])
        return response.text
    except Exception as e:
        print(f"Error generating explanation: {e}")
        return "Explanation not available at this time."

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_term = request.form.get('search')
        if not search_term:
            return render_template('index.html', error="Please enter a search term")
        
        session = Session()
        results = session.query(Question).filter(
            Question.question_text.ilike(f"%{search_term}%")
        ).limit(5).all()  # Limit to 5 results to avoid API rate limits
        
        processed_results = []
        for result in results:
            explanation = generate_explanation(result.question_text, result.answer_text)
            processed_results.append({
                'question_text': result.question_text,
                'answer_text': result.answer_text,
                'video_text': result.video_text,
                'explanation': explanation
            })
        
        session.close()
        return render_template('results.html', 
                            results=processed_results, 
                            search_term=search_term)
    
    return render_template('index.html')

@app.template_filter('md')
def markdown_filter(text):
    return markdown(text, extensions=['fenced_code', 'tables'])

if __name__ == '__main__':
    app.run(debug=True)
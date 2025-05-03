from flask import Flask, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Question
from google import genai
from dotenv import load_dotenv
import os
from markdown import markdown
import tempfile

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)
# Configure Gemini client

app = Flask(__name__)

# Database setup
engine = create_engine('sqlite:///PHSI191_questions.db')
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
    ONLY AND ONLY SAY THESE THINGS: The correct answer is **D** because of three main factors:

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

def extract_text_from_image(image_path):
    try:
        with open(image_path, "rb") as image_file:
            image_bytes = image_file.read()

        # Send image + prompt together in parts

        my_file = client.files.upload(file=image_path)

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[my_file, "Extract all text from this physics problem exactly as written. ONLY RETURN THE QUESTION TEXT, NOTHING ELSE."],
        )
        
        print("Gemini response:", response.text)
        return response.text.strip()
    except Exception as e:
        print(f"Image processing failed: {e}")
        return None

    
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_term = request.form.get('search')
        uploaded_file = request.files.get('image')  # Fixed line

        if uploaded_file and uploaded_file.filename != '':
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
                uploaded_file.save(tmp.name)
                extracted_text = extract_text_from_image(tmp.name)
                if extracted_text:
                    search_term = extracted_text.strip()  # Clean up any trailing newlines or whitespace

        if not search_term:
            return render_template('index.html', error="Please enter a search term or upload an image.")
        
        session = Session()
        results = session.query(Question).filter(
            Question.question_text.ilike(f"%{search_term}%")
        ).limit(5).all()
        
        processed_results = []
        for result in results:
            explanation = generate_explanation(result.question_text, result.answer_text)
            processed_results.append({
                'question_text': result.question_text,
                'answer_text': result.answer_text,
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
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

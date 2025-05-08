QuBot PHSI191 Question Search
#### Video Demo:  https://youtu.be/dmpEndy8054 
#### Description:
QuBot is an intelligent, searchable web app designed to help students at my Univerasity succeed in Physics, a first-year physics course that often challenges students with conceptual depth and demanding multiple-choice assessments. This project aims to make exam preparation more efficient and meaningful by providing not only access to past questions and correct answers, but also detailed explanations powered by AI.

Built with Python and Flask, QuBot combines a structured SQLite database with the language capabilities of the Gemini API to offer a seamless, searchable interface for physics revision. Whether you're targeting specific physics topics or just reviewing past paper questions, QuBot offers an interactive and intelligent platform to study smarter.

Many students struggle to prepare for physics exams due to a lack of structured access to past questions and explanations. While practice questions are often provided in bulk PDF format, they lack interactivity and real-time feedback. This slows down revision and leads to passive learning. QuBot solves this by providing:

* A fast, keyword-based search engine for past questions.
* Immediate access to correct answers.
* AI-generated, context-specific explanations using Gemini, which help reinforce understanding of core physics concepts.

How It Works?

1. Database Creation (SQLAlchemy):
   The foundation of the app is a custom SQLite database built using SQLAlchemy ORM. Data for this database was sourced from a CSV file that separated each physics multiple-choice question and its correct answer using a semicolon (;) as the delimiter. Each row in the CSV represents one question-answer pair. The import process was handled by a Python script that reads the CSV file line by line, extracts the question and answer, and inserts them into the database through the SQLAlchemy model. This method allowed for clean and consistent population of the database without manual entry. The simplicity of using semicolons as delimiters was a deliberate choice to avoid parsing issues caused by commas, which are often found in question text.

2. Flask Web App:
   The core application was built using Flask, chosen for its lightweight and flexible architecture. Users interact with a simple and intuitive web interface. When a search is performed, the backend receives the search term, queries the SQLite database using SQLAlchemy, and returns all matching questions. The search functionality checks for the presence of the keyword within the question text, allowing students to look up concepts, terms, or phrases they are currently studying. When the matching question is displayed, the app automatically prompts the Gemini API using the full question and its correct answer, returning a detailed explanation alongside the result. This removes the need for additional clicks and streamlines the user experience for rapid study and comprehension.

3. GEMINI API Integration
   When a user performs a search and a matching question is found, the app automatically sends a prompt to the Gemini API. The prompt includes:

   * The full original question
   * The correct answer

   Gemini then responds with a detailed explanation, including:

   * The reasoning steps leading to the correct answer
   * Common misconceptions
   * Core physics principles involved

   This turns each past question into a micro-lesson, helping students not only memorize answers but build real understanding. This integration allows the app to provide tailored explanations that adapt to the context of each question, mimicking the effect of having a private tutor. It also gives students confidence in their reasoning process by showing them the logic and physics laws behind each answer. The automation of this step — immediately after a search — was a deliberate design choice to keep the interface simple and user-focused, minimizing friction during study sessions.

File Structure:
app.py: contains the routing logic, search query handling, and the Gemini API integration. When a search request is made, it queries the database and renders the result page with matched questions. As soon as a question is retrieved, app.py also handles the Gemini API call and returns the AI-generated explanation along with the question and answer. This centralized control ensures clean communication between the frontend and backend and allows easy future modifications like adding filters, topics, or difficulty levels.

models.py: This defines the SQLAlchemy model for the questions database. Each question includes a question_text and correct_answer field. The model was designed to be simple yet scalable, in case more fields like topic tags or difficulty levels are added later. The use of SQLAlchemy also makes the codebase more maintainable and database-agnostic for future expansion beyond SQLite.

This project reflects a balance between simplicity, usability, and technical depth. I debated whether to allow multiple questions to be explained at once or limit it to one explanation per search to avoid unnecessary API calls and cost. In the end, I opted for a one-question-one-prompt approach to maintain clarity and control. I also chose Gemini over other models due to its integration flexibility and explanation quality. Future improvements could include user authentication, bookmarking questions, tagging by topic, and even tracking performance over time. QuBot has already proven useful as a study tool and has the potential to be scaled to other university courses or subjects.

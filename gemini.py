import base64
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
import io
import httpx


load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

doc_url_1 = "https://dl.ibdocs.re/IB%20PAST%20PAPERS%20-%20SUBJECT/Group%204%20-%20Sciences/Physics_HL/2008%20November%20Examination%20Session/Physics_paper_1_HL.pdf"
doc_url_2 = "https://dl.ibdocs.re/IB%20PAST%20PAPERS%20-%20SUBJECT/Group%204%20-%20Sciences/Physics_HL/2008%20November%20Examination%20Session/Physics_paper_1_HL_markscheme.pdf"

# Retrieve and upload both PDFs using the File API
doc_data_1 = io.BytesIO(httpx.get(doc_url_1).content)
doc_data_2 = io.BytesIO(httpx.get(doc_url_2).content)

sample_pdf_1 = client.files.upload(
  file=doc_data_1,
  config=dict(mime_type='application/pdf')
)
sample_pdf_2 = client.files.upload(
  file=doc_data_2,
  config=dict(mime_type='application/pdf')
)

prompt = "What is the answer to 'The diameter of a proton is of the order of which of the following?"

response = client.models.generate_content(
  model="gemini-2.0-flash",
  contents=[sample_pdf_1, sample_pdf_2, prompt])
print(response.text)
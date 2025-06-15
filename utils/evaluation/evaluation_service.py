import docx
import PyPDF2
import json
import re
import os
from utils.common.gemini_service import GeminiService
from utils.common.db import DatabaseService

gemini = GeminiService()
data=DatabaseService()


def extract_text(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.pdf':
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
    elif ext == '.docx':
        doc = docx.Document(file_path)
        text = ""
        for para in doc.paragraphs:
            text += para.text + "\n"
        return text
    else:
        raise ValueError("Unsupported file type. Please provide a .pdf or .docx file.")


def evaluate_exam_prompt(exam_content):
    prompt = f"""
Evaluate the exam answers provided below using ADK criteria. Provide a summary evaluation and a score out of 100.

Exam Content:
{exam_content}

Return the evaluation in JSON format with the keys:
- "evaluation": a string summary of the exam performance.
- "score": an integer score between 0 and 100.
Only return the JSON.
"""
    return prompt
def clean_response(response):
    cleaned = re.sub(r"^```(?:json)?|```$", "", response, flags=re.IGNORECASE).strip()
    return json.loads(cleaned)

def evaluate_exam(file_path):
    exam_content = extract_text(file_path)
    prompt = evaluate_exam_prompt(exam_content)
    response = gemini.get_response(prompt)
    cleaned=clean_response(response)
    print(cleaned)
    data.store_exam_values(file_path, cleaned)



path=input("Enter the absolute path of the file")
evaluate_exam(path)



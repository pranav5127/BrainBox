import os
import json
import re

import PyPDF2
from docx import Document
from utils.common.gemini_service import GeminiService
from utils.common.db import ExamDataBaseService

"""
AI-Powered Exam Evaluation Service

This module automates end-to-end exam evaluation using:
- Gemini AI for evaluation generation
- JSON parsing and validation
- Database storage for evaluated results

The module includes utilities for:
    - Extracting text from uploaded exam files (PDF/DOCX)
    - Generating structured evaluation prompt using Gemini API
    - Parsing and cleaning AI response
    - Persisting evaluation results to database

Dependencies:
    - GeminiService (for prompt-based evaluation)
    - ExamDataBaseService (for storing evaluation results)

Functions:
    - build_evaluation_prompt(exam_content): Constructs a formatted evaluation prompt.
    - clean_gemini_response(response): Cleans and parses Gemini output.
    - evaluate_exam_from_file(file_path): Full pipeline to extract, evaluate, and store exam result.
"""



class ExamEvaluationService:
    gemini = GeminiService()
    database = ExamDataBaseService()

    @staticmethod
    def extract_text(file_path: str) -> str:
        """
        Extracts text from a PDF or DOCX exam file.
        """
        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.pdf':
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                return text

        elif ext == '.docx':
            doc = Document(file_path)
            text = ""
            for para in doc.paragraphs:
                text += para.text + "\n"
            return text

        else:
            raise ValueError("Unsupported file type. Only PDF and DOCX supported.")

    @staticmethod
    def build_evaluation_prompt(exam_content: str) -> str:
        """
        Builds structured Gemini prompt for exam evaluation.
        """
        return f"""
        Evaluate the exam answers provided below using ADK criteria. Provide a detailed evaluation and a score out of 100.

        Exam Content:
        {exam_content}

        Output JSON only with:
        - "evaluation": string (exam performance summary)
        - "score": integer (0-100)
        No extra text, no ```json or markdown formatting.
        """

    @staticmethod
    def clean_gemini_response(response: str) -> dict:
        """
        Cleans Gemini's raw response and parses it into a dictionary.
        """
        cleaned = re.sub(r"^```(?:json)?|```$", "", response, flags=re.IGNORECASE).strip()
        return json.loads(cleaned)

    @classmethod
    def evaluate_exam_from_file(cls, file_path: str) -> dict:
        """
        Full evaluation pipeline:
        - Extract exam text
        - Generate Gemini evaluation
        - Clean & parse response
        - Store in database
        """
        if not file_path or not os.path.exists(file_path):
            return {"status": "error", "error": "Invalid or missing file path."}

        try:
            exam_content = cls.extract_text(file_path)
            prompt = cls.build_evaluation_prompt(exam_content)
            response = cls.gemini.get_response(prompt)
            result = cls.clean_gemini_response(response)

            cls.database.store_exam_values(file_path, result)

            return {
                "status": "success",
                "file": file_path,
                "evaluation": result
            }

        except Exception as e:
            return {"status": "error", "error": str(e)}



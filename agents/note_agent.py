from utils.common.db import NoteDataBaseService
from utils.common.rag_service import GeminiRAGService



Store=NoteDataBaseService()

def generate_notes_prompt():
        prompt = f"""
Create a list of 10 concise bullet points about the topic: in the above text.
Respond in JSON format as a simple array of strings.
Example:
[
  "Bullet point 1",
  "Bullet point 2",
  ...
  "Bullet point 10"
]
Only return the JSON array. No extra explanations or markdown.
"""
        return prompt

FilePath=input("Enter the file path of the document")

gemini=GeminiRAGService(
    file_path=FilePath
)

prompt=generate_notes_prompt()
response=gemini.get_answer(prompt)
print(response)
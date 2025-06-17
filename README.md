# 📚 **BrainBox AI Agent**

**BrainBox** is an AI-powered, multi-functional Python project that combines:
- 📑 Automatic **presentation generation** with relevant images
- 📝 Smart **exam evaluation**
- 📌 Context-aware **note extraction**
- ☁️ Automatic **file hosting** on Cloudinary with scheduled cleanup  
- 🔑 Seamless integration with **Google Gemini** (Generative AI) for all text generations and RAG (retrieval-augmented generation).

This project uses **LangChain**, **Gemini API**, **Cloudinary**, **python-pptx**, and **SQLite** — all orchestrated with a local agent or programmatic interface.

---

## 🚀 **Features**

✅ Generate beautiful PowerPoint slides for any topic, complete with AI-generated content and relevant images.  
✅ Upload generated presentations to Cloudinary with auto-expiry for efficient storage.  
✅ Evaluate textual exam answers automatically using Gemini and store results.  
✅ Extract concise bullet-point notes from any document.  
✅ Use an **ADK Agent** to run all tools programmatically.

---

## 🗂️ **Project Structure**

| File / Directory | Description |
|------------------|--------------|
| `agents/evaluation_agent.py` | Defines the `evaluate_agent` function to score and analyze exams. |
| `agents/presentation_agent.py` | Defines `generate_presentation_from_topic` for creating slides with Gemini + images. |
| `utils/common/cloudinary_service.py` | Handles Cloudinary uploads & schedules auto-deletion after a delay. |
| `utils/common/db.py` | Contains `NoteDataBaseService` & `ExamDataBaseService` for SQLite storage of notes and exam results. |
| `utils/common/gemini_service.py` | Gemini API integration for prompt-based text generation. |
| `utils/common/rag_service.py` | Handles retrieval-augmented generation for smarter answers from local documents. |
| `utils/evaluation/evaluation_service.py` | Core logic to score & evaluate exams using Gemini. |
| `utils/presentation/image_search_service.py` | Finds slide-relevant images (e.g., via Wikimedia) for each slide. |
| `utils/presentation/presentation_service.py` | Creates `.pptx` slides using `python-pptx`. |
| `root_agent.py` | Defines the ADK `Agent` that exposes presentation creation and exam evaluation as callable tools. |
| `.env` | Stores your API keys & credentials (should not be committed to version control!). |

---

## ⚙️ **Installation**

### ✅ 1️⃣ Clone the repo

```bash
git clone https://github.com/pranav5127/BrainBox.git

```

### ✅ 2️⃣ Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
---

## 🔑 **Environment Setup**

Create a `.env` file in the **root** folder:

```env
# .env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
CLOUDINARY_CLOUD_NAME=YOUR_CLOUDINARY_CLOUD_NAME
CLOUDINARY_API_KEY=YOUR_CLOUDINARY_API_KEY
CLOUDINARY_API_SECRET=YOUR_CLOUDINARY_API_SECRET
```

**Important:**  
✅ Never commit `.env` to GitHub!  
✅ Add `.env` to `.gitignore`:
```txt
.env
```

---

## ⚡ **Usage**

### 🖼️ 1️⃣ Generate a presentation

```python
from agents.presentation_agent import generate_presentation_from_topic

result = generate_presentation_from_topic("Artificial Intelligence")
print(result["presentation_url"])
```

This will:
- Use Gemini to generate slides + bullet points.
- Use image search to find relevant images.
- Create a `.pptx` file.
- Upload it to Cloudinary.
- Return a shareable link that auto-deletes after 5 minutes.

---

### 📝 2️⃣ Evaluate an exam file

```python
from agents.evaluation_agent import evaluate_agent

result = evaluate_agent("/path/to/exam.txt")
print(result)
```

---

## 🚀 Run the Project

Once your `.env` is set, start the agent with **ADK**:

```bash
adk run agents
```

---

## 🗂️ **Database**

✅ Exam results are stored in `data/question.db`  
✅ Notes are stored in `data/notes.db`

SQLite tables are created automatically if they don’t exist.

---
[LICENSE](LICENSE)
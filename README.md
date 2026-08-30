# 🚀 AI Internship Match Assistant

> **AI-powered Resume–JD Analysis platform for students and internship seekers.**  
> Upload a resume, upload or paste a job description, get a realistic match analysis, identify missing skills, download a PDF report, and ask follow-up questions using a RAG-style contextual assistant.

---

## 🌐 Live Demo

🔗 Live App: https://ai-internship-match-assistant.onrender.com
---

## 📌 Project Overview

**AI Internship Match Assistant** is a Flask-based web application that helps students compare their resume with an internship or job description.

Many students apply to internships without clearly knowing:

- Whether their resume matches the role
- Which skills are missing
- Which JD keywords are important
- Whether their projects are relevant
- What they should improve first

This project solves that problem using an LLM-powered Resume–JD analysis flow with file upload support, PDF report generation, and a RAG-style follow-up assistant.

The assistant focuses on **honest, practical, and student-friendly feedback** rather than unrealistic or exaggerated resume suggestions.

---

## ✨ Key Features

### 📄 Resume & JD Input

- Upload resume as **PDF** or **DOCX**
- Upload job description as **PDF**, **DOCX**, or **TXT**
- Paste resume text manually
- Paste job description manually
- File name preview after upload

### 🤖 AI Resume–JD Analysis

- Overall match score
- Strong matching areas
- Partial matching areas
- Missing or weak skills
- Resume weak point analysis
- JD keywords to add honestly
- Project relevance analysis
- Internship suitability verdict
- Practical 5-step action plan

### 🧠 RAG-Style Follow-up Assistant

- Ask follow-up questions after analysis
- Context-aware answers based on resume, JD, and previous analysis
- Basic retrieved context support
- Retrieved context transparency in UI
- Suggestion chips for common questions

Example questions:

```text
Which skill should I learn first?
What keywords can I honestly add?
Rewrite my project section for this JD.
Which RAG and vector database skills are missing?
```

### 📥 Report & Productivity Features

- Copy analysis result
- Clear all inputs and outputs
- Download analysis as **PDF report**
- Dark/light theme toggle
- Clean reading-friendly result layout
- Responsive UI for desktop and mobile

---

## 🧰 Tech Stack

### 🎨 Frontend

- HTML
- CSS
- JavaScript

### ⚙️ Backend

- Python
- Flask

### 🧠 AI / LLM

- Groq API
- openai/gpt-oss-20b

### 📄 Document Processing

- pypdf
- python-docx

### 🧩 RAG-Style Retrieval

- Text cleaning
- Text chunking
- Resume/JD chunk labeling
- Keyword-based retrieval
- Phrase-boost retrieval
- Retrieved context display

### 📑 Report Generation

- ReportLab

### ☁️ Deployment

- Render
- Gunicorn

---

## ⚙️ How It Works

```text
Resume / JD Upload
        ↓
Text Extraction
        ↓
AI Resume–JD Analysis
        ↓
Structured Match Report
        ↓
Follow-up Question
        ↓
RAG-style Context Retrieval
        ↓
Context-aware Assistant Answer
        ↓
PDF Report Download
```

Step-by-step flow:

1. User uploads or pastes a resume.
2. User uploads or pastes a job description.
3. Flask backend extracts text from uploaded files.
4. Resume and JD text are sent to the Groq LLM API.
5. AI generates a structured Resume–JD analysis.
6. User can ask follow-up questions.
7. The app retrieves relevant resume/JD chunks.
8. The assistant answers using retrieved context and previous analysis.
9. User can copy the result or download it as a PDF report.

---

## 🧠 Current RAG Implementation

This project currently includes a **RAG-style contextual follow-up assistant**.

### ✅ Implemented

- Text cleaning
- Text chunking
- Resume/JD chunk labeling
- Basic keyword-based retrieval
- Phrase-boost retrieval
- Retrieved context formatting
- Retrieved context display in UI
- Context-aware follow-up answers

### 🚧 Not Yet Implemented

- Embedding-based semantic search
- FAISS or ChromaDB vector database
- Persistent vector storage
- Login system
- Saved analysis history

> The current version uses a retrieval-augmented flow, but it does **not** claim full vector database RAG yet.

---

## 📁 Project Structure

```text
AI_Internship_Match_Assistant/
│
├── app.py
├── rag_utils.py
├── requirements.txt
├── Procfile
├── .env.example
├── .gitignore
├── README.md
│
├── templates/
│   └── index.html
│
└── static/
    ├── style.css
    └── script.js
```

---

## 🛠️ Local Setup

### 1️⃣ Clone the repository

```bash
git clone https://github.com/sauravoole-ai/AI_Internship_Match_Assistant.git
cd AI_Internship_Match_Assistant
```

### 2️⃣ Create a virtual environment

```bash
python -m venv venv
```

### 3️⃣ Activate the virtual environment

For Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

For Command Prompt:

```cmd
venv\Scripts\activate.bat
```

### 4️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 5️⃣ Create `.env` file

Create a file named `.env` in the root folder.

Add your Groq API key:

```env
GROQ_API_KEY=your_real_groq_api_key_here
```

⚠️ Do not upload the real `.env` file to GitHub.

### 6️⃣ Run the app locally

```bash
python app.py
```

Open in browser:

```text
http://127.0.0.1:5000
```

---

## 🔐 Environment Variables

Use `.env.example` as a reference.

```env
GROQ_API_KEY=your_groq_api_key_here
```

The real key should be stored only in `.env`.

---

## ☁️ Deployment on Render

### Build Command

```bash
pip install -r requirements.txt
```

### Start Command

```bash
gunicorn app:app
```

### Environment Variable on Render

```env
GROQ_API_KEY=your_real_groq_api_key_here
```

---

## 📦 Requirements

The project uses the following Python packages:

```text
flask
python-dotenv
groq
gunicorn
pypdf
python-docx
reportlab
```

---

## ✅ Completed Features

```text
✅ Resume text paste
✅ JD text paste
✅ Resume PDF/DOCX upload
✅ JD PDF/DOCX/TXT upload
✅ AI Resume–JD analysis
✅ Match score generation
✅ Skill gap analysis
✅ ATS keyword suggestions
✅ Project relevance analysis
✅ RAG-style follow-up assistant
✅ Retrieved context transparency
✅ Copy result
✅ Clear all
✅ PDF report download
✅ Dark/light theme toggle
✅ Responsive premium UI
```

---

## 🚧 Future Improvements

- FAISS or ChromaDB vector database integration
- Embedding-based semantic search
- Persistent vector storage
- Login system
- Saved analysis history
- Advanced PDF report design
- Resume rewrite assistant
- Cover letter generator
- Job application tracker
- Multiple resume comparison
- Better analytics dashboard

---

## 🎯 Resume Relevance

This project demonstrates practical skills in:

- Flask web development
- REST-style backend API handling
- LLM API integration
- Prompt engineering
- File upload handling
- PDF/DOCX/TXT text extraction
- RAG-style retrieval
- Frontend UI/UX development
- Responsive web design
- PDF report generation
- Deployment preparation

---

## ⚠️ Important Notes

- This app provides AI-generated guidance, not guaranteed hiring results.
- The app does not claim that a candidate will be selected.
- Resume keywords should only be added if the user can honestly justify them.
- The current RAG feature is keyword/phrase-retrieval based.
- Full vector database RAG is planned as a future improvement.
- Real API keys must not be committed to GitHub.

---

## 👨‍💻 Author

**Saurav Jha**  
B.Tech Electronics and Communication Engineering

Interests:

- Applied AI
- Generative AI
- LLM API-based applications
- AI automation
- AIoT
- Resume-focused AI tools
- Internship-ready AI product development

---

## 📜 Disclaimer

This project is intended for educational and career-assistance purposes.  
The analysis generated by the AI should be treated as guidance and not as a final hiring decision.

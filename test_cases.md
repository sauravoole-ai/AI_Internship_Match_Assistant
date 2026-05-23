# 🧪 Test Cases — AI Internship Match Assistant

A short manual testing checklist for the most important project features.

---

## ✅ Test Summary

| Feature Area | Status |
|---|---|
| Resume–JD Analysis | Tested |
| File Upload | Tested |
| Follow-up Assistant | Tested |
| RAG-style Context Retrieval | Tested |
| PDF Report Download | Tested |
| UI/UX Actions | Tested |

---

## 1. Resume–JD Analysis

**Test:** Paste resume text and job description manually.

**Expected Result:**

- App accepts both inputs.
- AI analysis is generated successfully.
- Result includes match score, strong areas, weak/missing skills, project relevance, and action plan.

**Status:** ✅ Passed

---

## 2. Resume and JD File Upload

**Test:** Upload resume as PDF/DOCX and job description as PDF/DOCX/TXT.

**Expected Result:**

- Uploaded file names appear correctly.
- Backend extracts text from uploaded files.
- Analysis works using uploaded documents.

**Status:** ✅ Passed

---

## 3. Follow-up Assistant

**Test Question:**

```text
Which skill should I learn first for this JD?

Expected Result:

Assistant answers only after analysis is completed.
Answer uses resume, job description, and previous analysis context.
Assistant gives practical improvement guidance.

Status: ✅ Passed

4. RAG-style Context Retrieval

Test Question:

Which RAG and vector database skills are missing from my resume?

Expected Result:

Assistant identifies missing skills such as RAG, embeddings, FAISS, ChromaDB, LangChain, semantic search, and document Q&A.
Retrieved Context Used section shows relevant resume/JD chunks.
Assistant does not wrongly treat IoT/ESP32 as vector database experience.

Status: ✅ Passed

5. PDF Report Download

Test: Run analysis and click Download Report.

Expected Result:

PDF report downloads successfully.
Report contains the generated Resume–JD analysis.

Status: ✅ Passed

6. UI/UX Actions

Test: Check Clear All, Copy Result, theme toggle, and mobile layout.

Expected Result:

Clear All resets inputs, file names, result, assistant answer, and retrieved context.
Copy Result copies the generated analysis.
Dark/light theme toggle works and remains saved after refresh.
Layout remains usable in mobile preview.

Status: ✅ Passed

Notes
Testing was done manually during local development.
Current RAG implementation is keyword/phrase retrieval based.
The app provides AI-generated guidance and does not guarantee internship selection.
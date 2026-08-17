from flask import Flask, render_template, request, jsonify, send_file
from dotenv import load_dotenv
from groq import Groq
from pypdf import PdfReader
from rag_utils import create_document_chunks, retrieve_relevant_chunks, format_retrieved_chunks
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import docx
import os
import io
import textwrap

load_dotenv()

app = Flask(__name__)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)


def extract_text_from_pdf(file):
    pdf_bytes = file.read()
    pdf_stream = io.BytesIO(pdf_bytes)

    reader = PdfReader(pdf_stream)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text.strip()


def extract_text_from_docx(file):
    document = docx.Document(file)

    text = ""

    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            text += paragraph.text.strip() + "\n"

    return text.strip()


def extract_text_from_txt(file):
    text_bytes = file.read()

    try:
        return text_bytes.decode("utf-8").strip()
    except UnicodeDecodeError:
        return text_bytes.decode("latin-1").strip()


def extract_text_from_uploaded_file(file, allowed_types_text):
    if not file or not file.filename:
        return ""

    filename = file.filename.lower()

    if filename.endswith(".pdf"):
        return extract_text_from_pdf(file)

    if filename.endswith(".docx"):
        return extract_text_from_docx(file)

    if filename.endswith(".txt"):
        return extract_text_from_txt(file)

    raise ValueError(f"Unsupported file type. Please upload {allowed_types_text}.")


def get_final_text(pasted_text, uploaded_file, allowed_types_text):
    if uploaded_file and uploaded_file.filename:
        return extract_text_from_uploaded_file(uploaded_file, allowed_types_text)

    return pasted_text.strip()


def create_pdf_report(report_text):
    buffer = io.BytesIO()

    pdf = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    left_margin = 0.75 * inch
    right_margin = 0.75 * inch
    top_margin = 0.75 * inch
    bottom_margin = 0.75 * inch

    y_position = height - top_margin

    pdf.setTitle("Resume JD Analysis Report")

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(left_margin, y_position, "AI Internship Match Assistant Report")

    y_position -= 0.35 * inch

    pdf.setFont("Helvetica", 9)
    pdf.drawString(left_margin, y_position, "AI-generated guidance report. Use as support, not as a guaranteed hiring decision.")

    y_position -= 0.35 * inch

    pdf.setFont("Helvetica", 10)

    usable_width = width - left_margin - right_margin
    characters_per_line = int(usable_width / 5.2)

    lines = report_text.splitlines()

    for line in lines:
        if not line.strip():
            y_position -= 0.16 * inch
            continue

        wrapped_lines = textwrap.wrap(line, width=characters_per_line)

        for wrapped_line in wrapped_lines:
            if y_position <= bottom_margin:
                pdf.showPage()
                y_position = height - top_margin
                pdf.setFont("Helvetica", 10)

            if line.strip().startswith(tuple([f"{i}." for i in range(1, 11)])):
                pdf.setFont("Helvetica-Bold", 11)
            else:
                pdf.setFont("Helvetica", 10)

            pdf.drawString(left_margin, y_position, wrapped_line)
            y_position -= 0.20 * inch

    pdf.save()

    buffer.seek(0)
    return buffer


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        resume_text = request.form.get("resume_text", "").strip()
        jd_text = request.form.get("jd_text", "").strip()

        resume_file = request.files.get("resume_file")
        jd_file = request.files.get("jd_file")

        final_resume_text = get_final_text(
            resume_text,
            resume_file,
            "a PDF, DOCX, or pasted resume text"
        )

        final_jd_text = get_final_text(
            jd_text,
            jd_file,
            "a PDF, DOCX, TXT, or pasted job description"
        )

        if not final_resume_text or not final_jd_text:
            return jsonify({
                "success": False,
                "error": "Please provide resume and job description using paste or file upload."
            }), 400

        prompt = f"""
You are an expert AI Resume-JD Analyzer and Internship Match Assistant.

Your job is to compare the given resume with the given internship/job description.

Important rules:
- Read the resume carefully before judging.
- Do not say a skill or project is missing if it is already present in the resume.
- Do not invent skills, projects, experience, certifications, or achievements.
- Be honest and practical.
- Avoid generic advice.
- Focus on internship readiness.
- If a skill is partially present, mention it as "partially matching" only when actual related evidence exists.
- Career interest alone must not be counted as real skill experience.
- Do not connect unrelated technologies.
- IoT, ESP32, MQTT, sensors, or hardware exposure must not be treated as RAG, embeddings, vector database, LangChain, or semantic search experience.
- PDF download support must not be treated as PDF parsing or document intelligence.
- If the resume mentions AI chatbot, LLM API, Flask, deployment, GitHub, REST API, or project work, recognize it properly.
- Keep the tone professional and useful for a student improving their resume.

Analyze using this exact structure:

1. Overall Match Score out of 100
Give a realistic score and one short reason.

2. Strong Matching Areas
List the strongest overlaps between resume and JD.

3. Partial Matching Areas
List skills where the resume shows related exposure but not full JD-level strength.

4. Missing or Weak Areas
List only those skills that are genuinely absent or weak.

5. Resume Weak Points
Mention issues in the resume presentation, clarity, keyword usage, or project description.

6. JD Keywords to Add Honestly
Suggest keywords only if the student can honestly justify them through real project work or learning.

7. Project Relevance Analysis
Explain how the mentioned projects help for this JD.

8. Upgrade Suggestions
Suggest practical improvements to make the profile stronger for this internship.

9. Internship Suitability Verdict
Classify as one of:
- Strong fit
- Good fit with improvements
- Moderate fit
- Weak fit currently

10. Final 5-Step Action Plan
Give exactly 5 clear actions.

Resume:
{final_resume_text}

Job Description:
{final_jd_text}
"""

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "system",
                    "content": "You are a careful, accurate, professional resume and job description matching assistant."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            reasoning_effort="medium",
            include_reasoning=False,
            temperature=0.2,
            max_tokens=1700
        )

        ai_result = response.choices[0].message.content

        return jsonify({
            "success": True,
            "result": ai_result,
            "resume_text_used": final_resume_text[:6000],
            "jd_text_used": final_jd_text[:6000]
        })

    except ValueError as error:
        return jsonify({
            "success": False,
            "error": str(error)
        }), 400

    except Exception as error:
        return jsonify({
            "success": False,
            "error": str(error)
        }), 500


@app.route("/ask", methods=["POST"])
def ask_followup():
    try:
        data = request.get_json()

        question = data.get("question", "").strip()
        resume_text = data.get("resume_text", "").strip()
        jd_text = data.get("jd_text", "").strip()
        analysis_text = data.get("analysis_text", "").strip()

        if not question:
            return jsonify({
                "success": False,
                "error": "Please enter a follow-up question."
            }), 400

        if not analysis_text:
            return jsonify({
                "success": False,
                "error": "Please run a Resume-JD analysis first, then ask a follow-up question."
            }), 400

        document_chunks = create_document_chunks(resume_text, jd_text)
        retrieved_chunks = retrieve_relevant_chunks(question, document_chunks, top_k=4)
        retrieved_context = format_retrieved_chunks(retrieved_chunks)

        prompt = f"""
You are a RAG-style follow-up assistant for a Resume-JD analysis tool.

You must answer the user's question using:
1. Retrieved resume/JD chunks
2. Previous AI analysis
3. The user's actual question

Rules:
- Prioritize the retrieved context.
- Do not invent experience.
- Do not overclaim.
- Clearly separate what is present, missing, and recommended.
- If suggesting resume keywords, mention only those that can be honestly justified.
- If rewriting content, keep it suitable for a student/fresher profile.
- If the retrieved context is insufficient, say what is missing.
- Keep the answer concise but useful.
- Use bullet points when helpful.

Retrieved Resume/JD Context:
{retrieved_context}

Previous Analysis:
{analysis_text}

User Question:
{question}
"""

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "system",
                    "content": "You are a practical RAG-style resume improvement and internship matching assistant."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            reasoning_effort="low",
            include_reasoning=False,
            temperature=0.25,
            max_tokens=900
        )

        answer = response.choices[0].message.content

        return jsonify({
            "success": True,
            "answer": answer,
            "retrieved_context": retrieved_context
        })

    except Exception as error:
        return jsonify({
            "success": False,
            "error": str(error)
        }), 500


@app.route("/download-report", methods=["POST"])
def download_report():
    try:
        data = request.get_json()
        report_text = data.get("report_text", "").strip()

        if not report_text:
            return jsonify({
                "success": False,
                "error": "No report text available to download."
            }), 400

        pdf_buffer = create_pdf_report(report_text)

        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name="resume_jd_analysis_report.pdf",
            mimetype="application/pdf"
        )

    except Exception as error:
        return jsonify({
            "success": False,
            "error": str(error)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)

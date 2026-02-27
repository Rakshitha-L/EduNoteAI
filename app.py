import streamlit as st
from fpdf import FPDF
import re

st.set_page_config(page_title="EduNote AI", layout="wide")

st.title("🎓 EduNote AI")
st.subheader("Lecture Text → Smart Notes Generator")

# -----------------------------
# Simple Text Cleaning
# -----------------------------
def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# -----------------------------
# Simple Extractive Summary
# -----------------------------
def generate_summary(text):
    sentences = text.split(".")
    summary = ". ".join(sentences[:3])
    return summary.strip()

# -----------------------------
# Key Points Generator
# -----------------------------
def generate_keypoints(text):
    sentences = text.split(".")
    points = sentences[:5]
    return "\n".join([f"• {point.strip()}" for point in points if point.strip()])

# -----------------------------
# Quiz Generator
# -----------------------------
def generate_quiz(text):
    sentences = text.split(".")
    questions = []
    for i, sentence in enumerate(sentences[:3]):
        if sentence.strip():
            questions.append(f"{i+1}. What does this mean?\n   → {sentence.strip()}?\n")
    return "\n".join(questions)

# -----------------------------
# PDF Generator
# -----------------------------
def generate_pdf(content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 8, content)
    file_path = "Lecture_Notes.pdf"
    pdf.output(file_path)
    return file_path

# -----------------------------
# Text Input
# -----------------------------
lecture_text = st.text_area("📚 Paste Your Lecture Text Here", height=250)

if st.button("Generate Smart Notes"):

    if lecture_text.strip() == "":
        st.warning("Please paste lecture text.")
    else:
        cleaned = clean_text(lecture_text)

        st.subheader("📄 Cleaned Text")
        st.write(cleaned)

        st.subheader("📝 Summary")
        summary = generate_summary(cleaned)
        st.write(summary)

        st.subheader("📌 Key Points")
        keypoints = generate_keypoints(cleaned)
        st.write(keypoints)

        st.subheader("❓ Quiz Questions")
        quiz = generate_quiz(cleaned)
        st.write(quiz)

        full_content = f"""
SUMMARY:
{summary}

KEY POINTS:
{keypoints}

QUIZ:
{quiz}
"""

        if st.button("Download Notes as PDF"):
            pdf_file = generate_pdf(full_content)
            with open(pdf_file, "rb") as f:
                st.download_button("Click Here to Download", f, file_name="Lecture_Notes.pdf")

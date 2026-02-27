import streamlit as st
import re
from fpdf import FPDF

# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(page_title="EduNoteAI", layout="wide")
st.title("🎓 EduNoteAI – Smart Lecture Notes Generator")
st.subheader("Lecture Text → Structured Smart Notes")

# -------------------------------------------------
# Text Cleaning
# -------------------------------------------------
def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    return text

# -------------------------------------------------
# Smart Summary Generator
# -------------------------------------------------
def generate_summary(text):
    sentences = text.split(". ")
    summary = ". ".join(sentences[:3])
    return summary.strip() + "."

# -------------------------------------------------
# Key Points Generator
# -------------------------------------------------
def generate_keypoints(text):
    sentences = text.split(". ")
    keypoints = []

    for sentence in sentences:
        sentence = sentence.strip()
        if len(sentence) > 50:
            keypoints.append("• " + sentence)

        if len(keypoints) == 6:
            break

    return "\n".join(keypoints)

# -------------------------------------------------
# Important Terms Extractor
# -------------------------------------------------
def extract_important_terms(text):
    words = text.split()
    terms = []

    for word in words:
        clean_word = re.sub(r'[^A-Za-z]', '', word)

        if clean_word.istitle() and len(clean_word) > 4:
            if clean_word not in terms:
                terms.append(clean_word)

        if len(terms) == 5:
            break

    return ", ".join(terms)

# -------------------------------------------------
# Quiz Generator
# -------------------------------------------------
def generate_quiz(text):
    keywords = []
    words = text.split()

    for word in words:
        clean_word = re.sub(r'[^A-Za-z]', '', word)

        if clean_word.istitle() and len(clean_word) > 4:
            if clean_word not in keywords:
                keywords.append(clean_word)

        if len(keywords) == 3:
            break

    questions = []
    for word in keywords:
        questions.append(f"1. What is the significance of {word} in this topic?")

    return "\n\n".join(questions)

# -------------------------------------------------
# PDF Generator
# -------------------------------------------------
def generate_pdf(content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 8, content)

    file_path = "Smart_Lecture_Notes.pdf"
    pdf.output(file_path)
    return file_path

# -------------------------------------------------
# User Input
# -------------------------------------------------
lecture_text = st.text_area("📚 Paste Your Lecture Text Here", height=250)

if st.button("Generate Smart Notes"):

    if lecture_text.strip() == "":
        st.warning("Please paste lecture text first.")
    else:
        cleaned = clean_text(lecture_text)

        summary = generate_summary(cleaned)
        keypoints = generate_keypoints(cleaned)
        terms = extract_important_terms(cleaned)
        quiz = generate_quiz(cleaned)

        # -------------------------------------------------
        # Display Output
        # -------------------------------------------------
        st.markdown("## 📄 Cleaned Text")
        st.write(cleaned)

        st.markdown("## 📝 Smart Summary")
        st.write(summary)

        st.markdown("## 📌 Key Concepts")
        st.text(keypoints)

        st.markdown("## 🧠 Important Terms")
        st.write(terms)

        st.markdown("## ❓ Quiz Questions")
        st.text(quiz)

        # -------------------------------------------------
        # PDF Download
        # -------------------------------------------------
        if st.button("Download as PDF"):
            full_content = f"""
SMART LECTURE NOTES

SUMMARY:
{summary}

KEY POINTS:
{keypoints}

IMPORTANT TERMS:
{terms}

QUIZ QUESTIONS:
{quiz}
"""
            pdf_file = generate_pdf(full_content)

            with open(pdf_file, "rb") as f:
                st.download_button(
                    "Click to Download PDF",
                    f,
                    file_name="Smart_Lecture_Notes.pdf"
                )

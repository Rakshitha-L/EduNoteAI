import streamlit as st
import re
from fpdf import FPDF

# -----------------------------------------
# Page Config
# -----------------------------------------
st.set_page_config(page_title="EduNote AI", layout="wide")
st.title("🎓 EduNote AI")
st.subheader("Lecture Text → Smart Structured Notes Generator")

# -----------------------------------------
# Text Cleaning
# -----------------------------------------
def clean_text(text):
    text = re.sub(r'\b(um|ah|okay|so|like)\b', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# -----------------------------------------
# Smart Summary (Better Compression)
# -----------------------------------------
def generate_summary(text):
    sentences = text.split(". ")
    summary_sentences = []

    for sentence in sentences:
        if len(sentence) > 60:
            summary_sentences.append(sentence.strip())
        if len(summary_sentences) == 3:
            break

    return ". ".join(summary_sentences) + "."

# -----------------------------------------
# Key Concepts Extractor
# -----------------------------------------
STOPWORDS = {
    "While", "This", "That", "These", "Those",
    "The", "And", "For", "With", "Such",
    "Are", "Was", "Were", "From", "Into",
    "Between", "However"
}

def extract_key_concepts(text):
    words = re.findall(r'\b[A-Z][a-zA-Z]+\b', text)
    concepts = []

    for word in words:
        if word not in STOPWORDS and len(word) > 5:
            if word not in concepts:
                concepts.append(word)
        if len(concepts) == 5:
            break

    return concepts

# -----------------------------------------
# Important Terms
# -----------------------------------------
def extract_important_terms(text):
    words = re.findall(r'\b[A-Z][a-zA-Z]+\b', text)
    terms = []

    for word in words:
        if word not in STOPWORDS and len(word) > 6:
            if word not in terms:
                terms.append(word)
        if len(terms) == 5:
            break

    return terms

# -----------------------------------------
# Quiz Generator (Better Style)
# -----------------------------------------
def generate_quiz(text):
    sentences = text.split(". ")
    questions = []

    for sentence in sentences[:3]:
        if len(sentence) > 50:
            questions.append(f"Explain the following concept:\n{sentence.strip()}?")

    return questions

# -----------------------------------------
# PDF Generator
# -----------------------------------------
def generate_pdf(content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 8, content)
    file_path = "Smart_Lecture_Notes.pdf"
    pdf.output(file_path)
    return file_path

# -----------------------------------------
# Input Area
# -----------------------------------------
lecture_text = st.text_area("📚 Paste Your Lecture Text Here", height=250)

if lecture_text:

    cleaned_text = clean_text(lecture_text)

    st.subheader("📄 Cleaned Text")
    st.write(cleaned_text)

    # Generate Smart Notes
    summary = generate_summary(cleaned_text)
    key_concepts = extract_key_concepts(cleaned_text)
    important_terms = extract_important_terms(cleaned_text)
    quiz_questions = generate_quiz(cleaned_text)

    # -----------------------------------------
    # Display Results
    # -----------------------------------------
    st.subheader("📝 Smart Summary")
    st.write(summary)

    st.subheader("📌 Key Concepts")
    for concept in key_concepts:
        st.write(f"• {concept}")

    st.subheader("🧠 Important Terms")
    st.write(", ".join(important_terms))

    st.subheader("❓ Quiz Questions")
    for i, question in enumerate(quiz_questions, 1):
        st.write(f"{i}. {question}")

    # -----------------------------------------
    # Download PDF
    # -----------------------------------------
    if st.button("Download Notes as PDF"):
        full_content = f"""
SMART SUMMARY:
{summary}

KEY CONCEPTS:
{chr(10).join(['• ' + c for c in key_concepts])}

IMPORTANT TERMS:
{', '.join(important_terms)}

QUIZ QUESTIONS:
{chr(10).join([str(i+1) + '. ' + q for i, q in enumerate(quiz_questions)])}
"""

        pdf_file = generate_pdf(full_content)

        with open(pdf_file, "rb") as f:
            st.download_button(
                "Click Here to Download",
                f,
                file_name="Smart_Lecture_Notes.pdf"
            )

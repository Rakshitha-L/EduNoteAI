import streamlit as st
import re
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from fpdf import FPDF
import torch

torch.set_num_threads(1)

# -----------------------------------------
# Page Configuration
# -----------------------------------------
st.set_page_config(page_title="EduNote AI", layout="wide")
st.title("🎓 EduNote AI")
st.subheader("Lecture Text → Smart Structured Notes Generator")

# -----------------------------------------
# Load Model (Cached)
# -----------------------------------------
@st.cache_resource
def load_model():
    model_name = "google/flan-t5-base"

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    return tokenizer, model

tokenizer, model = load_model()

# -----------------------------------------
# Text Cleaning
# -----------------------------------------
def clean_text(text):
    text = re.sub(r'\b(um|ah|okay|so|like)\b', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# -----------------------------------------
# Generate AI Output
# -----------------------------------------
def generate_output(prompt, max_len=200):
    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        max_length=1024,
        truncation=True
    )

    output_ids = model.generate(
        inputs.input_ids,
        max_length=max_len,
        min_length=50,
        num_beams=4,
        length_penalty=2.0,
        early_stopping=True
    )

    return tokenizer.decode(output_ids[0], skip_special_tokens=True)

# -----------------------------------------
# PDF Generator
# -----------------------------------------
def generate_pdf(content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 8, content)

    file_path = "Lecture_Notes.pdf"
    pdf.output(file_path)
    return file_path

# -----------------------------------------
# User Input
# -----------------------------------------
lecture_text = st.text_area("📚 Paste Your Lecture Text Here", height=250)

if st.button("Generate Smart Notes"):

    if lecture_text.strip() == "":
        st.warning("Please enter lecture text.")
    else:
        cleaned_text = clean_text(lecture_text)

        st.subheader("📄 Cleaned Text")
        st.write(cleaned_text)

        # -----------------------------------------
        # Summary
        # -----------------------------------------
        st.info("Generating Summary...")
        summary_prompt = f"""
        Summarize the following lecture clearly in 5-6 concise sentences:

        {cleaned_text}
        """
        summary = generate_output(summary_prompt, max_len=220)

        st.subheader("📝 Summary")
        st.write(summary)

        # -----------------------------------------
        # Key Points
        # -----------------------------------------
        st.info("Extracting Key Points...")
        keypoints_prompt = f"""
        Extract exactly 5 short bullet point key points from this lecture:

        {cleaned_text}
        """
        keypoints = generate_output(keypoints_prompt, max_len=180)

        st.subheader("📌 Key Points")
        st.write(keypoints)

        # -----------------------------------------
        # Quiz Questions
        # -----------------------------------------
        st.info("Generating Quiz Questions...")
        quiz_prompt = f"""
        Generate exactly 3 short exam-style questions based on this lecture.
        Write only the questions.

        {cleaned_text}
        """
        quiz = generate_output(quiz_prompt, max_len=180)

        st.subheader("❓ Quiz Questions")
        st.write(quiz)

        # -----------------------------------------
        # PDF Download
        # -----------------------------------------
        if st.button("Download Notes as PDF"):

            full_content = f"""
SUMMARY:
{summary}

KEY POINTS:
{keypoints}

QUIZ QUESTIONS:
{quiz}
"""

            pdf_file = generate_pdf(full_content)

            with open(pdf_file, "rb") as f:
                st.download_button(
                    "Click Here to Download PDF",
                    f,
                    file_name="Lecture_Notes.pdf"
                )

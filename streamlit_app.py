import streamlit as st
import os
import json
from extract_text import extract_text
from verify_aadhaar import validate_text, load_aadhaar_db, match_with_db

st.set_page_config(page_title="Document Verification", layout="centered")

def homepage():
    st.title("📄 Document Verification System")
    st.markdown("Welcome to the document verification portal.")
    st.markdown("Click **Next** to verify your Aadhaar card.")
    if st.button("Next ➡️"):
        st.session_state.page = "aadhaar"

def aadhaar_page():
    st.title("🔍 Aadhaar Verification")
    uploaded_file = st.file_uploader("Upload Aadhaar image", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        img_path = os.path.join("data", uploaded_file.name)
        with open(img_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.image(img_path, caption="Uploaded Aadhaar", use_column_width=True)

        st.subheader("📄 Extracted Text")
        extracted = extract_text(img_path)
        st.code(extracted)

        st.subheader("✅ Aadhaar Validation")
        result = validate_text(extracted)
        st.json(result)

        if result["valid"]:
            st.subheader("🧾 Matching with Database")
            db = load_aadhaar_db()
            match_result = match_with_db(result, db)
            st.json(match_result)

            if match_result["matched"]:
                st.success("🎉 Aadhaar Verified Successfully!")
            else:
                st.warning("⚠️ Aadhaar Details Not Found in Database.")
        else:
            st.error("❌ Invalid Aadhaar")

    if st.button("⬅️ Back"):
        st.session_state.page = "home"

# Page navigation logic
if "page" not in st.session_state:
    st.session_state.page = "home"

if st.session_state.page == "home":
    homepage()
elif st.session_state.page == "aadhaar":
    aadhaar_page()

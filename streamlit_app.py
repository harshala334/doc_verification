import streamlit as st
import os
import json
from extract_text import extract_text
from verify_aadhaar import validate_text, load_aadhaar_db, match_with_db

st.set_page_config(page_title="Document Verification", layout="centered")

def homepage():
    st.title("📄 Document Verification System")
    st.markdown("Welcome to the document verification portal.")
    st.markdown("Please select the type of document you want to verify and click **Next**.")

    doc_type = st.selectbox("Select Document Type", ["Aadhaar", "PAN", "Voter ID"])
    st.session_state.selected_doc = doc_type  # store selected type

    if st.button("Next ➡️"):
        if doc_type == "Aadhaar":
            st.session_state.page = "aadhaar"
        else:
            st.session_state.page = "coming_soon"

def aadhaar_page():
    st.title("🔍 Aadhaar Verification")

    uploaded_file = st.file_uploader("Upload Aadhaar Image", type=["jpg", "jpeg", "png"])

    if uploaded_file:
        img_path = os.path.join("data", uploaded_file.name)
        with open(img_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.image(img_path, caption="📷 Uploaded Aadhaar", use_column_width=True)

        st.markdown("---")
        st.subheader("📄 Extracted Text")
        extracted = extract_text(img_path)
        st.code(extracted)

        st.markdown("---")
        st.subheader("✅ Aadhaar Validation")
        result = validate_text(extracted)
        st.json(result)

        if result["valid"]:
            st.markdown("---")
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

    st.markdown("---")
    if st.button("⬅️ Back"):
        st.session_state.page = "home"

def coming_soon():
    st.title("🚧 Feature Coming Soon")
    doc_type = st.session_state.get("selected_doc", "Document")
    st.info(f"⚙️ {doc_type} verification is not implemented yet. Stay tuned!")

    if st.button("⬅️ Back"):
        st.session_state.page = "home"

# Navigation logic
if "page" not in st.session_state:
    st.session_state.page = "home"

if st.session_state.page == "home":
    homepage()
elif st.session_state.page == "aadhaar":
    aadhaar_page()
elif st.session_state.page == "coming_soon":
    coming_soon()

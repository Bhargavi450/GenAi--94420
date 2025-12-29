import streamlit as st
import os
import json
import requests
import tempfile

from langchain.embeddings import init_embeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
 
VECTOR_DB_DIR = "chroma_db"
RESUME_DIR = "stored_resumes"
COLLECTION_NAME = "resumes"

os.makedirs(VECTOR_DB_DIR, exist_ok=True)
os.makedirs(RESUME_DIR, exist_ok=True)
 
embed_model = init_embeddings(
    model="nomic-ai/nomic-embed-text-v1.5-GGUF",
    provider="openai",
    base_url="http://10.161.130.59:1234/v1",
    api_key="not-needed",
    check_embedding_ctx_length=False
)
 
vectorstore = Chroma(
    collection_name=COLLECTION_NAME,
    embedding_function=embed_model,
    persist_directory=VECTOR_DB_DIR
)
 
LLM_URL = "http://10.161.130.59:1234/v1/chat/completions"
LLM_MODEL = "google/gemma-3-4b"
 
def load_pdf_resume(uploaded_file):
    file_path = os.path.join(RESUME_DIR, uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    loader = PyPDFLoader(file_path)
    pages = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    documents = []
    for page in pages:
        chunks = splitter.split_text(page.page_content)
        for chunk in chunks:
            documents.append(
                Document(
                    page_content=chunk,
                    metadata={
                        "filename": uploaded_file.name,
                        "file_path": file_path
                    }
                )
            )

    return documents
 
def generate_summary(job_description, resume_text):
    system_prompt = """
You are a strict but fair HR recruiter.

Evaluation Rules:
- Carefully compare the resume with the job description
- Judge suitability based on required skills, relevant experience, education, and role alignment
- Do NOT reject a candidate only because they lack minor or optional skills
- Consider transferable skills, internships, projects, and academic experience for freshers

Response Rules:
- If the candidate is clearly NOT suitable for the role, respond exactly with:
  NOT SUITABLE

- If the candidate meets most core requirements or shows strong potential:
  - Respond with 3 to 5 bullet points
  - Each bullet must clearly state a reason for shortlisting
  - Do NOT add any extra text, headings, or explanations outside the bullets

Tone & Output:
- Be professional, realistic, and unbiased
- Do not be overly strict or overly lenient
- Output only the final decision as per the rules

"""

    payload = {
        "model": LLM_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": f"""
JOB DESCRIPTION:
{job_description[:1500]}

RESUME:
{resume_text[:2500]}
"""
            }
        ]
    }

    try:
        response = requests.post(
            LLM_URL,
            headers={
                "Authorization": "Bearer not-needed",
                "Content-Type": "application/json"
            },
            data=json.dumps(payload),
            timeout=60
        )

        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"].strip()
        else:
            return "NOT SUITABLE"

    except:
        return "NOT SUITABLE"
 
st.set_page_config(page_title="Resume ATS", layout="wide")
st.title("AI Resume Shortlisting System")

with st.sidebar:
    choice = st.selectbox(
        "Menu",
        [
            "Upload Resume",
            "Shortlist Resumes",
            "List All Resumes",
            "Delete Resume"
        ]
    )
 
def upload_resume():
    st.header("Upload Resume")

    file = st.file_uploader("Upload PDF", type=["pdf"])
    if file:
        documents = load_pdf_resume(file)
 
        vectorstore._collection.delete(
            where={"filename": file.name}
        )

        vectorstore.add_documents(documents)
        vectorstore.persist()

        st.success(f"Resume '{file.name}' saved successfully")
 
def shortlist_resumes():
    st.header("Shortlist Resumes")

    job_description = st.text_area("Enter Job Description", height=200)
    top_k = st.slider("Candidates to evaluate", 1, 10, 5)

    if st.button("Start Shortlisting"):
        if not job_description.strip():
            st.warning("Enter job description")
            return

        try:
            results = vectorstore.similarity_search_with_score(
                job_description[:800], k=top_k * 3
            )
        except:
            st.error("Embedding server timeout")
            return

        shortlisted = {}
        SIMILARITY_THRESHOLD = 0.35

        for doc, score in results:
            if score > SIMILARITY_THRESHOLD:
                continue

            filename = doc.metadata["filename"]
            analysis = generate_summary(job_description, doc.page_content)

            if analysis != "NOT SUITABLE":
                shortlisted[filename] = (
                    analysis,
                    doc.metadata["file_path"],
                    score
                )

        if not shortlisted:
            st.error("No candidate is suitable for this role.")
            return

        st.success(f" {len(shortlisted)} candidate(s) shortlisted")

        for i, (fname, data) in enumerate(shortlisted.items(), 1):
            reason, path, score = data
            match = round((1 - score) * 100, 2)

            st.markdown(f"### {i}. {fname}")
            st.write(f"Match Score: {match}%")
            st.markdown(reason)

            with open(path, "rb") as f:
                st.download_button(
                    "Download Resume",
                    f,
                    file_name=fname,
                    mime="application/pdf"
                )
 
def list_resumes():
    st.header("All Uploaded Resumes")

    data = vectorstore.get(include=["metadatas"])
    if not data or not data.get("metadatas"):
        st.info("No resumes uploaded")
        return

    filenames = sorted(set(m["filename"] for m in data["metadatas"]))

    for i, name in enumerate(filenames, 1):
        st.write(f"{i}. {name}")

# ================= DELETE =================
def delete_resume():
    st.header("Delete Resume")

    data = vectorstore.get(include=["metadatas"])
    if not data or not data.get("metadatas"):
        st.info("No resumes to delete")
        return

    filenames = sorted(set(m["filename"] for m in data["metadatas"]))
    selected = st.selectbox("Select resume", filenames)

    if st.button("Delete"):
        vectorstore._collection.delete(where={"filename": selected})
        vectorstore.persist()

        path = os.path.join(RESUME_DIR, selected)
        if os.path.exists(path):
            os.remove(path)

        st.success("Resume deleted successfully")

# ================= ROUTING =================
if choice == "Upload Resume":
    upload_resume()
elif choice == "Shortlist Resumes":
    shortlist_resumes()
elif choice == "List All Resumes":
    list_resumes()
elif choice == "Delete Resume":
    delete_resume()

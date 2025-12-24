import streamlit as st
import tempfile
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.embeddings import init_embeddings
from langchain_community.vectorstores import Chroma

st.set_page_config(page_title="Resume Shortlisting", layout="wide")

VECTOR_DB_DIR = "chroma_db"
COLLECTION_NAME = "resumes"

embed_model = init_embeddings(
    model="text-embedding-3-small",
    provider="openai",
    base_url="http://192.168.52.59:1234/v1",
    api_key="not-needed",
    check_embedding_ctx_length=False
)
   
vectorstore = Chroma(
    collection_name=COLLECTION_NAME,
    embedding_function=embed_model,
    persist_directory=VECTOR_DB_DIR
)
 
def load_pdf_resume(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        temp_path = tmp.name

    loader = PyPDFLoader(temp_path)
    docs = loader.load()

    resume_text = ""
    for page in docs:
        resume_text += page.page_content

    metadata = {
        "filename": uploaded_file.name,
        "page_count": len(docs)
    }

    return resume_text, metadata

 
st.title("Resume Management & Shortlisting System")

tab1, tab2 = st.tabs(["Resume Upload", "Resume Shortlisting"])

 
with tab1:
    st.header("Upload Resume (PDF)")

    uploaded_file = st.file_uploader("Choose Resume PDF", type=["pdf"])

    if uploaded_file is not None:
        resume_text, resume_info = load_pdf_resume(uploaded_file)

        st.write("Resume Metadata")
        st.json(resume_info)

        if st.button("Store / Update Resume"):
           
            vectorstore._collection.delete(
                where={"filename": resume_info["filename"]}
            )

            vectorstore.add_texts(
                texts=[resume_text],
                metadatas=[resume_info]
            )

            vectorstore.persist()
            st.success("Resume stored successfully in Chroma Vector DB")
 
with tab2:
    st.header("Resume Shortlisting")

    job_description = st.text_area(
        "Enter Job Description",
        height=200,
        placeholder="Example: Looking for a Python developer with ML, SQL, and data analysis experience"
    )

    top_k = st.slider("Number of resumes to shortlist", 1, 10, 5)

    if st.button("Shortlist Resumes"):
        if not job_description.strip():
            st.warning("Please enter a job description")
        else:
            results = vectorstore.similarity_search_with_score(
                job_description,
                k=top_k
            )

            if not results:
                st.error("No resumes found in database")
            else:
                st.subheader("Shortlisted Resumes")

                for idx, (doc, score) in enumerate(results, start=1):
                    match_percent = round((1 - score) * 100, 2)

                    st.markdown(f"""
                    ### {idx}. {doc.metadata.get("filename", "Unknown")}
                    - **Pages**: {doc.metadata.get("page_count")}
                    - **Match Score**: {match_percent} %
                    """)

                    with st.expander("View Resume Text"):
                        st.write(doc.page_content[:2000])

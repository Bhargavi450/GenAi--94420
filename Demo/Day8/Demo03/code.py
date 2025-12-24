from langchain_community.document_loaders import PyPDFLoader
from langchain.embeddings import init_embeddings

embed_model=init_embeddings(
    model="nomic-ai/nomic-embed-text-v1.5-GGUF",
    provider="openai",
    base_url="http://10.161.130.59:1234/v1",
    api_key="not-needed",
    check_embedding_ctx_length=False
)

def load_pdf_resume(pdf_path):
    loader=PyPDFLoader(pdf_path)
    docs=loader.load()
    resume_content=" "
    for page in docs:
        resume_content+=page.page_content
    metadata={
        "source":pdf_path,
        "page_count":len(docs)
    }
    return resume_content,metadata

resume_path="C:/Users/Bhargavi/Downloads/Rohit_CV.pdf"
resume_text,resume_info=load_pdf_resume(resume_path)
print(resume_info)
print(resume_text)

resume_embeddings=embed_model.embed_documents([resume_text])
for embedding in resume_embeddings:
    print(f"Len = {len(embedding)}-->{embedding[:4]}")
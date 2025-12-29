from langchain.chat_models import init_chat_model
from langchain.embeddings import init_embeddings

llm=init_chat_model(
    model="google/gemma-3-4b",
    model_provider="openai",
    base_url="http://10.161.130.59:1234/v1",
    api_key="not-needed"
)
embeddings_model=init_embeddings(
    model="nomic-ai/nomic-embed-text-v1.5-GGUF",
    provider="openai",
    base_url="http://10.161.130.59:1234/v1",
    api_key="not-needed",
    check_embedding_ctx_length=False
)
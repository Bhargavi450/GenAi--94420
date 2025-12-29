import chromadb
from langchain.tools import tool
from agent import embeddings_model

DB_PATH = "./chroma_db"
COLLECTION_NAME = "mycollection"


@tool
def chroma_retrieval(query_text: str) -> str:
    """
    Retrieve relevant content from the currently indexed PDF.
    """

    client = chromadb.PersistentClient(path=DB_PATH)

    try:
        collection = client.get_collection(COLLECTION_NAME)
    except Exception:
        return "No document is currently indexed."

    if collection.count() == 0:
        return "No document is currently indexed."

    query_embedding = embeddings_model.embed_query(query_text)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    documents = results.get("documents", [[]])[0]

    if not documents:
        return "No relevant information found."

    return "\n\n".join(documents)

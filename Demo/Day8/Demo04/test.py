import chromadb
 
client = chromadb.Client(
    settings=chromadb.Settings(
        persist_directory="./knowledge_base"
    )
)
 
collection = client.get_or_create_collection(
    name="resumes"
)
 
collection.add(
    ids=["resume1"],
    documents=["Bhargavi is an AI & DS student skilled in Python and Java"],
    metadatas=[{"type": "resume"}]
)
 
results = collection.query(
    query_texts=["AI student with Python"],
    n_results=1
)

print(results)

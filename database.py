import chromadb
from chromadb.utils import embedding_functions

# 로컬 저장소 초기화
client = chromadb.PersistentClient(path="./chroma_db")
embedding_func = embedding_functions.DefaultEmbeddingFunction()

collection = client.get_or_create_collection(
    name="restaurant_data",
    embedding_function=embedding_func
)

def add_restaurant(id, name, menu, description):
    collection.add(
        ids=[id],
        documents=[f"{name} - {menu}: {description}"],
        metadatas=[{"name": name, "menu": menu}]
    )

import os
import chromadb
from langchain_core.tools import tool
from chromadb.utils import embedding_functions

class RestaurantDB:
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(base_dir, "chroma_db")
        self.client = chromadb.PersistentClient(path=self.db_path)
        api_key = os.environ.get("GOOGLE_API_KEY")
        
        embedding_func = embedding_functions.GoogleGenerativeAiEmbeddingFunction(
            api_key=api_key,
            model_name="models/gemini-embedding-001"
        )
        
        self.collection = self.client.get_or_create_collection(
            name="suwon_restaurants",
            embedding_function=embedding_func
        )


@tool
def search_restaurant_tool(query: str):
    """사용자가 찾는 맛집 데이터를 검색하는 도구입니다."""
    db = RestaurantDB()
    results = db.collection.query(query_texts=[query], n_results=3)
    return str(results["documents"][0])


if __name__ == "__main__":
    db = RestaurantDB()
    # 전체 데이터가 몇 개인지 확인
    print(f"현재 DB에 저장된 맛집 개수: {db.collection.count()}")
    # 샘플 조회
    print(db.collection.peek())
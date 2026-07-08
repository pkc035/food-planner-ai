import requests
import time
import os
from db.loader import RestaurantDB

class RestaurantCrawler:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://openapi.gg.go.kr/PlaceThatDoATasteyFoodSt"

    def fetch_restaurant_data(self):
        """경기도 맛집 API를 호출하여 데이터를 수집"""
        params = {
            "KEY": self.api_key,
            "Type": "json",
            "pSize": 100  # 한 번에 가져올 데이터 개수
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status() # 오류 발생 시 예외 처리
            data = response.json()
            
            # API 응답 구조 파싱
            # 데이터가 있는 경로 확인
            rows = data['PlaceThatDoATasteyFoodSt'][1]['row']
            
            processed_data = []
            for row in rows:
                # 에이전트가 이해하기 쉬운 문장 형태로 가공
                text = f"식당명: {row['RESTRT_NM']}, 대표메뉴: {row['REPRSNT_FOOD_NM']}, 주소: {row['REFINE_LOTNO_ADDR']}"
                processed_data.append({
                    "text": text,
                    "id": f"gg_{row['SIGUN_CD']}_{row['RESTRT_NM']}"
                })
            return processed_data

        except Exception as e:
            print(f"❌ 데이터 수집 에러: {e}")
            return []

    def save_to_db(self):
        data = self.fetch_restaurant_data()
        if not data:
            print("저장할 데이터가 없습니다.")
            return

        db = RestaurantDB()
        
        # 20개씩 쪼개서 저장 (Batch Processing)
        batch_size = 20
        for i in range(0, len(data), batch_size):
            batch = data[i : i + batch_size]
            documents = [item['text'] for item in batch]
            ids = [item['id'] for item in batch]
            
            try:
                db.collection.add(documents=documents, ids=ids)
                print(f"✅ {i + len(batch)}/{len(data)}개 데이터 적재 중...")
                time.sleep(10)
            except Exception as e:
                print(f"❌ 배치 저장 중 에러: {e}")
                time.sleep(10)
                break

if __name__ == "__main__":
    api_key = os.environ.get("GG_API_KEY")
    crawler = RestaurantCrawler(api_key)
    crawler.save_to_db()
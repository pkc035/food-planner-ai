import requests
from bs4 import BeautifulSoup

class RestaurantCrawler:
    def __init__(self, base_url):
        self.base_url = base_url

    def fetch_restaurant_data(self):
        """특정 웹페이지에서 데이터를 수집"""
        try:
            return []
        except Exception as e:
            print(f"❌ 크롤링 에러: {e}")
            return []
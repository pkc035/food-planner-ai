from langchain.tools import tool

@tool
def get_current_weather(location: str):
    """현재 날씨 정보를 가져오는 도구입니다. 날씨가 궁금할 때 사용하세요."""
    # 실제로는 OpenWeatherMap API 등을 호출
    return f"{location}의 현재 날씨는 흐리고 비가 옵니다. 따뜻한 국물이 당기는 날씨네요!"
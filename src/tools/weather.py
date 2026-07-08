import os
import requests
from datetime import datetime
from langchain.tools import tool
from utils.converter import lat_lon_to_grid


def _get_current_weather(location: list):
    """사용자의 위치 좌표 [lat, lon]을 입력받아 상세 날씨를 가져옵니다."""
    
    if not isinstance(location, list) or len(location) < 2:
        return "좌표 형식이 올바르지 않습니다. [위도, 경도] 형식으로 전달해주세요."

    lat, lon = float(location[0]), float(location[1])
    nx, ny = lat_lon_to_grid(lat, lon)
    
    service_key = os.environ.get("KMA_SERVICE_KEY")
    now = datetime.now()
    base_date = now.strftime("%Y%m%d")
    base_time = now.strftime("%H00") 

    # 기상청 초단기실황 조회 API 주소 (정확한 엔드포인트 확인 필요)
    base_url = "https://apihub.kma.go.kr/api/typ02/openApi/VilageFcstInfoService_2.0/getUltraSrtFcst"

    params = {
        "authKey": os.environ.get("KMA_SERVICE_KEY"), # serviceKey가 아니라 authKey로 변경
        "numOfRows": "100",
        "pageNo": "1",
        "dataType": "JSON", # API HUB는 XML/JSON 지원 여부 확인 필수
        "base_date": base_date,
        "base_time": base_time,
        "nx": int(nx),
        "ny": int(ny)
    }
    
    try:
        response = requests.get(base_url, params=params)

        # 1. 상태 코드 확인
        if response.status_code != 200:
            return f"API 서버 응답 실패: {response.status_code}"

        # 2. JSON 파싱 전 텍스트 확인
        data = response.json()
        
        # 3. 응답 구조 검증 (에러 메시지 처리)
        if "response" not in data or "body" not in data["response"]:
            return f"API 응답 데이터 구조 오류: {data}"
        
        items = data['response']['body']['items']['item']
        
        # 데이터를 category별로 우선 저장
        weather_data = {}
        for item in items:
            # PTY: 강수형태, T1H: 기온(실황), T3H: 기온(예보), REH: 습도 등
            # 여러 시간대의 데이터가 섞여 올 수 있으므로 가장 최근 것 혹은 첫 번째 것을 사용
            if item['category'] not in weather_data:
                weather_data[item['category']] = item['fcstValue']
                
        # T1H가 없으면 T3H(3시간 기온)를 찾는 등 예외 처리 보강
        temp = weather_data.get('T1H') or weather_data.get('T3H') or "정보없음"
        humidity = weather_data.get('REH', '정보없음')
        pty = weather_data.get('PTY', '0')

        pty_map = {"0": "없음", "1": "비", "2": "비/눈", "3": "눈", "5": "빗방울", "6": "빗방울눈날림", "7": "눈날림"}
        pty_desc = pty_map.get(pty, "알 수 없음")
            
        return f"현재 날씨: 기온 {temp}도, 습도 {humidity}%, 강수형태 {pty_desc}."
        
    except Exception as e:
        # 에러 발생 시 response.text를 출력하여 원인 파악
        return f"날씨 정보 조회 오류: {str(e)}"

@tool
def get_current_weather(location: list):
    """
    사용자의 위도와 경도를 입력받아 현재 날씨를 조회합니다. 
    입력값은 [위도, 경도] 형식의 리스트여야 합니다.
    """
    return _get_current_weather(location)
    

if __name__ == "__main__":
    test_loc = [37.2456, 127.0621]
    # @tool을 거치지 않고 직접 로직 함수 실행
    print(_get_current_weather(test_loc))
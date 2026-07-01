# 파이썬 3.11 슬림 버전 사용
FROM python:3.11-slim

# 작업 디렉토리 설정
WORKDIR /app

# 의존성 파일 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스코드 복사
COPY . .

# 스트림릿 실행 포트 오픈
EXPOSE 8501

# Streamlit 실행
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
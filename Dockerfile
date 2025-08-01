FROM python:3.11-slim

# 시스템 의존성 설치
RUN apt-get update && apt-get install -y \
    xvfb \
    x11vnc \
    xserver-xorg \
    xauth \
    x11-utils \
    x11-xserver-utils \
    novnc \
    websockify \
    libnss3 \
    libatk-bridge2.0-0 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libxss1 \
    libasound2 \
    libatspi2.0-0 \
    libgtk-3-0 \
    && rm -rf /var/lib/apt/lists/*

# 작업 디렉토리 설정
WORKDIR /app

# Python 의존성 설치
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN playwright install chromium --with-deps

# 애플리케이션 파일 복사
COPY . .

# 스크립트 실행 권한 부여
RUN chmod +x script/start.sh

# 포트 노출
EXPOSE 5900 6080

# 환경변수 설정
ENV DISPLAY=:99
ENV PYTHONUNBUFFERED=1

# 컨테이너 시작 스크립트 실행
CMD ["./script/start.sh"]

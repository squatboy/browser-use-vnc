FROM python:3.11-slim

WORKDIR /app

# Chromium 런타임/폰트(DejaVu로 대체), 유틸 설치
RUN apt-get update && apt-get install -y --no-install-recommends \
    libnss3 libatk-bridge2.0-0 libdrm2 libxkbcommon0 libxcomposite1 \
    libxdamage1 libxrandr2 libgbm1 libxss1 libasound2 libatspi2.0-0 \
    libgtk-3-0 libu2f-udev libvulkan1 libxshmfence1 libxkbfile1 \
    fonts-liberation fonts-unifont fonts-dejavu fonts-noto-color-emoji \
    xdg-utils ca-certificates curl wget && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir playwright

# 브라우저만 설치 (–with-deps 사용하지 않음)
RUN python -m playwright install chromium

COPY flight.py .

ENV DISPLAY=:99

CMD ["python", "flight.py"]
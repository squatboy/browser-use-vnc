#!/bin/bash

# 환경변수 설정
export DISPLAY=:99

# 가상 디스플레이 시작
Xvfb :99 -screen 0 1280x720x24 -ac +extension GLX +render -noreset &

# VNC 서버 시작
x11vnc -display :99 -nopw -forever -shared -rfbport 5900 &

# noVNC 웹 서버 시작
websockify --web=/usr/share/novnc/ 6080 localhost:5900 &

# 서비스들이 시작될 때까지 대기
sleep 3

# 디스플레이 테스트
echo "🔍 Testing display..."
xwininfo -root -display :99

# DISPLAY 환경변수 확인
echo "📺 DISPLAY is set to: $DISPLAY"

# agent.py 실행
echo "🚀 Starting browser-use agent..."
python browser-use-agent.py

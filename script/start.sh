#!/bin/bash

# 환경변수 설정
export DISPLAY=:99
echo "📺 Setting DISPLAY=$DISPLAY"

# 가상 디스플레이 시작
echo "🖥️ Starting Xvfb..."
Xvfb :99 -screen 0 1280x720x24 -ac +extension GLX +render -noreset &
XVFB_PID=$!

# Xvfb가 시작될 때까지 대기
sleep 2

# 디스플레이 확인
echo "🔍 Testing display..."
if xwininfo -root -display :99 > /dev/null 2>&1; then
    echo "✅ Display :99 is ready"
else
    echo "❌ Display :99 is not ready"
    exit 1
fi

# VNC 서버 시작
echo "📡 Starting x11vnc..."
x11vnc -display :99 -nopw -forever -shared -rfbport 5900 &
VNC_PID=$!

# noVNC 웹 서버 시작
echo "🌐 Starting websockify..."
websockify --web=/usr/share/novnc/ 6080 localhost:5900 &
WEBSOCKIFY_PID=$!

# 모든 서비스가 시작될 때까지 대기
sleep 3

# 포트 확인
echo "� Checking services..."
netstat -tlnp | grep -E "(5900|6080)" || echo "⚠️ Ports not ready yet"

# 환경변수 최종 확인
echo "📺 Final DISPLAY check: $DISPLAY"

# agent.py 실행
echo "🚀 Starting browser-use agent..."
python browser-use-agent.py

# 정리 함수
cleanup() {
    echo "🧹 Cleaning up..."
    kill $XVFB_PID $VNC_PID $WEBSOCKIFY_PID 2>/dev/null
    exit
}

# 시그널 처리
trap cleanup SIGTERM SIGINT

# 무한 대기 (컨테이너가 종료되지 않도록)
wait

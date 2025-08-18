#!/bin/bash

# 환경변수 설정
export DISPLAY=:99
echo "📺 Setting DISPLAY=$DISPLAY"

# 기존 Xvfb 가상 디스플레이 시작 전에 잠금 파일 삭제
if [ -e /tmp/.X99-lock ]; then
  echo "🧹 Removing stale X11 lock file /tmp/.X99-lock"
  rm -f /tmp/.X99-lock
fi

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

#############################################
# VNC 서버 시작 (TigerVNC: x0vncserver)
#############################################
echo "🐯 Starting TigerVNC (x0vncserver) without password..."

VNC_AUTH_ARGS="-SecurityTypes None"

# x0vncserver 는 Xvfb(:99) 위의 x11 화면을 VNC로 노출
# -NeverShared: 단일 클라이언트, -AlwaysShared: 다중 접속 허용. 여기서는 shared 사용
# -localhost=0: 외부 접속 허용
x0vncserver \
    -display :99 \
    -rfbport 5900 \
    -AlwaysShared=1 \
    -localhost=0 \
    -IdleTimeout=0 \
    $VNC_AUTH_ARGS &
VNC_PID=$!

# noVNC 웹 서버 시작
echo "🌐 Starting websockify..."
websockify --web=/usr/share/novnc/ --log-file=/dev/null 6080 localhost:5900 &
WEBSOCKIFY_PID=$!

# 모든 서비스가 시작될 때까지 대기
sleep 3

# 포트 확인 (TigerVNC 포함)
echo "🔧 Checking services..."
netstat -tlnp | grep -E "(5900|6080)" || echo "⚠️ Ports not ready yet"

# TigerVNC 프로세스 가동 확인
if ! kill -0 $VNC_PID 2>/dev/null; then
    echo "❌ TigerVNC (x0vncserver) failed to start"
    exit 1
fi

# 환경변수 최종 확인
echo "📺 Final DISPLAY check: $DISPLAY"

# VNC 서비스가 준비되었음을 알림
echo "✅ VNC services are ready!"
echo "🌐 Access via: http://your-server-ip:6080/vnc.html"
echo "📍 Python scripts can now be executed manually"

# 정리 함수
cleanup() {
    echo "🧹 Cleaning up..."
    kill $XVFB_PID $VNC_PID $WEBSOCKIFY_PID 2>/dev/null
    exit
}

# 시그널 처리
trap cleanup SIGTERM SIGINT

# 간단한 대기 - 컨테이너를 유지하기 위해
echo "🔄 VNC services running. Container will stay alive..."
echo "💡 To stop: docker compose down"

# wait 명령으로 백그라운드 프로세스들을 기다림 (훨씬 효율적)
wait $XVFB_PID $VNC_PID $WEBSOCKIFY_PID
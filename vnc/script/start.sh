#!/bin/bash
set -euo pipefail

echo "START_SH_VERSION=2025-08-23_17-00_KST"

NOVNC_PORT="${NOVNC_PORT:-6080}"

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

# VNC 서버 시작
echo "📡 Starting x11vnc..."
x11vnc -display :99 -nopw -forever -shared -rfbport 5900 -localhost -quiet -o /var/log/x11vnc.log &
VNC_PID=$!

# x11vnc가 5900 리스닝 확인 루프
for i in {1..20}; do
  if netstat -tln | grep -q ":5900 "; then break; fi
  sleep 0.2
done
if ! netstat -tln | grep -q ":5900 "; then
  echo "❌ x11vnc failed to listen on 5900. Recent log:"
  tail -n 100 /var/log/x11vnc.log || true
  exit 1
fi

sleep 2

# noVNC 웹 서버 시작
echo "🌐 Starting websockify..."
# 내부는 6080 고정, x11vnc는 5900 고정
websockify --web=/usr/share/novnc/ --log-file=/dev/null 6080 localhost:5900 &
WEBSOCKIFY_PID=$!

# 6080 리스닝 확인 루프
for i in {1..20}; do
  if netstat -tln | grep -q ":6080 "; then break; fi
  sleep 0.2
done
if ! netstat -tln | grep -q ":6080 "; then
  echo "❌ websockify failed to listen on 6080"
  exit 1
fi


# 포트 확인
echo "🔧 Checking services..."
# 내부 포트 기준으로 확인
netstat -tlnp | grep -E "(5900|6080)" || echo "⚠️ Ports not ready yet"


# 환경변수 최종 확인
echo "📺 Final DISPLAY check: $DISPLAY"

# VNC 서비스가 준비되었음을 알림
echo "✅ VNC services are ready!"
echo "🌐 Access via: http://<host>:${NOVNC_PORT}/vnc.html"
echo "📍 Python scripts can now be executed manually"

# 정리 함수
cleanup() {
    echo "🧹 Cleaning up..."
    kill $XVFB_PID $VNC_PID $WEBSOCKIFY_PID 2>/dev/null
    exit
}

# 시그널 처리
trap cleanup SIGTERM SIGINT EXIT

# 간단한 대기 - 컨테이너를 유지하기 위해
echo "🔄 VNC services running. Container will stay alive..."
echo "💡 To stop: docker compose down"

# wait 명령으로 백그라운드 프로세스들을 기다림 (훨씬 효율적)
wait $XVFB_PID $VNC_PID $WEBSOCKIFY_PID
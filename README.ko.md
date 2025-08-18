# Browser-Use VNC Web View
VNC/noVNC를 통해 실시간 가상 모니터 시스템을 제공하는 Docker 컨테이너입니다.  
이 시스템은 두 개의 컨테이너로 구성되어 있습니다:  
- **vnc 컨테이너**: 가상 디스플레이 및 VNC 서버를 제공합니다.  
- **agent 컨테이너**: 예를 들어 `flight.py`와 같은 애플리케이션을 실행하며, `.env` 파일을 `agent` 디렉토리 내에 두고 `env_file`로 참조합니다.  

외부에서 실행되는 애플리케이션은 `DISPLAY=:99` 환경으로 실행되어 가상 모니터 화면에서 확인할 수 있습니다.

## 화면 출력 플로우
<img width="996" height="933" alt="noVNC-arch" src="https://github.com/user-attachments/assets/33de6c7a-f74b-4330-85f1-72ee5840e53c" />

## 데모 영상

https://github.com/user-attachments/assets/5fd999db-980d-4e34-ae8a-dd1c2dd2567a


## 빠른 시작

## 요구사항
- Docker & Docker Compose
- git

### 1. 저장소 클론
```bash
git clone https://github.com/squatboy/browser-use-vnc.git
cd browser-use-vnc/
```

### 2. VNC 및 Agent 서비스 시작
```bash
cd vnc/
docker-compose up -d --build
```

### 3. 실시간 모니터링 및 로그 확인
- **noVNC**: http://서버IP:6080/vnc.html
- 외부에서 실행되는 애플리케이션(e.g., browser-use, Chromium 등)은 `DISPLAY=:99` 환경으로 실행되며 이 화면에서 실시간으로 확인할 수 있습니다.
- `flight.py` 등 agent 컨테이너에서 실행되는 애플리케이션 로그는 다음 명령어로 확인 가능합니다:
```bash
docker logs agent
```

### Security Group 설정 (서버 호스트에서 실행 시)
인바운드 허용 포트:
- 포트 5900 (VNC)
- 포트 6080 (noVNC)

## 시스템 구조

- **vnc 컨테이너**  
  - Xvfb: 가상 디스플레이 서버 (:99)  
  - x11vnc: VNC 서버 (포트 5900)  
  - websockify: VNC를 WebSocket으로 변환 (포트 6080)  

- **agent 컨테이너**  
  - browser-use 또는 기타 애플리케이션 실행 (예: flight.py)  
  - `.env` 파일은 `agent` 디렉토리에 위치하며, `docker-compose.yml`에서 `env_file`로 참조  

## 커스터마이징
이 시스템은 VNC/noVNC를 제공하는 `vnc` 컨테이너와, 실제 애플리케이션을 실행하는 `agent` 컨테이너로 분리되어 있습니다.  
외부에서 실행하는 애플리케이션(browser-use, Chromium 등)은 `DISPLAY=:99` 환경으로 실행하면 가상 모니터에서 확인할 수 있습니다.

## 오류 시 확인사항

- **Chrome 실행 실패**: 컨테이너 재시작 `docker-compose restart`
- **VNC 연결 실패**: 보안 그룹 포트 확인

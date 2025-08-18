# Browser-Use VNC Web View
VNC/noVNC를 통해 실시간 가상 모니터 시스템을 제공하는 Docker 컨테이너입니다.  
이 컨테이너 자체에는 browser-use나 Python 코드가 포함되지 않으며, 외부에서 실행되는 애플리케이션을 DISPLAY=:99 환경으로 띄우면 화면을 확인할 수 있습니다.

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
cd browser-use-vnc
```

### 2. VNC 서비스 시작
```bash
docker-compose up -d --build
```

### 3. 실시간 모니터링
- **noVNC**: http://서버IP:6080/vnc.html
- 외부에서 실행되는 애플리케이션(e.g., browser-use, Chromium 등)이 DISPLAY=:99 환경으로 실행되면 이 화면에서 실시간으로 확인할 수 있습니다

## 서버 호스트에서 실행

### Security Group 설정
Security Group에서 인바운드 허용 포트:
- 포트 5900 (VNC)
- 포트 6080 (noVNC)

## 시스템 구조

- **Xvfb**: 가상 디스플레이 서버 (:99)
- **TigerVNC (x0vncserver)**: VNC 서버 (포트 5900)
- **websockify**: VNC를 WebSocket으로 변환 (포트 6080)

## 커스터마이징
이 컨테이너는 VNC/noVNC 시스템만 제공합니다.  
외부에서 실행하는 애플리케이션(browser-use, Chromium 등)을 DISPLAY=:99 환경으로 실행하면 가상 모니터에서 확인할 수 있습니다.

## 오류 시 확인사항

- **Chrome 실행 실패**: 컨테이너 재시작 `docker-compose restart`
- **VNC 연결 실패**: 보안 그룹 포트 확인

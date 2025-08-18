# Browser-Use VNC Web View
VNC/noVNC를 통해 실시간 가상 모니터 시스템을 제공하는 Docker 컨테이너입니다.  
이 시스템은 두 개의 컨테이너로 구성되어 있습니다:  
- **vnc 컨테이너**: 가상 디스플레이 및 VNC 서버를 제공합니다.  
- **agent 컨테이너**: 예를 들어 `flight.py`와 같은 애플리케이션을 실행하며, `.env` 파일과 agent 스크립트를 `agent` 디렉토리에 두고 `env_file`로 자동 로드합니다.  

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

### 2. `.env` 파일 및 agent 스크립트 준비
- `.env`: Browser-Use에 사용될 LLM API KEY 작성
- `browser-use` 에이전트 스크립트 파일: `flight.py`

> `docker-compose.yml`에서 `env_file`로 `.env`를 자동 로드하며, agent 스크립트도 이 컨테이너 내에서 실행됩니다.

### 3. VNC 및 Agent 서비스 시작
```bash
cd vnc/
docker-compose up -d --build
```

### 4. 실시간 모니터링 및 로그 확인
- **noVNC**: http://서버IP:6080/vnc.html

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
  - vnc 컨테이너와 X11 소켓을 공유하여 가상 디스플레이에 접근  


### Browser-use BrowserSession Settings

```python
browser_session = BrowserSession(
    headless=False,
    args=[
        "--no-sandbox",           # Docker root 권한 환경에서 브라우저 샌드박스가 충돌하므로 비활성화 필요
        "--disable-dev-shm-usage" # 컨테이너의 /dev/shm(공유 메모리)가 작아 발생하는 크래시/메모리 부족 문제를 피하기 위해
    ],
)
```

## 커스터마이징
이 시스템은 VNC/noVNC를 제공하는 `vnc` 컨테이너와, 실제 애플리케이션을 실행하는 `agent` 컨테이너로 분리되어 있습니다.  
외부에서 실행하는 애플리케이션(browser-use, Chromium 등)은 `DISPLAY=:99` 환경으로 실행하면 가상 모니터에서 확인할 수 있습니다.

## Use-Case: 웹사이트 내 noVNC 세션 임베딩
웹사이트에 noVNC 접속 화면을 iframe으로 삽입할 수 있습니다.  
예를 들어, 다음과 같이 HTML에 추가하세요:

```html
<iframe
    src="http://Server-IP:6080/vnc.html?autoconnect=true"
    width="1280" height="720">
</iframe>
```


## 오류 시 확인사항

- **Chrome 실행 실패**: 컨테이너 재시작 `docker-compose restart`
- **VNC 연결 실패**: 보안 그룹 포트 확인

# Browser-Use noVNC Web View

VNC/noVNC를 사용하여 실시간 웹 주소 접근 기반 가상 모니터를 제공하는 Docker 기반 시스템으로, **vnc**와 **agent** 두 개의 컨테이너로 구성되어 있습니다. `vnc` 컨테이너는 가상 디스플레이 서버와 VNC 서비스를 실행하고, `agent` 컨테이너는 `agent.py`와 같은 브라우저 자동화 스크립트를 실행합니다. 두 컨테이너는 공유된 X11 UNIX 소켓 볼륨을 통해 통신하며, 세션을 격리하고 보안을 보장합니다.


## 시스템 아키텍처 & 워크플로우

각 VNC/agent 세션 쌍은 Docker 네임스페이스와 고유한 X11 소켓 볼륨을 사용하여 격리되어 실행됩니다. 이러한 설계는 세션 간의 디스플레이 데이터가 안전하게 분리되도록 보장합니다.

### vnc 컨테이너

- **Xvfb**: 가상 디스플레이 서버 (예: :99)
- **x11vnc**: VNC 서버
- **websockify**: VNC를 WebSocket으로 변환하여 noVNC 접근 제공

### agent 컨테이너

- Browser-use Python 스크립트 실행 (예: `agent.py`)
- `vnc` 컨테이너와 X11 소켓 볼륨을 공유하여 가상 디스플레이에 출력 렌더링


## 시작하기

### 요구사항

- Docker & Docker Compose
- git
- Python 3.8 이상

### 1. 저장소 클론

```bash
git clone https://github.com/squatboy/browser-use-vnc.git
cd browser-use-vnc/
```

### 2. Agent 파일 준비

다음 파일들을 `agent/` 디렉토리에 배치합니다:

- `.env`: browser-use용 LLM API 키 및 기타 환경 변수
- `agent.py`: browser-use agent 스크립트

> 이 파일들은 Docker Compose에 의해 자동으로 로드되어 agent 컨테이너를 구성하고 실행합니다.
> 

### 3. FastAPI Orchestrator 실행

세션 생성을 관리하는 오케스트레이터 서비스를 시작합니다:

```bash
uvicorn app_orchestrator:app --host 0.0.0.0 --port 8000
```

### 4. 새 세션 생성

POST 요청을 보내 새로운 VNC/agent 세션을 생성합니다:

```
POST http://<Server-IP>:8000/sessions
```

응답에는 세션 ID와 동적으로 할당된 noVNC 포트가 포함됩니다:

```json
{
  "session_id": "session123",
  "novnc_port": 6081,
  "url": "http://<Server-IP>:6081/vnc.html"
}
```

### 5. 세션 접속

제공된 URL을 웹 브라우저에서 열어 noVNC를 통해 가상 모니터에 접속합니다.

## 멀티 세션 수동 테스트 예시

오케스트레이션을 통해 사용하지 않고 직접 다른 `SESSION_ID`와 `NOVNC_PORT` 환경 변수를 지정하고 별도의 Docker Compose 프로젝트를 실행하여 여러 독립 세션을 수동으로 생성할 수 있습니다.

```bash
# 첫 번째 세션
cd vnc/
SESSION_ID=session1 NOVNC_PORT=6081 docker compose -p vnc1 up -d --build

# 두 번째 세션
SESSION_ID=session2 NOVNC_PORT=6082 docker compose -p vnc2 up -d --build
```

그런 다음 세션에 각각 접속합니다:

- http://:6081/vnc.html
- http://:6082/vnc.html

각 세션은 고유한 X11 소켓 볼륨을 사용하므로 세션 간 데이터 누출 없이 격리됩니다.


## 보안 그룹 & 네트워크 설정

공용 서버에 배포할 경우, 세션에 필요한 noVNC 포트만 열어두세요 (예: 6080, 6081, 6082, ...). 필요에 따라 접근을 제한하는 것이 중요합니다.


## BrowserSession Python 설정 예시

Agent 컨테이너 내에서 브라우저를 실행할 때, 다음 설정을 사용하여 Docker 관련 일반적인 문제를 피하세요:

```python
browser_session = BrowserSession(
    headless=False,
    args=[
        "--no-sandbox",            # Docker에서 root로 실행할 때 필요
        "--disable-dev-shm-usage"  # 제한된 컨테이너 환경에서 /dev/shm 크래시 방지
    ],
)
```


## 커스터마이징 & 고급 사용법

- 시스템은 `vnc` 컨테이너(가상 디스플레이 및 VNC 서비스)와 `agent` 컨테이너(브라우저 자동화 스크립트)를 분리합니다.
- 자동화 워크플로우에 맞게 agent 스크립트(`agent.py`)를 확장하거나 수정할 수 있습니다.
- agent 컨테이너는 `vnc` 컨테이너가 관리하는 가상 디스플레이에 브라우저 출력을 렌더링하기 위해 공유된 X11 소켓 볼륨에 연결됩니다.


## 사용 사례: 웹사이트 내 VNC 데스크탑 임베딩

noVNC 웹 클라이언트를 iframe에 삽입하여 원격 데스크탑을 웹 애플리케이션에 직접 통합할 수 있습니다:

```html
<iframe
    src="http://<Server-IP>:6080/vnc.html?autoconnect=true"
    width="1280" height="720">
</iframe>
```


## 문제 해결 & 팁

- **Chrome 실행 실패**: `docker compose restart`로 컨테이너를 재시작하세요.
- **VNC 연결 실패**: 방화벽이나 보안 그룹에서 noVNC 포트의 인바운드 트래픽 허용 여부를 확인하세요.


## 추가 참고 사항

- 각 세션은 Docker 네임스페이스와 고유한 X11 소켓 볼륨을 통해 격리됩니다.
- `agent`와 `vnc` 컨테이너 간의 통신은 네트워크가 아닌 X11 UNIX 소켓을 통해서만 이루어집니다.
- 사용 사례에 맞게 agent 측 스크립트와 종속성을 자유롭게 추가하거나 수정할 수 있습니다.
# Browser-Use VNC Web View
[Browser-use](https://github.com/browser-use/browser-use) 를 사용한 브라우저 자동화 에이전트를 VNC를 통해 실시간으로 모니터링하고 제어할 수 있는 시스템입니다.

## 화면 출력 플로우
<img width="996" height="933" alt="noVNC-arch" src="https://github.com/user-attachments/assets/33de6c7a-f74b-4330-85f1-72ee5840e53c" />

## 데모 영상

https://github.com/user-attachments/assets/5fd999db-980d-4e34-ae8a-dd1c2dd2567a



## 요구사항
- Docker & Docker Compose
- Google Gemini API 키 또는 browser-use가 support하는 모델 (다른 모델 사용 시 agent LLM model 수정 필요)

### 1. 저장소 클론
```bash
git clone https://github.com/squatboy/browser-use-vnc.git
cd browser-use-vnc
```

### 2. 환경변수 설정
```bash
cp .env.example .env
# .env 파일에서 본인의 실제 API 키로 변경
```

### 3. Docker 실행
```bash
docker-compose up --build
```

### 4. 브라우저에서 접속
- **noVNC**: http://Public-IP:6080/vnc.html
- 브라우저 자동화 과정을 실시간으로 확인하고 제어 가능

## 서버 호스트에서 실행

### Security Group 설정
Security Group에서 인바운드 허용 포트:
- 포트 5900 (VNC)
- 포트 6080 (noVNC)

## 시스템 구조

- **Xvfb**: 가상 디스플레이 서버 (:99)
- **x11vnc**: VNC 서버 (포트 5900)
- **websockify**: VNC를 WebSocket으로 변환 (포트 6080)
- **browser-use**: Gemini LLM 기반 브라우저 자동화 에이전트

## 커스터마이징

`browser-use-agent.py` 파일에서 자동화 작업을 수정할 수 있습니다:

```python
agent = Agent(
    task="여기에 원하는 작업을 입력하세요",
    llm=llm,
    browser_session=browser_session,
)
```

**iframe 임베드로 웹사이트 통합:**
다음과 같이 noVNC를 iframe에 임베드하면 자신의 웹사이트에 VNC 서버의 원격 데스크탑 화면을 통합할 수 있습니다.

```html
<iframe 
    src="http://서버IP:6080/vnc.html?autoconnect=true" 
    width="1280" height="720">
</iframe>
```

## 오류 시 확인사항

- **Chrome 실행 실패**: 컨테이너 재시작 `docker-compose restart`
- **VNC 연결 실패**: 보안 그룹 포트 확인
- **API 오류**: .env 파일의 GOOGLE_API_KEY 확인

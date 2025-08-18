## 🇰🇷 [한국어 보기](README.ko.md)

# Browser-Use VNC Web View

A Docker-based system that provides a real-time virtual monitor using VNC/noVNC with two containers: **vnc** and **agent**. The `vnc` container runs the virtual display server and VNC services, while the `agent` container runs `browser-use` script (flight.py) and other applications inside the container, connected via a shared X11 socket.

## Screen Output Flow

<img width="996" height="933" alt="noVNC-arch" src="https://github.com/user-attachments/assets/d86b43ec-4204-4a94-ae86-01c63c39dfe1" />

## Demo

https://github.com/user-attachments/assets/910da29b-46bb-4ed9-95b0-0ea42cadf190

## Quick Start

## Requirements
- Docker & Docker Compose
- git

### 1. Clone Repository
```bash
git clone https://github.com/squatboy/browser-use-vnc.git
cd browser-use-vnc/
```

### 2. Prepare Environment & Agent Files
Before running, place your files inside the `agent` directory:
- `.env`: include your LLM API KEY for browser-use
- `browser-use agent file`: `flight.py`

> These will be automatically loaded by `docker-compose.yml` to configure and run the `agent` container.

### 3. Start VNC and Agent Services
```bash
cd vnc/
docker-compose up -d --build
```

### 4. Access VNC Desktop
- **noVNC**: http://Server-IP:6080/vnc.html

### Configuration if Running on Server Host
Allow inbound ports:
- Port 5900 (VNC)
- Port 6080 (noVNC)

## 🛠️ System Architecture

- **vnc container**:
  - **Xvfb**: Virtual display server (:99)
  - **x11vnc**: VNC server (port 5900)
  - **websockify**: Converts VNC to WebSocket (port 6080)
- **agent container**:
  - **Python + Playwright + flight.py**: Runs browser-use and other apps
  - Shares X11 socket with `vnc` to display output on virtual monitor

### Browser-use BrowserSession Settings

```python
browser_session = BrowserSession(
    headless=False,
    args=[
        "--no-sandbox",           # required in Docker root environments
        "--disable-dev-shm-usage" # prevents /dev/shm crashes in limited containers
    ],
)
```
> Use `--no-sandbox` (root in Docker) and `--disable-dev-shm-usage` (avoid /dev/shm crash).


## 📝 Customization
This system uses two containers working together. Run your applications such as `browser-use` inside the `agent` container, which connects to the virtual display provided by the `vnc` container.

## Use-Case
**Integrating websites with embedding:**
By embedding the noVNC address in an iframe, you can integrate a remote VNC server's desktop screen directly into your own website.

```html
<iframe
    src="http://Server-IP:6080/vnc.html?autoconnect=true"
    width="1280" height="720">
</iframe>
```

## Notes

- **Chrome execution failure**: Restart containers with `docker-compose restart`
- **VNC connection failure**: Check security group ports
- **Multiple sessions**: To run multiple VNC sessions, use different DISPLAY numbers, ports, and unique Docker Compose project names to isolate environments.

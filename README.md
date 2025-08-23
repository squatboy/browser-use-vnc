## 🇰🇷 [한국어 보기](README.ko.md)

# Browser-Use noVNC Web View

A Docker-based system providing a real-time virtual monitor using VNC/noVNC, composed of two containers: **vnc** and **agent**. The `vnc` container runs the virtual display server and VNC services, while the `agent` container runs browser automation scripts such as `agent.py`. The two containers communicate via a shared X11 UNIX socket volume, ensuring isolated and secure sessions.



## System Architecture & Workflow

Each VNC/agent session pair runs isolated using Docker namespaces and unique X11 socket volumes. This design ensures that display data is securely separated between sessions.

### vnc Container

- **Xvfb**: Virtual display server (e.g., :99)
- **x11vnc**: VNC server
- **websockify**: Converts VNC to WebSocket for noVNC access

### agent Container

- Runs Browser-use Python scripts (e.g., `agent.py`)
- Shares the X11 socket volume with the `vnc` container to render output to the virtual display




## Quick Start

### Requirements

- Docker & Docker Compose
- git
- Python 3.8 or higher

### 1. Clone the Repository

```bash
git clone https://github.com/squatboy/browser-use-vnc.git
cd browser-use-vnc/
```

### 2. Prepare Agent Files

Place the following files inside the `agent/` directory:

- `.env`: Your LLM API key and other environment variables for browser-use
- `agent.py`: Your browser-use agent script

> These files will be automatically loaded by Docker Compose to configure and run the agent container.

### 3. Run the FastAPI Orchestrator

Start the orchestrator service which manages session creation:

```bash
uvicorn app_orchestrator:app --host 0.0.0.0 --port 8000
```

### 4. Create a New Session

Send a POST request to create a new VNC/agent session:

```
POST http://<Server-IP>:8000/sessions
```

The response includes the session ID and a dynamically assigned noVNC port:

```json
{
  "session_id": "session123",
  "novnc_port": 6081,
  "url": "http://<Server-IP>:6081/vnc.html"
}
```

### 5. Connect to the Session

Open the provided `url` in your web browser to access virtual display via noVNC.


## Manual Multi-Session Test Example

You can manually create multiple independent sessions by specifying different `SESSION_ID` and `NOVNC_PORT` environment variables and running separate Docker Compose projects.

```bash
# First session
cd vnc/
SESSION_ID=session1 NOVNC_PORT=6081 docker compose -p vnc1 up -d --build

# Second session
SESSION_ID=session2 NOVNC_PORT=6082 docker compose -p vnc2 up -d --build
```

Then access the sessions independently:

- http://<Server-IP>:6081/vnc.html
- http://<Server-IP>:6082/vnc.html

Each session uses its own X11 socket volume, ensuring isolation with no data leakage between sessions.


## Security Group & Network Configuration

When deploying on a public server, open only the noVNC ports required for your sessions (e.g., 6080, 6081, 6082, ...). Make sure to restrict access appropriately.


## BrowserSession Python Configuration Example

When running browsers inside the agent container, use the following settings to avoid common Docker-related issues:

```python
browser_session = BrowserSession(
    headless=False,
    args=[
        "--no-sandbox",            # Required for running as root inside Docker
        "--disable-dev-shm-usage"  # Prevents /dev/shm crashes in limited containers
    ],
)
```


## Customization & Advanced Usage

- The system separates the `vnc` container (virtual display and VNC services) and the `agent` container (browser automation scripts).
- You can extend or modify agent scripts (`agent.py`) to suit your automation workflows.
- The agent container connects to the shared X11 socket volume to render browser output on the virtual display managed by the vnc container.


## Use Case: Embedding VNC Desktop in Your Website

Embed the noVNC web client inside an iframe to integrate the remote desktop directly into your web application:

```html
<iframe
    src="http://<Server-IP>:6080/vnc.html?autoconnect=true"
    width="1280" height="720">
</iframe>
```


## Troubleshooting & Tips

- **Chrome fails to launch**: Restart the containers using `docker compose restart`.
- **VNC connection fails**: Verify your firewall or security group allows inbound traffic on the noVNC ports.


## Additional Notes

- Each session is isolated via Docker namespaces and unique X11 socket volumes.
- Communication between `agent` and `vontainers occurs only through the Xnc` c11 UNIX socket, not over the network.
- You can freely add or modify agent-side scripts and dependencies to fit your use case.

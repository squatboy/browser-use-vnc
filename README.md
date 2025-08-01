## 🇰🇷 [한국어 보기](README.ko.md)

# Browser-Use VNC Web View

A Docker container that enables real-time monitoring and control of AI browser automation using [Browser-use](https://github.com/browser-use/browser-use) through VNC.

## Screen Output Flow

<img width="996" height="933" alt="noVNC-arch" src="https://github.com/user-attachments/assets/d86b43ec-4204-4a94-ae86-01c63c39dfe1" />


## Demo

https://github.com/user-attachments/assets/910da29b-46bb-4ed9-95b0-0ea42cadf190


## Quick Start

## Requirements
- Docker & Docker Compose
- Google Gemini API Key or any browser-use supported model (if using other models, modify the agent LLM model accordingly)

### 1. Clone Repository
```bash
git clone https://github.com/your-username/browser-use-vnc
cd browser-use-vnc
```

### 2. Environment Setup
```bash
cp .env.example .env
# Edit .env file with your actual API key
```

### 3. Run Docker
```bash
docker-compose up --build
```

### 4. Access via Browser
- **noVNC**: http://Server-IP:6080/vnc.html
- Real-time monitoring and control of browser automation process

## Running on Server Host

### 1. Security Group Configuration
Allow inbound ports in Security Group:
- Port 5900 (VNC)
- Port 6080 (noVNC)

### 2. Execution
```bash
git clone https://github.com/squatboy/browser-use-vnc
cd browser-use-vnc
docker-compose up -d
```

### 3. Access
- http://Server-IP:6080/vnc.html

## 🛠️ System Architecture

- **Xvfb**: Virtual display server (:99)
- **x11vnc**: VNC server (port 5900)
- **websockify**: Converts VNC to WebSocket (port 6080)
- **browser-use**: Gemini LLM-based browser automation agent

## 📝 Customization

You can modify automation tasks in the `browser-use-agent.py` file:

```python
agent = Agent(
    task="Enter your desired task here",
    llm=llm,
    browser_session=browser_session,
)
```

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

- **Chrome execution failure**: Restart container `docker-compose restart`
- **VNC connection failure**: Check security group ports
- **API error**: Verify GOOGLE_API_KEY in .env file


## 🇰🇷 [한국어 보기](README.ko.md)

# Browser-Use VNC Web View

A Docker container that provides a real-time virtual monitor system using VNC/noVNC.
This container does not include or execute browser-use itself — run browser-use (or any other app) externally with DISPLAY=:99 to display it here.

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
cd browser-use-vnc
```


### 2. Start VNC Services
```bash
docker-compose up -d --build
```

### 4. Access VNC Desktop
- **noVNC**: http://Server-IP:6080/vnc.html
- The VNC desktop is now ready and will remain accessible


### 3. Monitor in Real-time
- Open **noVNC**: http://Server-IP:6080/vnc.html
- Any external application (e.g., browser-use, Chromium, etc.) running with DISPLAY=:99 will be visible here in real-time

## Running on Server Host

### Security Group Configuration
Allow inbound ports in Security Group:
- Port 5900 (VNC)
- Port 6080 (noVNC)

## 🛠️ System Architecture

- **Xvfb**: Virtual display server (:99)
- **TigerVNC (x0vncserver)**: VNC server (port 5900)
- **websockify**: Converts VNC to WebSocket (port 6080)

## 📝 Customization
This container only provides the VNC/noVNC system.
Run your own applications externally (e.g., browser-use, Chromium) with DISPLAY=:99 to display them on the virtual monitor.

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


# Use a general-purpose base image
FROM ubuntu:22.04

# Set non-interactive frontend to avoid prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies required for VNC, virtual display, and browser
RUN apt-get update && apt-get install -y \
    # X11 & Virtual Display
    xvfb \
    x11vnc \
    xserver-xorg \
    xauth \
    x11-utils \
    x11-xserver-utils \
    # VNC Server (provides x0vncserver)
    tigervnc-standalone-server \
    tigervnc-common \
    # Web VNC client
    novnc \
    websockify \
    # Web Browser
    chromium-browser \
    # Dependencies for browser/display
    libnss3 \
    libatk-bridge2.0-0 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libxss1 \
    libasound2 \
    libatspi2.0-0 \
    libgtk-3-0 \
    # Networking tools for debugging
    net-tools \
    curl \
    # Clean up apt cache
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy the start script into the container
COPY script/start.sh .

# Grant execution permission to the script
RUN chmod +x start.sh

# Expose ports for VNC and noVNC
EXPOSE 5900 6080

# Set the virtual display environment variable
ENV DISPLAY=:99

# Set the command to run when the container starts
CMD ["./start.sh"]

# 컨테이너 시작 스크립트 실행
CMD ["./script/start.sh"]
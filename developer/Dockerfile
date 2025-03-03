# developer/Dockerfile
FROM ubuntu:24.04

# Configurar entorno no interactivo
ENV DEBIAN_FRONTEND=noninteractive

# Instalar TODAS las dependencias
RUN apt-get update && apt-get install -y \
    gnupg \
    xfce4 \
    xfce4-goodies \
    tightvncserver \
    dbus-x11 \
    xfonts-base \
    libgl1-mesa-dri \
    x11-xkb-utils \
    openssh-server \
    postgresql-client \
    wget \
    sudo \
    python3 \
    python3-pip \
    python3-venv \
    git \
    nano \
    net-tools \
    --no-install-recommends

# Configurar entorno virtual Python
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Instalar Flask y dependencias
RUN pip install flask psycopg2-binary

# Instalar Visual Studio Code (paso completo)
RUN wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg \
    && install -o root -g root -m 644 packages.microsoft.gpg /etc/apt/trusted.gpg.d/ \
    && echo "deb [arch=amd64 signed-by=/etc/apt/trusted.gpg.d/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" > /etc/apt/sources.list.d/vscode.list \
    && apt-get update \
    && apt-get install -y code \
    && rm -f packages.microsoft.gpg

# Crear usuario developer
RUN useradd -m -s /bin/bash developer \
    && echo "developer:developer" | chpasswd \
    && usermod -aG sudo developer \
    && echo "developer ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

# Configurar VNC
USER developer
RUN mkdir -p /home/developer/.vnc \
    && echo "password" | vncpasswd -f > /home/developer/.vnc/passwd \
    && chmod 600 /home/developer/.vnc/passwd \
    && echo '#!/bin/sh\nunset SESSION_MANAGER\nunset DBUS_SESSION_BUS_ADDRESS\nexec startxfce4' > /home/developer/.vnc/xstartup \
    && chmod +x /home/developer/.vnc/xstartup

# Script de inicio
USER root
COPY startup.sh /startup.sh
RUN chmod +x /startup.sh

# Limpiar cache
RUN apt-get clean \
    && rm -rf /var/lib/apt/lists/*

CMD ["/startup.sh"]
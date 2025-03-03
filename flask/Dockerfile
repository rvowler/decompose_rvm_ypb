FROM python:3.8-slim

# Instal·lar dependències
RUN apt-get update && apt-get install -y openssh-server && rm -rf /var/lib/apt/lists/*

# Configurar SSH
RUN mkdir /var/run/sshd
RUN echo 'root:password' | chpasswd
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# Configurar aplicació
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Script d'inici
COPY ./start.sh /start.sh
RUN chmod +x /start.sh
CMD ["/start.sh"]
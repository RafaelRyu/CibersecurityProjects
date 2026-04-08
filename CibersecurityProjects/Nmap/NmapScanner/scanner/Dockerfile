FROM python:3.10-slim

# Instala o binário do Nmap no sistema operacional do container
RUN apt-get update && apt-get install -y nmap && rm -rf /var/lib/apt/lists/*

# Define o diretório de trabalho
WORKDIR /app

# Instala a biblioteca python-nmap
RUN pip install --no-cache-dir python-nmap

# Copia o seu script para o container
COPY scanner.py .

# Comando para rodar o script
ENTRYPOINT ["python", "scanner.py"]
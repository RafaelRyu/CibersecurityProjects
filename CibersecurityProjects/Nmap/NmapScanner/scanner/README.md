# Network Scanner Interativo com Python & Docker

Este projeto é um scanner de rede interativo que utiliza a biblioteca `python-nmap`. Ele permite realizar diferentes tipos de varredura (SYN, TCP, UDP, detecção de OS) de forma simplificada, com opções de exportação de resultados.

## 🚀 Pré-requisitos

Para rodar este script, você tem duas opções:

### Opção 1: Rodar nativamente (Local)
* **Python 3.10+** instalado.
* **Nmap** instalado no sistema operacional (O binário do Nmap deve estar no seu PATH).
* Biblioteca `python-nmap`:
    ```bash
    pip install python-nmap
    ```

### Opção 2: Rodar via Docker (Recomendado)
* **Docker** instalado.  
* O sistema requer **sudo** para executar os comandos Docker.  
* É necessário **baixar a pasta `scanner` localmente** e executar todos os comandos Docker **dentro da pasta `scanner`**, pois é nela que estão os arquivos necessários para a construção da imagem.

## 🛠️ Como usar

### Usando Docker (Mais fácil)

1. **Baixe a pasta `scanner` localmente** e navegue até ela:
    ```bash
    cd scanner
    ```

2. **Construa a imagem (com sudo):**
    ```bash
    sudo docker build -t nmap-scanner .
    ```

3. **Execute o container (com sudo):**
    Para scans básicos:
    ```bash
    sudo docker run -it --rm nmap-scanner
    ```
    
    Para scans que exigem privilégios de root (como o SYN Scan `-sS`):
    ```bash
    sudo docker run -it --rm --privileged nmap-scanner
    ```

### Usando Python Localmente

1. Execute o script principal:
    ```bash
    python main.py
    ```
2. Siga as instruções no terminal para inserir o IP alvo, tipo de scan e formato de saída.

## 📋 Funcionalidades
- [x] Escolha de flags do Nmap via menu.
- [x] Especificação de portas ou intervalos customizados.
- [x] Exportação de resultados para arquivos `.txt` ou `.xml`.
- [x] Suporte a detecção de Sistema Operacional e Versão de Serviços.

## ⚠️ Aviso de Segurança
Este script foi desenvolvido para fins educacionais e testes de segurança autorizados. **Nunca** escaneie redes ou dispositivos sem a permissão explícita do proprietário.

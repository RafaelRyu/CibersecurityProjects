import nmap
import sys
import re

def sanitize_input(text, pattern=r'^[a-zA-Z0-9\.\-\/]+$'):
    """
    Sanitiza o input contra caracteres especiais comuns em Injection.
    Permite apenas letras, números, pontos, hífens e barras (CIDR).
    """
    if not re.match(pattern, text):
        raise ValueError(f"Input inválido detectado: {text}")
    return text

def get_menu_choice(options, prompt="Opção: "):
    """Valida se a escolha do usuário está dentro das opções permitidas."""
    choice = input(prompt).strip()
    if choice not in options:
        print(f"[-] Erro: '{choice}' não é uma opção válida.")
        return None
    return choice

def run_scanner():
    nm = nmap.PortScanner()
    
    print("\n" + "="*30)
    print("   Python Nmap Automation")
    print("="*30)

    try:
        # 1. Input do Alvo e Sanitização
        raw_target = input("Digite o IP ou Host (ex: 192.168.1.1): ").strip()
        target = sanitize_input(raw_target)

        # 2. Tipo de Scan
        print("\nEscolha o tipo de scan:")
        print("1. SYN Scan (-sS) [Requer Root]")
        print("2. UDP Scan (-sU) [Requer Root]")
        print("3. Comprehensive Scan (-sS -sV -sC -A)")
        
        scan_choice = get_menu_choice(["1", "2", "3"])
        if not scan_choice: return # Volta para o loop principal
        
        flags = {
            "1": "-sS",
            "2": "-sU",
            "3": "-sS -sV -sC -A"
        }
        selected_flag = flags[scan_choice]

        # 3. Definição de portas (Sanitização simples para números, vírgulas e hífens)
        ports = None
        if input("\nDeseja especificar portas? (s/n): ").lower() == 's':
            raw_ports = input("Digite as portas (ex: 80,443 ou 1-1000): ").strip()
            ports = sanitize_input(raw_ports, pattern=r'^[0-9\-\,]+$')

        # 4. Opções de Output
        print("\nComo deseja salvar o resultado?")
        print("1. Apenas exibir na tela")
        print("2. Salvar em formato Normal (-oN)")
        print("3. Salvar em formato XML (-oX)")
        
        out_choice = get_menu_choice(["1", "2", "3"])
        if not out_choice: return

        output_args = ""
        filename = ""
        if out_choice in ["2", "3"]:
            raw_filename = input("Nome do arquivo (sem extensão): ").strip()
            filename = sanitize_input(raw_filename, pattern=r'^[a-zA-Z0-9_\-]+$')
            ext = ".txt" if out_choice == "2" else ".xml"
            output_args = f" -oN {filename}{ext}" if out_choice == "2" else f" -oX {filename}{ext}"

        # 5. Execução
        print(f"\n[*] Iniciando scan em {target}...")
        arguments = f"{selected_flag}{output_args}"
        
        # O nmap pode lançar exceções se o comando falhar ou não houver privilégios
        nm.scan(hosts=target, ports=ports, arguments=arguments)
        
        if not nm.all_hosts():
            print("[-] Nenhum host encontrado ou alvo inacessível.")
            return

        for host in nm.all_hosts():
            print(f"\nHost: {host} ({nm[host].hostname()})")
            print(f"Estado: {nm[host].state()}")
            
            for proto in nm[host].all_protocols():
                print(f"Protocolo: {proto}")
                lport = nm[host][proto].keys()
                for port in sorted(lport):
                    print(f"Porta: {port}\tEstado: {nm[host][proto][port]['state']}")
                    
        if filename:
            print(f"\n[+] Resultado salvo com sucesso.")

    except ValueError as ve:
        print(f"\n[!] Erro de Validação: {ve}")
    except nmap.PortScannerError as pe:
        print(f"\n[!] Erro do Nmap: {pe}")
        print("Dica: Alguns scans exigem privilégios de administrador (sudo).")
    except Exception as e:
        print(f"\n[!] Ocorreu um erro inesperado: {e}")

if __name__ == "__main__":
    while True:
        run_scanner()
        
        print("\n" + "-"*30)
        cont = input("Deseja realizar outro scan? (s/n): ").lower().strip()
        if cont != 's':
            print("Encerrando... Até logo!")
            sys.exit(0)
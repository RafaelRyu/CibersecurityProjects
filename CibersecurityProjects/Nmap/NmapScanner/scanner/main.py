import nmap
import sys

def run_scanner():
    nm = nmap.PortScanner()
    
    print("--- Python Nmap Automation ---")
    target = input("Digite o IP ou Host para escanear: ")
    
    print("\nEscolha o tipo de scan:")
    print("1. SYN Scan (-sS)")
    print("2. UDP Scan (-sU)")
    print("3. Comprehensive Scan (-sS -sV -sC -A)")
    scan_type_choice = input("Opção: ")
    
    # Mapeamento de flags
    flags = {
        "1": "-sS",
        "2": "-sU",
        "3": "-sS -sV -sC -A"
    }
    selected_flag = flags.get(scan_type_choice, "-sS")

    # Definição de portas
    port_choice = input("\nDeseja especificar portas? (s/n): ").lower()
    ports = None
    if port_choice == 's':
        ports = input("Digite as portas (ex: 80,443 ou 1-1000): ")

    # Opções de Output
    print("\nComo deseja salvar o resultado?")
    print("1. Apenas exibir na tela")
    print("2. Salvar em formato Normal (-oN)")
    print("3. Salvar em formato XML (-oX)")
    output_choice = input("Opção: ")

    output_flag = ""
    filename = ""
    if output_choice in ["2", "3"]:
        filename = input("Digite o nome do arquivo (sem extensão): ")
        ext = ".txt" if output_choice == "2" else ".xml"
        output_flag = f" -oN {filename}{ext}" if output_choice == "2" else f" -oX {filename}{ext}"

    # Execução do Scan
    print(f"\nIniciando scan em {target}...")
    arguments = f"{selected_flag}{output_flag}"
    
    try:
        # O nmap precisa de privilégios de root para certos tipos de scan (como -sS)
        nm.scan(hosts=target, ports=ports, arguments=arguments)
        
        for host in nm.all_hosts():
            print(f"\nHost: {host} ({nm[host].hostname()})")
            print(f"Estado: {nm[host].state()}")
            
            for proto in nm[host].all_protocols():
                print(f"Protocolo: {proto}")
                lport = nm[host][proto].keys()
                for port in sorted(lport):
                    print(f"Porta: {port}\tEstado: {nm[host][proto][port]['state']}")
                    
        if output_choice in ["2", "3"]:
            print(f"\n[+] Resultado salvo em {filename}")

    except Exception as e:
        print(f"Erro ao executar scan: {e}")

if __name__ == "__main__":
    run_scanner()
import os
import sys
import time
from colorama import Fore, Style, init
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from requests.exceptions import RequestException, Timeout, ConnectionError, ProxyError, SSLError

# Inicializar colorama
init()

def clear_screen():
    """Limpia la pantalla de la consola"""
    os.system('cls' if os.name == 'nt' else 'clear')

def count_proxies():
    """Cuenta el número de proxies en el archivo"""
    try:
        with open("proxies.txt", "r") as f:
            proxies = f.readlines()
            return len([p for p in proxies if p.strip()])
    except FileNotFoundError:
        return 0

def print_banner():
    """Imprime el banner del sistema"""
    banner = f"""
{Fore.CYAN}
██████╗  ██████╗ ████████╗ █████╗ ████████╗ ██████╗ ██████╗ 
██╔══██╗██╔═══██╗╚══██╔══╝██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗
██████╔╝██║   ██║   ██║   ███████║   ██║   ██║   ██║██████╔╝
██╔══██╗██║   ██║   ██║   ██╔══██║   ██║   ██║   ██║██╔══██╗
██║  ██║╚██████╔╝   ██║   ██║  ██║   ██║   ╚██████╔╝██║  ██║
╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝
{Style.RESET_ALL}
{Fore.YELLOW}🚀 Sistema Integrado de Gestión de Proxies{Style.RESET_ALL}
{Fore.GREEN}🔗 Rota + Proxytron3000 Fusionados{Style.RESET_ALL}
"""
    print(banner)

def main_menu():
    """Menú principal del sistema"""
    while True:
        clear_screen()
        print_banner()
        
        # Mostrar información del sistema
        try:
            proxy_count = count_proxies()
            print(f"{Fore.GREEN}📊 Proxies cargados: {proxy_count}{Style.RESET_ALL}")
        except:
            print(f"{Fore.RED}📊 No se pudo cargar información de proxies{Style.RESET_ALL}")
        
        print(f"\n{Fore.WHITE}╔══════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
        print(f"{Fore.WHITE}║{Style.RESET_ALL}               {Fore.CYAN}📋 MENÚ PRINCIPAL{Style.RESET_ALL}                    {Fore.WHITE}║{Style.RESET_ALL}")
        print(f"{Fore.WHITE}╠══════════════════════════════════════════════════════════╣{Style.RESET_ALL}")
        print(f"{Fore.WHITE}║{Style.RESET_ALL}  {Fore.YELLOW}1.{Style.RESET_ALL} 🔍 Buscar nuevos proxies (Proxytron3000)       {Fore.WHITE}║{Style.RESET_ALL}")
        print(f"{Fore.WHITE}║{Style.RESET_ALL}  {Fore.YELLOW}2.{Style.RESET_ALL} 🚀 Gestión del servidor proxy (Rota)          {Fore.WHITE}║{Style.RESET_ALL}")
        print(f"{Fore.WHITE}║{Style.RESET_ALL}  {Fore.YELLOW}3.{Style.RESET_ALL} 👀 Gestión de proxies                         {Fore.WHITE}║{Style.RESET_ALL}")
        print(f"{Fore.WHITE}║{Style.RESET_ALL}  {Fore.YELLOW}4.{Style.RESET_ALL} 📊 Estadísticas y reportes                    {Fore.WHITE}║{Style.RESET_ALL}")
        print(f"{Fore.WHITE}║{Style.RESET_ALL}  {Fore.YELLOW}5.{Style.RESET_ALL} ⚙️  Configuración del sistema                 {Fore.WHITE}║{Style.RESET_ALL}")
        print(f"{Fore.WHITE}║{Style.RESET_ALL}  {Fore.YELLOW}6.{Style.RESET_ALL} ❓ Ayuda y información                        {Fore.WHITE}║{Style.RESET_ALL}")
        print(f"{Fore.WHITE}║{Style.RESET_ALL}  {Fore.YELLOW}7.{Style.RESET_ALL} 🚪 Salir                                     {Fore.WHITE}║{Style.RESET_ALL}")
        print(f"{Fore.WHITE}╚══════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
        
        choice = input(f"\n{Fore.GREEN}👉 Selecciona una opción (1-7): {Style.RESET_ALL}")
        
        if choice == "1":
            search_proxies_menu()
        elif choice == "2":
            server_management_menu()
        elif choice == "3":
            proxy_management_menu()
        elif choice == "4":
            statistics_menu()
        elif choice == "5":
            config_menu()
        elif choice == "6":
            help_menu()
        elif choice == "7":
            print(f"\n{Fore.GREEN}👋 ¡Hasta luego!{Style.RESET_ALL}")
            sys.exit(0)
        else:
            print(f"\n{Fore.RED}❌ Opción no válida. Intenta de nuevo.{Style.RESET_ALL}")
            time.sleep(1)

def search_proxies_menu():
    """Menú de búsqueda de proxies"""
    clear_screen()
    print(f"\n{Fore.CYAN}🔍 MENÚ DE BÚSQUEDA DE PROXIES{Style.RESET_ALL}")
    print(f"{Fore.WHITE}══════════════════════════════════════════════════════════{Style.RESET_ALL}")
    
    print(f"\n{Fore.YELLOW}1.{Style.RESET_ALL} Buscar en GitHub")
    print(f"{Fore.YELLOW}2.{Style.RESET_ALL} Buscar en sitios web")
    print(f"{Fore.YELLOW}3.{Style.RESET_ALL} Búsqueda completa (GitHub + Web)")
    print(f"{Fore.YELLOW}4.{Style.RESET_ALL} Validar proxies encontrados")
    print(f"{Fore.YELLOW}5.{Style.RESET_ALL} Volver al menú principal")
    
    choice = input(f"\n{Fore.GREEN}👉 Selecciona una opción (1-5): {Style.RESET_ALL}")
    
    if choice == "1":
        print(f"\n{Fore.GREEN}🚀 Iniciando búsqueda en GitHub...{Style.RESET_ALL}")
        # Importar y ejecutar solo GitHub scraper
        try:
            from Proxytron3000 import github_scraper
            proxies = github_scraper.scrape_github()
            print(f"\n{Fore.GREEN}✅ Búsqueda completada. Encontrados {len(proxies)} proxies.{Style.RESET_ALL}")
            
            # Preguntar si validar automáticamente
            if proxies:
                validate_choice = input(f"\n{Fore.YELLOW}🔍 ¿Validar proxies automáticamente? (s/n): {Style.RESET_ALL}").lower()
                if validate_choice == 's':
                    validate_and_save_proxies(proxies, "github_proxies.txt")
                else:
                    save_proxies(proxies, "github_proxies.txt")
                    print(f"{Fore.YELLOW}📁 Proxies guardados en 'github_proxies.txt'{Style.RESET_ALL}")
            
        except Exception as e:
            print(f"{Fore.RED}❌ Error: {e}{Style.RESET_ALL}")
        input(f"\n{Fore.YELLOW}⏎ Presiona Enter para continuar...{Style.RESET_ALL}")
        
    elif choice == "2":
        print(f"\n{Fore.GREEN}🚀 Iniciando búsqueda en sitios web...{Style.RESET_ALL}")
        # Importar y ejecutar solo web scraper
        try:
            from Proxytron3000 import web_scraper
            proxies = web_scraper.scrape_websites()
            print(f"\n{Fore.GREEN}✅ Búsqueda completada. Encontrados {len(proxies)} proxies.{Style.RESET_ALL}")
            
            # Preguntar si validar automáticamente
            if proxies:
                validate_choice = input(f"\n{Fore.YELLOW}🔍 ¿Validar proxies automáticamente? (s/n): {Style.RESET_ALL}").lower()
                if validate_choice == 's':
                    validate_and_save_proxies(proxies, "web_proxies.txt")
                else:
                    save_proxies(proxies, "web_proxies.txt")
                    print(f"{Fore.YELLOW}📁 Proxies guardados en 'web_proxies.txt'{Style.RESET_ALL}")
            
        except Exception as e:
            print(f"{Fore.RED}❌ Error: {e}{Style.RESET_ALL}")
        input(f"\n{Fore.YELLOW}⏎ Presiona Enter para continuar...{Style.RESET_ALL}")
        
    elif choice == "3":
        print(f"\n{Fore.GREEN}🚀 Iniciando búsqueda completa...{Style.RESET_ALL}")
        # Ejecutar Proxytron3000 completo
        try:
            import subprocess
            subprocess.run(["python", "Proxytron3000/main.py"], cwd=".")
        except Exception as e:
            print(f"{Fore.RED}❌ Error: {e}{Style.RESET_ALL}")
        input(f"\n{Fore.YELLOW}⏎ Presiona Enter para continuar...{Style.RESET_ALL}")
        
    elif choice == "4":
        validate_existing_proxies_menu()
        
    elif choice == "5":
        return
    else:
        print(f"\n{Fore.RED}❌ Opción no válida.{Style.RESET_ALL}")
        time.sleep(1)

def server_management_menu():
    """Menú completo de gestión del servidor proxy"""
    clear_screen()
    print(f"\n{Fore.CYAN}🚀 GESTIÓN DEL SERVIDOR PROXY{Style.RESET_ALL}")
    print(f"{Fore.WHITE}══════════════════════════════════════════════════════════{Style.RESET_ALL}")
    
    print(f"\n{Fore.YELLOW}1.{Style.RESET_ALL} 🚀 Iniciar servidor")
    print(f"{Fore.YELLOW}2.{Style.RESET_ALL} ⏸️  Pausar servidor")
    print(f"{Fore.YELLOW}3.{Style.RESET_ALL} ⏹️  Detener servidor")
    print(f"{Fore.YELLOW}4.{Style.RESET_ALL} 📊 Estado del servidor")
    print(f"{Fore.YELLOW}5.{Style.RESET_ALL} 🔄 Reiniciar servidor")
    print(f"{Fore.YELLOW}6.{Style.RESET_ALL} 📋 Ver logs en tiempo real")
    print(f"{Fore.YELLOW}7.{Style.RESET_ALL} 🎯 Configuración avanzada")
    print(f"{Fore.YELLOW}8.{Style.RESET_ALL} ↩️  Volver al menú principal")
    
    choice = input(f"\n{Fore.GREEN}👉 Selecciona una opción (1-8): {Style.RESET_ALL}")
    
    if choice == "1":
        start_server_menu()
    elif choice == "2":
        pause_server()
    elif choice == "3":
        stop_server()
    elif choice == "4":
        check_server_status()
    elif choice == "5":
        restart_server()
    elif choice == "6":
        view_realtime_logs()
    elif choice == "7":
        advanced_server_config()
    elif choice == "8":
        return
    else:
        print(f"\n{Fore.RED}❌ Opción no válida.{Style.RESET_ALL}")
        time.sleep(1)

def start_server_menu():
    """Submenú para iniciar el servidor"""
    clear_screen()
    print(f"\n{Fore.CYAN}🚀 INICIAR SERVIDOR PROXY{Style.RESET_ALL}")
    print(f"{Fore.WHITE}══════════════════════════════════════════════════════════{Style.RESET_ALL}")
    
    print(f"\n{Fore.YELLOW}1.{Style.RESET_ALL} Iniciar en puerto 8080 (default)")
    print(f"{Fore.YELLOW}2.{Style.RESET_ALL} Iniciar en puerto 8081")
    print(f"{Fore.YELLOW}3.{Style.RESET_ALL} Iniciar en puerto personalizado")
    print(f"{Fore.YELLOW}4.{Style.RESET_ALL} Iniciar con configuración específica")
    print(f"{Fore.YELLOW}5.{Style.RESET_ALL} ↩️  Volver")
    
    choice = input(f"\n{Fore.GREEN}👉 Selecciona una opción (1-5): {Style.RESET_ALL}")
    
    if choice == "1":
        start_server(8080)
    elif choice == "2":
        start_server(8081)
    elif choice == "3":
        try:
            port = int(input(f"{Fore.GREEN}📋 Ingresa el número de puerto: {Style.RESET_ALL}"))
            start_server(port)
        except ValueError:
            print(f"{Fore.RED}❌ Puerto no válido.{Style.RESET_ALL}")
            time.sleep(1)
    elif choice == "4":
        start_with_custom_config()
    elif choice == "5":
        return
    else:
        print(f"\n{Fore.RED}❌ Opción no válida.{Style.RESET_ALL}")
        time.sleep(1)

def start_server(port):
    """Inicia el servidor proxy"""
    print(f"\n{Fore.GREEN}🚀 Iniciando servidor proxy en puerto {port}...{Style.RESET_ALL}")
    try:
        import subprocess
        # Ejecutar Rota en segundo plano
        subprocess.Popen(["python", "main.py", "--port", str(port)], 
                         cwd=".", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"{Fore.GREEN}✅ Servidor iniciado en puerto {port}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}❌ Error al iniciar servidor: {e}{Style.RESET_ALL}")
    input(f"\n{Fore.YELLOW}⏎ Presiona Enter para continuar...{Style.RESET_ALL}")

def check_server_status():
    """Verifica el estado del servidor"""
    print(f"\n{Fore.CYAN}📊 Estado del servidor:{Style.RESET_ALL}")
    # Aquí se podría implementar verificación real del estado
    print(f"{Fore.YELLOW}⚠️  Función de verificación de estado en desarrollo{Style.RESET_ALL}")
    input(f"\n{Fore.YELLOW}⏎ Presiona Enter para continuar...{Style.RESET_ALL}")

def stop_server():
    """Detiene el servidor proxy"""
    print(f"\n{Fore.RED}🛑 Deteniendo servidor proxy...{Style.RESET_ALL}")
    # Aquí se podría implementar la detención real
    print(f"{Fore.YELLOW}⚠️  Función de detención en desarrollo{Style.RESET_ALL}")
    input(f"\n{Fore.YELLOW}⏎ Presiona Enter para continuar...{Style.RESET_ALL}")

def view_proxies_menu():
    """Menú para ver los proxies"""
    clear_screen()
    print(f"\n{Fore.CYAN}👀 VISUALIZACIÓN DE PROXIES{Style.RESET_ALL}")
    print(f"{Fore.WHITE}══════════════════════════════════════════════════════════{Style.RESET_ALL}")
    
    try:
        with open("proxies.txt", "r") as f:
            proxies = f.readlines()
            print(f"{Fore.GREEN}📊 Total de proxies en el archivo: {len(proxies)}{Style.RESET_ALL}")
            
            if len(proxies) > 0:
                print(f"\n{Fore.YELLOW}Primeros 10 proxies:{Style.RESET_ALL}")
                for i, proxy in enumerate(proxies[:10], 1):
                    print(f"{i}. {proxy.strip()}")
                
                if len(proxies) > 10:
                    print(f"{Fore.YELLOW}... y {len(proxies) - 10} más{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}❌ No hay proxies en el archivo{Style.RESET_ALL}")
    except FileNotFoundError:
        print(f"{Fore.RED}❌ Archivo proxies.txt no encontrado{Style.RESET_ALL}")
    
    input(f"\n{Fore.YELLOW}⏎ Presiona Enter para continuar...{Style.RESET_ALL}")

def config_menu():
    """Menú de configuración"""
    clear_screen()
    print(f"\n{Fore.CYAN}⚙️  MENÚ DE CONFIGURACIÓN{Style.RESET_ALL}")
    print(f"{Fore.WHITE}══════════════════════════════════════════════════════════{Style.RESET_ALL}")
    
    print(f"\n{Fore.YELLOW}1.{Style.RESET_ALL} Ver configuración actual")
    print(f"{Fore.YELLOW}2.{Style.RESET_ALL} Editar configuración")
    print(f"{Fore.YELLOW}3.{Style.RESET_ALL} Restaurar configuración por defecto")
    print(f"{Fore.YELLOW}4.{Style.RESET_ALL} Volver al menú principal")
    
    choice = input(f"\n{Fore.GREEN}👉 Selecciona una opción (1-4): {Style.RESET_ALL}")
    
    if choice == "1":
        view_config()
    elif choice == "2":
        edit_config()
    elif choice == "3":
        reset_config()
    elif choice == "4":
        return
    else:
        print(f"\n{Fore.RED}❌ Opción no válida.{Style.RESET_ALL}")
        time.sleep(1)

def view_config():
    """Muestra la configuración actual"""
    print(f"\n{Fore.CYAN}📋 Configuración actual:{Style.RESET_ALL}")
    try:
        import yaml
        with open("config.yaml", "r") as f:
            config = yaml.safe_load(f)
            for section, settings in config.items():
                print(f"\n{Fore.YELLOW}{section.upper()}:{Style.RESET_ALL}")
                for key, value in settings.items():
                    print(f"  {key}: {value}")
    except Exception as e:
        print(f"{Fore.RED}❌ Error al leer configuración: {e}{Style.RESET_ALL}")
    input(f"\n{Fore.YELLOW}⏎ Presiona Enter para continuar...{Style.RESET_ALL}")

def edit_config():
    """Edita la configuración"""
    print(f"\n{Fore.YELLOW}⚠️  Función de edición de configuración en desarrollo{Style.RESET_ALL}")
    input(f"\n{Fore.YELLOW}⏎ Presiona Enter para continuar...{Style.RESET_ALL}")

def proxy_management_menu():
    """Menú completo de gestión de proxies"""
    clear_screen()
    proxy_count = count_proxies()
    print(f"\n{Fore.CYAN}📋 GESTIÓN DE PROXIES{Style.RESET_ALL}")
    print(f"{Fore.WHITE}══════════════════════════════════════════════════════════{Style.RESET_ALL}")
    print(f"{Fore.GREEN}📊 Proxies disponibles: {proxy_count}{Style.RESET_ALL}")
    
    print(f"\n{Fore.YELLOW}1.{Style.RESET_ALL} 👁️  Ver lista de proxies")
    print(f"{Fore.YELLOW}2.{Style.RESET_ALL} 🔍 Filtrar proxies")
    print(f"{Fore.YELLOW}3.{Style.RESET_ALL} 🗑️  Eliminar proxies")
    print(f"{Fore.YELLOW}4.{Style.RESET_ALL} 📊 Estadísticas de proxies")
    print(f"{Fore.YELLOW}5.{Style.RESET_ALL} 📤 Exportar proxies")
    print(f"{Fore.YELLOW}6.{Style.RESET_ALL} 📥 Importar proxies")
    print(f"{Fore.YELLOW}7.{Style.RESET_ALL} 🧹 Limpiar proxies inválidos")
    print(f"{Fore.YELLOW}8.{Style.RESET_ALL} ↩️  Volver al menú principal")
    
    choice = input(f"\n{Fore.GREEN}👉 Selecciona una opción (1-8): {Style.RESET_ALL}")
    
    if choice == "1":
        view_proxies_menu()
    elif choice == "2":
        filter_proxies_menu()
    elif choice == "3":
        delete_proxies_menu()
    elif choice == "4":
        proxy_statistics()
    elif choice == "5":
        export_proxies_menu()
    elif choice == "6":
        import_proxies()
    elif choice == "7":
        clean_invalid_proxies()
    elif choice == "8":
        return
    else:
        print(f"\n{Fore.RED}❌ Opción no válida.{Style.RESET_ALL}")
        time.sleep(1)

def filter_proxies_menu():
    """Submenú para filtrar proxies"""
    clear_screen()
    print(f"\n{Fore.CYAN}🔍 FILTRAR PROXIES{Style.RESET_ALL}")
    print(f"{Fore.WHITE}══════════════════════════════════════════════════════════{Style.RESET_ALL}")
    
    print(f"\n{Fore.YELLOW}1.{Style.RESET_ALL} Por protocolo (HTTP/HTTPS/SOCKS)")
    print(f"{Fore.YELLOW}2.{Style.RESET_ALL} Por país")
    print(f"{Fore.YELLOW}3.{Style.RESET_ALL} Por velocidad")
    print(f"{Fore.YELLOW}4.{Style.RESET_ALL} Por anonimidad")
    print(f"{Fore.YELLOW}5.{Style.RESET_ALL} ↩️  Volver")
    
    choice = input(f"\n{Fore.GREEN}👉 Selecciona una opción (1-5): {Style.RESET_ALL}")
    
    if choice == "1":
        filter_by_protocol()
    elif choice == "2":
        filter_by_country()
    elif choice == "3":
        filter_by_speed()
    elif choice == "4":
        filter_by_anonymity()
    elif choice == "5":
        return
    else:
        print(f"\n{Fore.RED}❌ Opción no válida.{Style.RESET_ALL}")
        time.sleep(1)

def delete_proxies_menu():
    """Submenú para eliminar proxies"""
    clear_screen()
    print(f"\n{Fore.CYAN}🗑️  ELIMINAR PROXIES{Style.RESET_ALL}")
    print(f"{Fore.WHITE}══════════════════════════════════════════════════════════{Style.RESET_ALL}")
    
    print(f"\n{Fore.YELLOW}1.{Style.RESET_ALL} Eliminar proxy específico")
    print(f"{Fore.YELLOW}2.{Style.RESET_ALL} Eliminar por rango")
    print(f"{Fore.YELLOW}3.{Style.RESET_ALL} Eliminar todos los proxies")
    print(f"{Fore.YELLOW}4.{Style.RESET_ALL} Eliminar duplicados")
    print(f"{Fore.YELLOW}5.{Style.RESET_ALL} ↩️  Volver")
    
    choice = input(f"\n{Fore.GREEN}👉 Selecciona una opción (1-5): {Style.RESET_ALL}")
    
    if choice == "1":
        delete_specific_proxy()
    elif choice == "2":
        delete_range_proxies()
    elif choice == "3":
        delete_all_proxies()
    elif choice == "4":
        remove_duplicates()
    elif choice == "5":
        return
    else:
        print(f"\n{Fore.RED}❌ Opción no válida.{Style.RESET_ALL}")
        time.sleep(1)

def export_proxies_menu():
    """Submenú para exportar proxies"""
    clear_screen()
    print(f"\n{Fore.CYAN}📤 EXPORTAR PROXIES{Style.RESET_ALL}")
    print(f"{Fore.WHITE}══════════════════════════════════════════════════════════{Style.RESET_ALL}")
    
    print(f"\n{Fore.YELLOW}1.{Style.RESET_ALL} Exportar a Excel (.xlsx)")
    print(f"{Fore.YELLOW}2.{Style.RESET_ALL} Exportar a CSV (.csv)")
    print(f"{Fore.YELLOW}3.{Style.RESET_ALL} Exportar a JSON (.json)")
    print(f"{Fore.YELLOW}4.{Style.RESET_ALL} Exportar a texto (.txt)")
    print(f"{Fore.YELLOW}5.{Style.RESET_ALL} ↩️  Volver")
    
    choice = input(f"\n{Fore.GREEN}👉 Selecciona una opción (1-5): {Style.RESET_ALL}")
    
    if choice == "1":
        export_to_excel()
    elif choice == "2":
        export_to_csv()
    elif choice == "3":
        export_to_json()
    elif choice == "4":
        export_to_text()
    elif choice == "5":
        return
    else:
        print(f"\n{Fore.RED}❌ Opción no válida.{Style.RESET_ALL}")
        time.sleep(1)

# Funciones placeholder para las nuevas opciones
def proxy_statistics():
    """Muestra estadísticas de proxies"""
    print(f"\n{Fore.YELLOW}⚠️  Función de estadísticas en desarrollo{Style.RESET_ALL}")
    input(f"\n{Fore.YELLOW}⏎ Presiona Enter para continuar...{Style.RESET_ALL}")

def import_proxies():
    """Importa proxies desde archivo"""
    print(f"\n{Fore.YELLOW}⚠️  Función de importación en desarrollo{Style.RESET_ALL}")
    input(f"\n{Fore.YELLOW}⏎ Presiona Enter para continuar...{Style.RESET_ALL}")

def clean_invalid_proxies():
    """Limpia proxies inválidos"""
    print(f"\n{Fore.YELLOW}⚠️  Función de limpieza en desarrollo{Style.RESET_ALL}")
    input(f"\n{Fore.YELLOW}⏎ Presiona Enter para continuar...{Style.RESET_ALL}")

def filter_by_protocol():
    """Filtra proxies por protocolo"""
    print(f"\n{Fore.YELLOW}⚠️  Función de filtrado por protocolo en desarrollo{Style.RESET_ALL}")
    input(f"\n{Fore.YELLOW}⏎ Presiona Enter para continuar...{Style.RESET_ALL}")

def filter_by_country():
    """Filtra proxies por país"""
    print(f"\n{Fore.YELLOW}⚠️  Función de filtrado por país en desarrollo{Style.RESET_ALL}")
    input(f"\n{Fore.YELLOW}⏎ Presiona Enter para continuar...{Style.RESET_ALL}")

def filter_by_speed():
    """Filtra proxies por velocidad"""
    print(f"\n{Fore.YELLOW}⚠️  Función de filtrado por velocidad en desarrollo{Style.RESET_ALL}")
    input(f"\n{Fore.YELLOW}⏎ Presiona Enter para continuar...{Style.RESET_ALL}")

def filter_by_anonymity():
    """Filtra proxies por anonimidad"""
    print(f"\n{Fore.YELLOW}⚠️  Función de filtrado por anonimidad en desarrollo{Style.RESET_ALL}")
    input(f"\n{Fore.YELLOW}⏎ Presiona Enter para continuar...{Style.RESET_ALL}")

def delete_specific_proxy():
    """Elimina proxy específico"""
    print(f"\n{Fore.YELLOW}⚠️  Función de eliminación específica en desarrollo{Style.RESET_ALL}")
    input(f"\n{Fore.YELLOW}⏎ Presiona Enter para continuar...{Style.RESET_ALL}")

def delete_range_proxies():
    """Elimina proxies por rango"""
    print(f"\n{Fore.YELLOW}⚠️  Función de eliminación por rango en desarrollo{Style.RESET_ALL}")
    input(f"\n{Fore.YELLOW}⏎ Presiona Enter para continuar...{Style.RESET_ALL}")

def delete_all_proxies():
    """Elimina todos los proxies"""
    print(f"\n{Fore.YELLOW}⚠️  Función de eliminación total en desarrollo{Style.RESET_ALL}")
    input(f"\n{Fore.YELLOW}⏎ Presiona Enter para continuar...{Style.RESET_ALL}")

def remove_duplicates():
    """Elimina duplicados"""
    print(f"\n{Fore.YELLOW}⚠️  Función de eliminación de duplicados en desarrollo{Style.RESET_ALL}")
    input(f"\n{Fore.YELLOW}⏎ Presiona Enter para continuar...{Style.RESET_ALL}")

def export_to_excel():
    """Exporta a Excel"""
    print(f"\n{Fore.YELLOW}⚠️  Función de exportación a Excel en desarrollo{Style.RESET_ALL}")
    input(f"\n{Fore.YELLOW}⏎ Presiona Enter para continuar...{Style.RESET_ALL}")

def export_to_csv():
    """Exporta a CSV"""
    print(f"\n{Fore.YELLOW}⚠️  Función de exportación a CSV en desarrollo{Style.RESET_ALL}")
    input(f"\n{Fore.YELLOW}⏎ Presiona Enter para continuar...{Style.RESET_ALL}")

def export_to_json():
    """Exporta a JSON"""
    print(f"\n{Fore.YELLOW}⚠️  Función de exportación a JSON en desarrollo{Style.RESET_ALL}")
    input(f"\n{Fore.YELLOW}⏎ Presiona Enter para continuar...{Style.RESET_ALL}")

def export_to_text():
    """Exporta a texto"""
    print(f"\n{Fore.YELLOW}⚠️  Función de exportación a texto en desarrollo{Style.RESET_ALL}")
    input(f"\n{Fore.YELLOW}⏎ Presiona Enter para continuar...{Style.RESET_ALL}")

def pause_server():
    """Pausa el servidor"""
    print(f"\n{Fore.YELLOW}⚠️  Función de pausa en desarrollo{Style.RESET_ALL}")
    input(f"\n{Fore.YELLOW}⏎ Presiona Enter para continuar...{Style.RESET_ALL}")

def restart_server():
    """Reinicia el servidor"""
    print(f"\n{Fore.YELLOW}⚠️  Función de reinicio en desarrollo{Style.RESET_ALL}")
    input(f"\n{Fore.YELLOW}⏎ Presiona Enter para continuar...{Style.RESET_ALL}")

def view_realtime_logs():
    """Muestra logs en tiempo real"""
    print(f"\n{Fore.YELLOW}⚠️  Función de logs en tiempo real en desarrollo{Style.RESET_ALL}")
    input(f"\n{Fore.YELLOW}⏎ Presiona Enter para continuar...{Style.RESET_ALL}")

def advanced_server_config():
    """Configuración avanzada del servidor"""
    print(f"\n{Fore.YELLOW}⚠️  Función de configuración avanzada en desarrollo{Style.RESET_ALL}")
    input(f"\n{Fore.YELLOW}⏎ Presiona Enter para continuar...{Style.RESET_ALL}")

def start_with_custom_config():
    """Inicia servidor con configuración personalizada"""
    print(f"\n{Fore.YELLOW}⚠️  Función de configuración personalizada en desarrollo{Style.RESET_ALL}")
    input(f"\n{Fore.YELLOW}⏎ Presiona Enter para continuar...{Style.RESET_ALL}")

def statistics_menu():
    """Menú de estadísticas"""
    print(f"\n{Fore.YELLOW}⚠️  Menú de estadísticas en desarrollo{Style.RESET_ALL}")
    input(f"\n{Fore.YELLOW}⏎ Presiona Enter para continuar...{Style.RESET_ALL}")

def help_menu():
    """Menú de ayuda"""
    print(f"\n{Fore.YELLOW}⚠️  Menú de ayuda en desarrollo{Style.RESET_ALL}")
    input(f"\n{Fore.YELLOW}⏎ Presiona Enter para continuar...{Style.RESET_ALL}")

# Funciones auxiliares para manejo de proxies
def save_proxies(proxies, filename):
    """Guarda una lista de proxies en un archivo"""
    try:
        with open(filename, 'w') as f:
            for proxy in proxies:
                f.write(proxy + '\n')
        return True
    except Exception as e:
        print(f"{Fore.RED}❌ Error al guardar proxies: {e}{Style.RESET_ALL}")
        return False

def merge_with_existing(new_proxies):
    """Fusiona nuevos proxies con los existentes en proxies.txt"""
    try:
        existing_proxies = set()
        
        # Leer proxies existentes
        try:
            with open("proxies.txt", 'r') as f:
                existing_proxies = set(line.strip() for line in f if line.strip())
        except FileNotFoundError:
            existing_proxies = set()
        
        # Combinar con nuevos proxies
        all_proxies = existing_proxies.union(set(new_proxies))
        
        # Guardar de vuelta
        with open("proxies.txt", 'w') as f:
            for proxy in all_proxies:
                f.write(proxy + '\n')
        
        print(f"{Fore.GREEN}✅ Fusionados {len(new_proxies)} nuevos proxies")
        print(f"📊 Total de proxies únicos: {len(all_proxies)}{Style.RESET_ALL}")
        
    except Exception as e:
        print(f"{Fore.RED}❌ Error al fusionar proxies: {e}{Style.RESET_ALL}")

def validate_and_save_proxies(proxies, filename):
    """Valida proxies usando Proxytron3000 y los guarda en archivo"""
    print(f"\n{Fore.BLUE}🔍 Validando {len(proxies)} proxies con Proxytron3000...{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}⚠️  Validando en lotes de mínimo 25 proxies...{Style.RESET_ALL}")
    
    # Importar el validador de Proxytron3000
    try:
        from Proxytron3000.validator import validate_proxies_batch, filter_valid_proxies, get_validation_stats
    except ImportError:
        print(f"{Fore.RED}❌ Error: No se pudo importar Proxytron3000{Style.RESET_ALL}")
        return
    
    # Validar en lotes de mínimo 25
    batch_size = max(25, min(50, len(proxies) // 10))  # Mínimo 25, máximo 50 o 10% del total
    valid_proxies = []
    
    for i in range(0, len(proxies), batch_size):
        batch = proxies[i:i + batch_size]
        print(f"\n{Fore.CYAN}📦 Procesando lote {i//batch_size + 1}/{(len(proxies)-1)//batch_size + 1} ({len(batch)} proxies){Style.RESET_ALL}")
        
        # Validar el lote actual
        validation_results = validate_proxies_batch(
            batch, 
            max_workers=15,
            test_url="http://httpbin.org/ip",
            timeout=10
        )
        
        # Obtener estadísticas del lote
        stats = get_validation_stats(validation_results)
        batch_valid = filter_valid_proxies(validation_results)
        valid_proxies.extend(batch_valid)
        
        print(f"{Fore.GREEN}✅ Lote completado: {len(batch_valid)}/{len(batch)} válidos ({stats['success_rate']:.1f}%){Style.RESET_ALL}")
    
    # Guardar todos los proxies válidos
    if valid_proxies:
        save_proxies(valid_proxies, filename)
        
        # Mostrar estadísticas finales
        final_stats = get_validation_stats(
            {proxy: {'valid': True, 'response_time': 0, 'protocol': 'http'} for proxy in valid_proxies}
        )
        
        print(f"\n{Fore.GREEN}🎉 Validación completada con Proxytron3000!")
        print(f"📊 Total válidos: {len(valid_proxies)}/{len(proxies)} ({final_stats['success_rate']:.2f}%)")
        print(f"📁 Guardados en: {filename}{Style.RESET_ALL}")
        
        # Preguntar si fusionar con proxies.txt
        merge_choice = input(f"\n{Fore.YELLOW}🔄 ¿Fusionar con proxies.txt? (s/n): {Style.RESET_ALL}").lower()
        if merge_choice == 's':
            merge_with_existing(valid_proxies)
    else:
        print(f"\n{Fore.RED}❌ No se encontraron proxies válidos{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}💡 Esto es normal con proxies públicos. Intenta con más proxies o fuentes diferentes.{Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}👋 Programa interrumpido por el usuario{Style.RESET_ALL}")
        sys.exit(0)
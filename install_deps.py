import subprocess
import sys
from colorama import Fore, Style, init

# Inicializar colorama
init()

def install_requirements():
    """Instala todas las dependencias necesarias"""
    print(f"{Fore.CYAN}📦 Instalando dependencias...{Style.RESET_ALL}")
    
    # Dependencias principales de Rota
    rota_deps = [
        "requests",
        "pyyaml",
        "aiohttp",
        "colorama"
    ]
    
    # Dependencias de Proxytron3000
    proxytron_deps = [
        "beautifulsoup4",
        "lxml",
        "openpyxl"  # Para manejar archivos Excel
    ]
    
    all_deps = rota_deps + proxytron_deps
    
    for dep in all_deps:
        try:
            print(f"{Fore.YELLOW}⬇️  Instalando {dep}...{Style.RESET_ALL}")
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
            print(f"{Fore.GREEN}✅ {dep} instalado correctamente{Style.RESET_ALL}")
        except subprocess.CalledProcessError:
            print(f"{Fore.RED}❌ Error al instalar {dep}{Style.RESET_ALL}")
    
    print(f"\n{Fore.GREEN}🎉 ¡Todas las dependencias han sido instaladas!{Style.RESET_ALL}")
    print(f"{Fore.CYAN}🚀 Puedes ejecutar el sistema con: python main.py --menu{Style.RESET_ALL}")

if __name__ == "__main__":
    install_requirements()
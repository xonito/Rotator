#!/usr/bin/env python3
"""
Script de prueba para la función de validación de proxies
"""

import sys
import os

# Añadir el directorio actual al path para importar menu_system
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from menu_system import validate_and_save_proxies

def test_validation():
    """Prueba la función de validación con algunos proxies de ejemplo"""
    
    # Proxies más prometedores (algunos de GitHub scraping reciente)
    test_proxies = [
        "http://8.210.97.116:80",           # Proxy HTTP conocido
        "https://45.77.243.236:3128",       # Proxy HTTPS
        "142.93.245.196:3128",              # Proxy sin protocolo especificado
        "socks5://94.154.127.101:8085",     # Proxy SOCKS5 de GitHub
        "47.91.89.3:8080",                  # Proxy de GitHub
        "148.72.177.90:8228",               # Proxy de GitHub
        "124.164.248.75:6060",              # Proxy de GitHub
        "http://20.219.178.121:3128",       # Proxy adicional
        "https://8.219.97.248:80"           # Proxy HTTPS adicional
    ]
    
    print("🧪 Probando función de validación de proxies...")
    print(f"📋 Proxies de prueba: {len(test_proxies)}")
    
    # Llamar a la función de validación
    validate_and_save_proxies(test_proxies, "test_proxies.txt")
    
    print("\n✅ Prueba completada!")
    
    # Mostrar resultados
    try:
        with open("test_proxies.txt", "r") as f:
            valid_proxies = f.read().splitlines()
        print(f"📊 Proxies válidos encontrados: {len(valid_proxies)}")
        for proxy in valid_proxies:
            print(f"   ✅ {proxy}")
    except FileNotFoundError:
        print("❌ No se encontraron proxies válidos")

if __name__ == "__main__":
    test_validation()
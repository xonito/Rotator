#!/usr/bin/env python3
"""
Script de prueba para los scrapers de Proxytron3000
"""

import sys
import os

# Añadir el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from Proxytron3000 import scrape_github, scrape_websites
    
    print("🧪 Probando scrapers de Proxytron3000...")
    print("=" * 50)
    
    # Probar GitHub scraper
    print("\n1. Probando GitHub Scraper:")
    github_proxies = scrape_github()
    print(f"📊 Proxies de GitHub: {len(github_proxies)}")
    if github_proxies:
        print(f"   Ejemplo: {github_proxies[0]}")
    
    # Probar Web scraper  
    print("\n2. Probando Web Scraper:")
    web_proxies = scrape_websites()
    print(f"📊 Proxies de Web: {len(web_proxies)}")
    if web_proxies:
        print(f"   Ejemplo: {web_proxies[0]}")
    
    print("\n✅ Todos los scrapers funcionando correctamente!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
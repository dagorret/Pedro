import os
import json
import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from datetime import datetime

def fetch_news():
    print("🕵️ Iniciando Motor de Inteligencia Pedro...")
    
    # 1. Cargar fuentes del archivo TXT
    sources_path = "data/news_sources.txt"
    if not os.path.exists(sources_path):
        print("❌ Error: data/news_sources.txt no encontrado.")
        return

    daily_news = []     # Para el DIB (Diario)
    tech_news = []      # Para el CTW (Magazine del viernes)

    with open(sources_path, "r", encoding="utf-8") as f:
        # Saltamos la cabecera
        lines = f.readlines()[1:] 
        
    for line in lines:
        if not line.strip() or line.startswith("#"): continue
        
        try:
            url, category, location, product = line.strip().split(";")
            print(f"📡 Escaneando [{product}] {location}: {url[:50]}...")
            
            response = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
            
            # Detectar si es RSS (XML) o Web (HTML)
            content_type = response.headers.get('Content-Type', '')
            
            titles = []
            
            if "xml" in content_type or url.endswith(".xml") or url.endswith(".rss"):
                # PROCESAR RSS
                root = ET.fromstring(response.content)
                for item in root.findall(".//item"):
                    title = item.find("title")
                    if title is not None:
                        titles.append(title.text)
            else:
                # PROCESAR HTML (BeautifulSoup)
                soup = BeautifulSoup(response.text, 'html.parser')
                for tag in soup.find_all(['h2', 'h3']):
                    texto = tag.get_text().strip()
                    if len(texto) > 25: titles.append(texto)

            # Clasificar según la columna 'Product'
            entry_list = [{"title": t, "source": url, "cat": category} for t in titles[:15]] # max 15 por fuente
            
            if product == "DIB":
                daily_news.extend(entry_list)
            elif product == "CTW":
                tech_news.extend(entry_list)

        except Exception as e:
            print(f"⚠️ Falló fuente {url}: {e}")

    # --- GUARDADO INTELIGENTE ---
    os.makedirs("data", exist_ok=True)

    # 1. El Diario del día (DIB)
    with open("data/latest_news.json", "w", encoding="utf-8") as f:
        json.dump(daily_news, f, indent=4, ensure_ascii=False)

    # 2. El Acumulador Tech (CTW)
    acc_path = "data/tech_accumulator.json"
    existing_tech = []
    if os.path.exists(acc_path):
        try:
            with open(acc_path, "r", encoding="utf-8") as f:
                existing_tech = json.load(f)
        except: pass
    
    existing_tech.extend(tech_news)
    with open(acc_path, "w", encoding="utf-8") as f:
        json.dump(existing_tech, f, indent=4, ensure_ascii=False)

    print(f"\n✅ PROCESO COMPLETADO:")
    print(f"📰 Noticias para DIB: {len(daily_news)}")
    print(f"💻 Noticias para CTW (Acumuladas): {len(tech_news)}")

if __name__ == "__main__":
    fetch_news()

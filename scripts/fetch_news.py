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

    # Filtro de Calidad (Blacklist de basura comercial)
    blacklist = ["Promo Code", "Coupon", "Deals", "Off", "Mattress", "Discount", "Save $", "Sale", "H&R Block"]

    with open(sources_path, "r", encoding="utf-8") as f:
        lines = f.readlines()[1:]

    for line in lines:
        if not line.strip() or line.startswith("#"): continue

        try:
            url, category, location, product = line.strip().split(";")
            print(f"📡 Escaneando [{product}] {location}: {url[:50]}...")

            response = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
            content_type = response.headers.get('Content-Type', '')

            titles = []

            if "xml" in content_type or url.endswith(".xml") or url.endswith(".rss"):
                root = ET.fromstring(response.content)
                for item in root.findall(".//item"):
                    title = item.find("title")
                    if title is not None:
                        titles.append(title.text)
            else:
                soup = BeautifulSoup(response.text, 'html.parser')
                for tag in soup.find_all(['h2', 'h3']):
                    texto = tag.get_text().strip()
                    if len(texto) > 25: titles.append(texto)

            # Clasificar y Filtrar
            for t in titles[:15]:
                # Limpieza básica de ruido en el texto
                t_clean = t.replace('"', "'").strip()

                # Aplicar filtro solo si es producto Tech (CTW)
                if product == "CTW":
                    if any(word.lower() in t_clean.lower() for word in blacklist):
                        continue # Salta los cupones
                    if len(t_clean) < 35:
                        continue # Salta títulos muy cortos/menús

                entry = {"title": t_clean, "source": url, "cat": category}

                if product == "DIB":
                    daily_news.append(entry)
                elif product == "CTW":
                    tech_news.append(entry)

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
                content = f.read()
                if content:
                    existing_tech = json.loads(content)
        except Exception as e:
            print(f"⚠️ No se pudo leer el acumulador, iniciando uno nuevo: {e}")

    # Agregamos lo nuevo a lo viejo
    existing_tech.extend(tech_news)

    # Guardar acumulado
    with open(acc_path, "w", encoding="utf-8") as f:
        json.dump(existing_tech, f, indent=4, ensure_ascii=False)

    print(f"\n✅ PROCESO COMPLETADO:")
    print(f"📰 Noticias para DIB: {len(daily_news)}")
    print(f"💻 Noticias para CTW (Nuevas filtradas): {len(tech_news)}")
    print(f"📦 Total en Acumulador: {len(existing_tech)}")

if __name__ == "__main__":
    fetch_news()

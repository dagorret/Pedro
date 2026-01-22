import feedparser
import requests
import urllib3

# Desactivar advertencias de SSL inseguro si fuera necesario
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def validate_feeds(file_path):
    print(f"--- Iniciando Validación de Fuentes en {file_path} ---")
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            # Filtramos líneas vacías y comentarios, pero mantenemos el índice
            lines = [line.strip() for line in f if line.strip() and not line.startswith("#")]
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo en {file_path}")
        return

    # Usamos enumerate para saber en qué número de línea estamos
    for i, line in enumerate(lines):
        # SALTAR LA CABECERA: Si es la primera línea con texto, la ignoramos
        if i == 0 and "URL;" in line:
            continue

        parts = line.split(";")
        if len(parts) < 3:
            print(f"❌ Error de formato en línea {i+1}: {line}")
            continue
            
        url = parts[0].strip()
        category = parts[1].strip()
        
        try:
            # User-Agent para que no nos bloqueen (simulamos un navegador)
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            resp = requests.get(url, timeout=15, headers=headers, verify=False) # verify=False ayuda con errores de SSL viejos
            
            if resp.status_code != 200:
                print(f"❌ HTTP {resp.status_code} - {url}")
                continue
            
            d = feedparser.parse(resp.content)
            
            if len(d.entries) > 0:
                print(f"✅ OK ({len(d.entries)} noticias) - {category} - {url[:50]}...")
            else:
                print(f"⚠️  VACÍO (Feed existe pero no tiene noticias) - {url}")
                
        except Exception as e:
            print(f"🔥 ERROR CRÍTICO - {url} -> {str(e)[:50]}")

if __name__ == "__main__":
    validate_feeds("data/news_sources.txt")

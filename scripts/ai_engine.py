import os
import json
import sys
import google.generativeai as genai
from datetime import datetime

# CONFIGURACIÓN SEGURA: Lee la clave desde las variables de entorno
API_KEY = os.environ.get("GOOGLE_API_KEY")

if not API_KEY:
    print("❌ ERROR: No se encontró la variable de entorno GOOGLE_API_KEY")
    sys.exit(1)

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def generate_report():
    # ... (el resto del código se mantiene igual) ...
    if not os.path.exists("data/latest_news.json"):
        print("❌ No hay noticias para procesar.")
        return

    with open("data/latest_news.json", "r") as f:
        news = json.load(f)

    if not news:
        print("⚠️ El archivo de noticias está vacío.")
        return

    news_subset = news[:40]
    prompt = f"Actúa como un experto analista. Resume estas noticias para Carlos Dagorret. Usa Markdown y sé conciso:\n\n{json.dumps(news_subset)}"

    try:
        print("🧠 Consultando a la IA (Gemini)...")
        response = model.generate_content(prompt)
        
        # Validación de seguridad por si la respuesta viene vacía
        if not response.text:
            raise Exception("La IA devolvió una respuesta vacía")

        fecha_hoy = datetime.now().strftime("%Y-%m-%d")
        os.makedirs("docs/dib", exist_ok=True)
        
        with open(f"docs/dib/{fecha_hoy}.md", "w", encoding="utf-8") as f:
            f.write(response.text)
        
        print(f"✅ Reporte generado: docs/dib/{fecha_hoy}.md")
        
    except Exception as e:
        print(f"❌ Error crítico en Gemini: {e}")
        sys.exit(1)

if __name__ == "__main__":
    generate_report()

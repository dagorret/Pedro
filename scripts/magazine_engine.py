import os
import json
import sys
import google.generativeai as genai
from datetime import datetime

# CONFIGURACIÓN DE API
API_KEY = os.environ.get("GOOGLE_API_KEY")

if not API_KEY:
    print("❌ ERROR: Variable GOOGLE_API_KEY no encontrada.")
    sys.exit(1)

genai.configure(api_key=API_KEY)

# Usamos el modelo 2.5-flash que confirmaste que funciona en tu consola
try:
    model = genai.GenerativeModel('gemini-2.5-flash')
except Exception as e:
    print(f"⚠️ Error al inicializar modelo 2.5: {e}")
    sys.exit(1)


def generate_magazine():
    input_path = "data/tech_accumulator.json"

    if not os.path.exists(input_path):
        print("❌ No hay acumulador tech para procesar (archivo inexistente).")
        return 1

    with open(input_path, "r", encoding="utf-8") as f:
        try:
            content = f.read()
            if not content:
                print("⚠️ El acumulador está vacío (archivo en blanco).")
                return 0
            all_tech_news = json.loads(content)
        except Exception as e:
            print(f"❌ Error al parsear JSON: {e}")
            return 1

    print(f"📊 Noticias totales en el acumulador: {len(all_tech_news)}")

    # --- FILTRO DE CALIDAD (Anti-Colchones y Cupones) ---
    blacklist = ["Promo Code", "Coupon", "Deals", "Off", "Mattress", "Discount", "Sale", "H&R Block"]

    clean_news = [
        n for n in all_tech_news
        if not any(word.lower() in n.get("title", "").lower() for word in blacklist)
           and len(n.get("title", "")) > 30
    ]

    print(f"🧹 Noticias después del filtrado: {len(clean_news)}")

    if len(clean_news) < 3:
        print("⚠️ Muy poca información relevante para armar un magazine. Se requiere más data.")
        return 0

    # Limitamos a las últimas 80 para el prompt
    tech_subset = clean_news[-80:]

    print(f"🔬 Enviando {len(tech_subset)} noticias a Gemini 2.5-Flash...")

    prompt = f"""
    Actúa como un Editor Jefe de una revista de tecnología de élite.
    Tu objetivo es redactar la "WEEKLY TECH MAGAZINE (CTW)" para Carlos Dagorret.

    ESTRUCTURA (Markdown):
    1. Título Creativo y la Fecha de hoy ({datetime.now().strftime('%Y-%m-%d')}).
    2. 'El Gran Tema': Elige la tendencia más disruptiva de estos datos y analízala.
    3. 'Secciones': IA, Hardware y Gadgets, Software y Ciberseguridad.
    4. 'Veredicto de Pedro': Una conclusión sarcástica pero inteligente sobre el estado de la tecnología esta semana.

    DATOS RECOLECTADOS:
    {json.dumps(tech_subset, ensure_ascii=False)}
    """

    try:
        response = model.generate_content(prompt)

        # Guardado en docs/ctw/
        fecha_hoy = datetime.now().strftime("%Y-%m-%d")
        os.makedirs("docs/ctw", exist_ok=True)

        ruta_salida = f"docs/ctw/{fecha_hoy}.md"
        with open(ruta_salida, "w", encoding="utf-8") as f:
            f.write(response.text)

        print(f"✅ MAGAZINE GENERADO: {ruta_salida}")
        print(f"📏 Tamaño: {os.path.getsize(ruta_salida)} bytes")
        return 0

    except Exception as e:
        print(f"❌ Error crítico en la generación de IA: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(generate_magazine())
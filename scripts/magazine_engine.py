import os
import json
import sys
import google.generativeai as genai
from datetime import datetime

# CONFIGURACIÓN
API_KEY = os.environ.get("GOOGLE_API_KEY")

if not API_KEY:
    print("❌ ERROR: Variable GOOGLE_API_KEY no encontrada.")
    sys.exit(1)

genai.configure(api_key=API_KEY)
# Para el magazine usamos 1.5-flash porque maneja ventanas de contexto grandes (útil para mucha data semanal)
model = genai.GenerativeModel('gemini-2.5-flash')

def generate_magazine():
    input_path = "data/tech_accumulator.json"
    
    if not os.path.exists(input_path):
        print("❌ No hay acumulador tech para procesar.")
        return

    with open(input_path, "r", encoding="utf-8") as f:
        all_tech_news = json.load(f)

    if len(all_tech_news) == 0:
        print("⚠️ El acumulador está vacío. Nada que reportar esta semana.")
        return

    # Limitar para no saturar tokens (las 80 más recientes)
    tech_subset = all_tech_news[-80:]
    
    print(f"🔬 Procesando {len(tech_subset)} noticias tecnológicas de la semana...")

    prompt = f"""
    Actúa como un Editor Jefe de una revista de tecnología (estilo Wired o TechCrunch).
    Analiza las siguientes noticias recolectadas durante la semana y crea el "MAGAZINE SEMANAL DE TECNOLOGÍA" para Carlos Dagorret.

    ESTRUCTURA REQUERIDA (en Español):
    1. Título impactante con la fecha.
    2. 'El Gran Tema': Elige la tendencia más importante de la semana y analízala en 2 párrafos.
    3. 'Breves de Innovación': Resúmenes de otras noticias importantes agrupadas por: IA, Hardware, Software y Negocios.
    4. 'Veredicto': Una breve reflexión sobre hacia dónde va la industria tras lo visto esta semana.

    NOTICIAS DE LA SEMANA:
    {json.dumps(tech_subset)}
    """

    try:
        response = model.generate_content(prompt)
        
        # Guardamos en la carpeta de CTW
        fecha_hoy = datetime.now().strftime("%Y-%m-%d")
        os.makedirs("docs/ctw", exist_ok=True)
        
        ruta_salida = f"docs/ctw/{fecha_hoy}.md"
        with open(ruta_salida, "w", encoding="utf-8") as f:
            f.write(response.text)
        
        print(f"✅ Magazine Semanal generado con éxito en: {ruta_salida}")
        
    except Exception as e:
        print(f"❌ Error en Magazine Engine: {e}")
        sys.exit(1)

if __name__ == "__main__":
    generate_magazine()

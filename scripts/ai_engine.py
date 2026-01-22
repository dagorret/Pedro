import os
import json
from datetime import datetime
from google import genai

# CONFIGURACIÓN DE IDENTIDAD
API_KEY = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=API_KEY)

# --- DATOS DEL PROYECTO ---
AUTOR = "Carlos Dagorret"
PROYECTO_INFO = "Generado por Pedro, un proyecto basado en Gemini AI"

def generate_reports():
    print(f"--- 🧠 Generando reporte para {AUTOR} ---")
    
    # Verificar si existen noticias
    if not os.path.exists("data/latest_news.json"):
        print("❌ Error: No existe data/latest_news.json"); return

    with open("data/latest_news.json", "r", encoding="utf-8") as f:
        news_data = json.load(f)

    # Filtrar noticias para el DIB
    dib_news = [n for n in news_data if n.get("product") == "DIB"]
    context_data = json.dumps(dib_news[:80], ensure_ascii=False)

    # FECHA ACTUAL
    date_str = datetime.now().strftime("%Y-%m-%d")

    # PROMPT DE INTELIGENCIA PURA (Sin saludos, directo al grano)
    prompt = f"""
    ACTÚA COMO UN ANALISTA SENIOR DE INTELIGENCIA CON PENSAMIENTO CRÍTICO.
    
    REGLA DE ORO DE FORMATO:
    - NO me saludes.
    - NO confirmes que recibiste la orden.
    - NO digas "Aquí tienes el informe".
    - COMIENZA DIRECTAMENTE con el título en Markdown: # Daily Intelligence Briefing - {date_str}
    - Usa un tono frío, profesional, directo y analítico.

    DATA DISPONIBLE:
    {context_data}
    
    INSTRUCCIONES DE CURATORÍA:
    1. PRIORIDAD: Selecciona los eventos con mayor potencial de impacto estructural.
    2. DIVERSIDAD: No permitas que un solo actor o país domine más del 40% del reporte.
    3. PROFUNDIDAD: Explica POR QUÉ esto le importa a un tomador de decisiones como {AUTOR}.

    ESTRUCTURA OBLIGATORIA DEL REPORTE:
    # Daily Intelligence Briefing - {date_str}
    ## Resumen Ejecutivo
    (Escribe 3 párrafos concisos y potentes)
    
    ## Análisis de Temas Clave
    (Desarrolla 5 temas con variedad geográfica y técnica)
    
    ## Conclusión Estratégica
    (Proyección a corto/mediano plazo)

    IMPORTANTE: Al final de todo el texto, añade esta línea de crédito:
    "{PROYECTO_INFO}"
    """

    try:
        # Llamada a la IA
        response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
        content_md = response.text
        
        # --- FILTRO DE SEGURIDAD (La "mordaza" por código) ---
        # Si la IA llega a saludar, cortamos todo lo que esté antes del primer '#'
        if "#" in content_md:
            content_md = content_md[content_md.find("#"):].strip()
        else:
            content_md = content_md.strip()

        # GUARDAR ARCHIVO MARKDOWN
        os.makedirs("docs/dib", exist_ok=True)
        md_path = f"docs/dib/{date_str}.md"
        
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(content_md)
            
        print(f"✅ Reporte Markdown generado: {md_path}")

    except Exception as e:
        print(f"❌ Error al llamar a Gemini: {e}")

if __name__ == "__main__":
    generate_reports()

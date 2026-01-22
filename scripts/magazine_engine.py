import os, json
from datetime import datetime
# ... (imports de genai y configuración)

def generar_magazine():
    ruta_tech = "data/tech_accumulator.json"
    if not os.path.exists(ruta_tech): return

    with open(ruta_tech, "r", encoding="utf-8") as f:
        noticias_tech = json.load(f)

    # Prompt enfocado en profundidad tecnológica
    # ... (lógica de Gemini) ...

    # Guardar el .md
    fecha = datetime.now().strftime("%Y-%m-%d")
    os.makedirs("docs/mag", exist_ok=True)
    with open(f"docs/mag/{fecha}.md", "w", encoding="utf-8") as f:
        f.write(contenido_ai)

    # LIMPIEZA: Solo se borra el semanal después de generar el magazine
    with open(ruta_tech, "w", encoding="utf-8") as f:
        json.dump([], f)
    
    print("✨ Magazine Tech generado y acumulador limpiado.")

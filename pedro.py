import os
import subprocess
import datetime

def main():
    print(f"--- 🚀 INICIO CICLO PEDRO: {datetime.datetime.now()} ---")
    
    # 1. TRAER NOTICIAS (¡Este paso es vital!)
    print("Paso 1: Recolectando noticias...")
    # Asegúrate de que la ruta al script sea correcta
    subprocess.run(["python3", "scripts/fetch_news.py"])

    # 2. Intentar generar Reporte Diario
    print("Paso 2: Generando reporte...")
    resultado_ai = subprocess.run(["python3", "scripts/ai_engine.py"])

    # 3. Borrado Inteligente
    # Solo borramos si el código de salida fue 0 (éxito) Y si el reporte se generó
    fecha_hoy = datetime.datetime.now().strftime("%Y-%m-%d")
    reporte_existe = os.path.exists(f"docs/dib/{fecha_hoy}.md")

    if resultado_ai.returncode == 0 and reporte_existe:
        if os.path.exists("data/latest_news.json"):
            with open("data/latest_news.json", "w") as f:
                f.write("[]")
            print("🗑️ Memoria diaria reseteada.")
    else:
        print("⚠️ No se borró el JSON: El reporte no se generó o no había noticias.")

    # 4. Generar Web
    subprocess.run(["python3", "scripts/generator.py"])
    print("--- ✅ FIN DEL CICLO ---")

if __name__ == "__main__":
    main()

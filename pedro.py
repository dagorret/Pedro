import os, subprocess, datetime

def main():
    print(f"--- 🚀 PEDRO: INICIO DE CICLO [{datetime.datetime.now().strftime('%H:%M')}] ---")
    
    # 1. Traer noticias (Esto genera latest_news.json y tech_accumulator.json)
    subprocess.run(["python3", "scripts/fetch_news.py"])

    # 2. Generar Reporte Diario (Usa latest_news.json)
    subprocess.run(["python3", "scripts/ai_engine.py"])
    
    # 3. Borrar el JSON diario (El semanal NO se toca)
    if os.path.exists("data/latest_news.json"):
        with open("data/latest_news.json", "w") as f: f.write("[]")
        print("🗑️ Memoria diaria borrada.")

    # 4. Verificar si es VIERNES >= 20:00 para el Magazine
    ahora = datetime.datetime.now()
    if ahora.weekday() == 4 and ahora.hour >= 20:
        print("📰 Es viernes 20hs. Generando Magazine Semanal Tech...")
        subprocess.run(["python3", "scripts/magazine_engine.py"])
        # El magazine_engine.py debe vaciar tech_accumulator.json al terminar

    # 5. Reconstruir la Web
    subprocess.run(["python3", "scripts/generator.py"])
    print("✅ Ciclo Pedro completado.")

if __name__ == "__main__":
    main()

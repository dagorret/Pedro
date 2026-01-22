import os
import subprocess
import datetime
import sys

def main():
    ahora = datetime.datetime.now()
    fecha_hoy = ahora.strftime("%Y-%m-%d")
    print(f"--- 🚀 INICIO CICLO PEDRO: {ahora} ---")
    
    # 1. TRAER NOTICIAS (DIB y CTW)
    print("Paso 1: Recolectando noticias desde fuentes internacionales y locales...")
    subprocess.run(["python3", "scripts/fetch_news.py"])

    # 2. GENERAR REPORTE DIARIO (DIB)
    print("Paso 2: Procesando reporte diario con IA...")
    resultado_ai = subprocess.run(["python3", "scripts/ai_engine.py"])

    # 3. VERIFICAR ÉXITO Y BORRADO DE MEMORIA DIARIA
    # Solo reseteamos el diario si la IA devolvió éxito (0) y el archivo existe
    reporte_diario_ruta = f"docs/dib/{fecha_hoy}.md"
    
    if resultado_ai.returncode == 0 and os.path.exists(reporte_diario_ruta):
        if os.path.exists("data/latest_news.json"):
            with open("data/latest_news.json", "w", encoding="utf-8") as f:
                f.write("[]")
            print("🗑️ Memoria diaria (DIB) reseteada correctamente.")
    else:
        print("⚠️ Advertencia: El reporte diario falló o no generó contenido. Se conserva JSON.")

    # 4. CICLO ESPECIAL: MAGAZINE TECH (Solo los Viernes)
    # 4 = Viernes en weekday()
    if ahora.weekday() == 4:
        print("📅 Hoy es viernes: Iniciando generación de Magazine (CTW)...")
        resultado_mag = subprocess.run(["python3", "scripts/magazine_engine.py"])
        
        # Si el magazine salió bien, reseteamos el acumulador semanal
        if resultado_mag.returncode == 0:
            acc_path = "data/tech_accumulator.json"
            if os.path.exists(acc_path):
                with open(acc_path, "w", encoding="utf-8") as f:
                    f.write("[]")
                print("🗑️ Acumulador semanal (CTW) reseteado.")

    # 5. GENERAR SITIO WEB (Actualizar index.html y listados)
    print("Paso 5: Actualizando portal web estático...")
    subprocess.run(["python3", "scripts/generator.py"])
    
    print(f"--- ✅ FIN DEL CICLO PEDRO: {datetime.datetime.now()} ---")

if __name__ == "__main__":
    main()

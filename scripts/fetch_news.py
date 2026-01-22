import json
import os

def guardar_noticias(nuevas_noticias):
    ruta_diario = "data/latest_news.json"
    ruta_semanal = "data/tech_accumulator.json"
    
    # 1. Cargamos el acumulador semanal (si existe)
    if os.path.exists(ruta_semanal):
        with open(ruta_semanal, "r", encoding="utf-8") as f:
            acumulador_tech = json.load(f)
    else:
        acumulador_tech = []

    noticias_diarias = []
    
    for n in nuevas_noticias:
        # Clasificación: Si es Tech o MAG va al acumulador
        es_tech = any(kw in n.get('title', '').lower() for kw in ['ai', 'tech', 'software', 'microtik', 'cyber'])
        
        if es_tech or n.get('product') == 'MAG':
            # Evitar duplicados en el semanal
            if n.get('link') not in {x.get('link') for x in acumulador_tech}:
                acumulador_tech.append(n)
        
        # Todas las noticias del día van al diario (para el DIB)
        noticias_diarias.append(n)

    # 2. Guardamos (El diario sobreescribe, el semanal acumula)
    with open(ruta_diario, "w", encoding="utf-8") as f:
        json.dump(noticias_diarias, f, ensure_ascii=False, indent=4)
        
    with open(ruta_semanal, "w", encoding="utf-8") as f:
        json.dump(acumulador_tech, f, ensure_ascii=False, indent=4)

    print(f"✅ Diario actualizado. Acumulador Tech tiene: {len(acumulador_tech)} noticias.")

import os
import glob
from datetime import datetime

NOMBRE_SISTEMA = "Carlos Dagorret Intelligence"
CREDITOS = "Generado por Pedro, un proyecto basado en Gemini AI"

def build_site():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    docs_dir = os.path.join(root_dir, "docs")
    
    # Buscamos en 'dib' para diario y 'ctw' para el magazine tech
    dibs = sorted(glob.glob(os.path.join(docs_dir, "dib", "*.md")), reverse=True)
    mags = sorted(glob.glob(os.path.join(docs_dir, "ctw", "*.md")), reverse=True)

    latest_dib = os.path.basename(dibs[0]) if dibs else None
    
    # CSS para forzar el texto blanco dentro del Markdown y mejorar legibilidad
    MD_STYLE = """
    <template>
        <style>
            .markdown-body { background:transparent!important; color:#e6edf3!important; font-family:sans-serif; line-height:1.6; }
            h1,h2,h3 { color:#58a6ff!important; border-bottom:1px solid #30363d!important; margin-top:24px; }
            li { margin-bottom: 8px; }
            blockquote { border-left: 4px solid #30363d; padding-left: 16px; color: #8b949e; }
        </style>
    </template>
    """

    # Generamos los links del historial (DIB)
    sidebar_html = "".join([f'<a href="visor.html?src=dib/{os.path.basename(d)}" class="list-item">📅 DIB - {os.path.basename(d).replace(".md","")}</a>' for d in dibs[1:6]])
    
    # Generamos los links para el Magazine Tech (CTW)
    mag_grid_html = "".join([f'<a href="visor_tech.html?src=ctw/{os.path.basename(m)}" class="mag-card">🛰️ MAGAZINE TECH - {os.path.basename(m).replace(".md","")}</a>' for m in mags])

    index_html = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>{NOMBRE_SISTEMA}</title>
        <script type="module" src="https://cdn.jsdelivr.net/gh/zerodevx/zero-md@2/dist/zero-md.min.js"></script>
        <style>
            :root {{ --bg: #0d1117; --card: #161b22; --text: #f0f6fc; --accent: #58a6ff; --tech: #7ee787; --border: #30363d; }}
            body {{ background: var(--bg); color: var(--text); font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; max-width: 1100px; margin: 0 auto; padding: 20px; }}
            .grid {{ display: grid; grid-template-columns: 2fr 1fr; gap: 20px; }}
            .box {{ background: var(--card); border: 1px solid var(--border); border-radius: 8px; padding: 20px; min-height: 400px; }}
            .list-item {{ display: block; padding: 10px; border: 1px solid var(--border); margin-bottom: 8px; border-radius: 5px; color: var(--accent); text-decoration: none; font-size: 0.9em; transition: 0.2s; }}
            .list-item:hover {{ background: #1f242c; border-color: var(--accent); }}
            .mag-section {{ margin-top: 50px; border-top: 2px solid var(--tech); padding-top: 20px; }}
            .mag-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 15px; }}
            .mag-card {{ border: 1px solid var(--tech); color: var(--tech); padding: 15px; border-radius: 8px; text-decoration: none; text-align: center; font-weight: bold; transition: 0.2s; }}
            .mag-card:hover {{ background: #1c2a22; transform: translateY(-2px); }}
            footer {{ text-align: center; margin-top: 50px; color: #8b949e; font-size: 0.8em; padding-bottom: 40px; }}
            @media (max-width: 768px) {{ .grid {{ grid-template-columns: 1fr; }} }}
        </style>
    </head>
    <body>
        <header>
            <h1>🕵️ {NOMBRE_SISTEMA}</h1>
        </header>
        <div class="grid">
            <div class="box">
                <h3 style="color: var(--accent)">Último Briefing Diario</h3>
                {f'<zero-md src="dib/{latest_dib}">{MD_STYLE}</zero-md>' if latest_dib else "<p>No hay reportes disponibles.</p>"}
            </div>
            <div class="box">
                <h3 style="color: var(--accent)">Historial Reciente</h3>
                {sidebar_html if sidebar_html else "<p>Próximamente...</p>"}
            </div>
        </div>
        <div class="mag-section">
            <h2 style="color: var(--tech)">🔬 Weekly Tech Magazine (CTW)</h2>
            <div class="mag-grid">
                {mag_grid_html if mag_grid_html else "<p style='color:#8b949e'>El primer ejemplar se publicará este viernes.</p>"}
            </div>
        </div>
        <footer>{CREDITOS} - {datetime.now().year}</footer>
    </body>
    </html>
    """
    with open(os.path.join(docs_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html)
    print("✅ Index.html generado con visibilidad y rutas corregidas.")

if __name__ == "__main__":
    build_site()

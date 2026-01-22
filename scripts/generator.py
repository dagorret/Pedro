import os
import glob
from datetime import datetime

NOMBRE_SISTEMA = "Carlos Dagorret Intelligence"
CREDITOS = "Generado por Pedro, un proyecto basado en Gemini AI"

def build_site():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    docs_dir = os.path.join(root_dir, "docs")
    
    dibs = sorted(glob.glob(os.path.join(docs_dir, "dib", "*.md")), reverse=True)
    mags = sorted(glob.glob(os.path.join(docs_dir, "mag", "*.md")), reverse=True)

    latest_dib = os.path.basename(dibs[0]) if dibs else None
    
    # CSS para forzar el texto blanco dentro del Markdown
    MD_STYLE = "<template><style>.markdown-body { background:transparent!important; color:#e6edf3!important; font-family:sans-serif; } h1,h2,h3 { color:#58a6ff!important; border-bottom:1px solid #30363d!important; }</style></template>"

    sidebar_html = "".join([f'<a href="visor.html?src=dib/{os.path.basename(d)}" class="list-item">📅 DIB - {os.path.basename(d).replace(".md","")}</a>' for d in dibs[1:6]])
    mag_grid_html = "".join([f'<a href="visor_tech.html?src=mag/{os.path.basename(m)}" class="mag-card">🛰️ MAGAZINE TECH - {os.path.basename(m).replace(".md","")}</a>' for m in mags])

    index_html = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <script type="module" src="https://cdn.jsdelivr.net/gh/zerodevx/zero-md@2/dist/zero-md.min.js"></script>
        <style>
            :root {{ --bg: #0d1117; --card: #161b22; --text: #f0f6fc; --accent: #58a6ff; --tech: #7ee787; --border: #30363d; }}
            body {{ background: var(--bg); color: var(--text); font-family: -apple-system, sans-serif; max-width: 1100px; margin: 0 auto; padding: 20px; }}
            .grid {{ display: grid; grid-template-columns: 2fr 1fr; gap: 20px; }}
            .box {{ background: var(--card); border: 1px solid var(--border); border-radius: 8px; padding: 20px; }}
            .list-item {{ display: block; padding: 10px; border: 1px solid var(--border); margin-bottom: 5px; border-radius: 5px; color: var(--accent); text-decoration: none; font-size: 0.9em; }}
            .mag-section {{ margin-top: 50px; border-top: 2px solid var(--tech); padding-top: 20px; }}
            .mag-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 15px; }}
            .mag-card {{ border: 1px solid var(--tech); color: var(--tech); padding: 15px; border-radius: 8px; text-decoration: none; text-align: center; font-weight: bold; }}
            footer {{ text-align: center; margin-top: 50px; color: #8b949e; font-size: 0.8em; }}
        </style>
    </head>
    <body>
        <h1>🕵️ {NOMBRE_SISTEMA}</h1>
        <div class="grid">
            <div class="box">
                <h3>Último Briefing Diario</h3>
                <zero-md src="dib/{latest_dib}">{MD_STYLE}</zero-md>
            </div>
            <div class="box">
                <h3>Historial</h3>
                {sidebar_html}
            </div>
        </div>
        <div class="mag-section">
            <h2>🔬 Tech Magazine Archive</h2>
            <div class="mag-grid">{mag_grid_html}</div>
        </div>
        <footer>{CREDITOS}</footer>
    </body>
    </html>
    """
    with open(os.path.join(docs_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html)
    print("✅ Index.html generado con visibilidad corregida.")

if __name__ == "__main__":
    build_site()

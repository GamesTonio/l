import os
import urllib.parse

# ==========================================
# CONFIGURACIÓN - CAMBIA ESTO
# ==========================================
USER_GITHUB = "TU_USUARIO_AQUÍ"
REPO_NAME = "NOMBRE_DE_TU_REPOSITORIO"
# ==========================================

BASE_URL = f"https://{USER_GITHUB}.github.io/{REPO_NAME}/"

def get_image_links():
    extensions = ('.jpg', '.jpeg', '.png', '.gif')
    images = []
    
    # Carpetas a escanear
    folders = ['Cartas', 'Portadas']
    
    for folder in folders:
        if not os.path.exists(folder):
            continue
            
        for root, dirs, files in os.walk(folder):
            for file in files:
                if file.lower().endswith(extensions):
                    # Obtener ruta relativa (ej: Cartas/Carpeta1/img.png)
                    relative_path = os.path.relpath(os.path.join(root, file))
                    # Normalizar para URL (usar / en lugar de \)
                    url_path = relative_path.replace(os.sep, '/')
                    # Codificar caracteres especiales (espacios, etc)
                    encoded_url = urllib.parse.quote(url_path)
                    
                    images.append({
                        "local_path": url_path,
                        "full_url": f"{BASE_URL}{encoded_url}"
                    })
    return images

def create_html(image_list):
    html_template = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Link Direct de las Imagenes</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            body {{ background-color: #1a2634; }}
            .custom-blue {{ background-color: #0081c9; }}
            .row-bg {{ background-color: #1e2d3d; }}
            .row-border {{ border-bottom: 1px solid #2d3e50; }}
        </style>
    </head>
    <body class="text-white font-sans mb-10">
        <!-- Header -->
        <div class="custom-blue w-full py-4 text-center shadow-lg mb-2">
            <h1 class="text-xl font-bold tracking-wide">Link Direct de las Imagenes</h1>
        </div>

        <!-- Container -->
        <div class="max-w-4xl mx-auto px-2">
            <div id="links-container">
                {"".join([f'''
                <div class="flex items-center p-2 row-bg row-border hover:bg-[#25374a] transition-colors">
                    <div class="w-10 text-gray-400 text-sm font-mono text-center">{i+1}</div>
                    <div class="w-12 h-12 flex-shrink-0 border border-gray-600 overflow-hidden ml-2">
                        <img src="{img['local_path']}" class="w-full h-full object-cover" loading="lazy">
                    </div>
                    <div class="ml-4 flex-grow truncate text-sm font-mono tracking-tight text-blue-100 select-all">
                        {img['full_url']}
                    </div>
                </div>
                ''' for i, img in enumerate(image_list)])}
            </div>

            <!-- Botón Copiar -->
            <div class="flex justify-center mt-8">
                <button onclick="copyLinks()" class="bg-[#00a8ff] hover:bg-[#0081c9] text-white font-bold py-3 px-16 rounded-xl shadow-lg transition-all active:scale-95 uppercase tracking-widest text-lg">
                    COPIAR
                </button>
            </div>
        </div>

        <script>
            function copyLinks() {{
                const links = { [img['full_url'] for img in image_list] };
                const textToCopy = links.join('\\n');
                
                navigator.clipboard.writeText(textToCopy).then(() => {{
                    alert('¡' + links.length + ' enlaces copiados al portapapeles!');
                }}).catch(err => {{
                    console.error('Error al copiar: ', err);
                }});
            }}
        </script>
    </body>
    </html>
    """
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_template)

if __name__ == "__main__":
    print("Escaneando imágenes...")
    lista_imagenes = get_image_links()
    create_html(lista_imagenes)
    print(f"¡Hecho! Se han encontrado {len(lista_imagenes)} imágenes.")
    print("Se ha generado el archivo 'index.html'.")

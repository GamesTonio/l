import os
import urllib.parse

# ==========================================
# CONFIGURACIÓN - CAMBIA ESTO
# ==========================================
USER_GITHUB = "GamesTonio"
REPO_NAME = "l"
# ==========================================

BASE_URL = f"https://{USER_GITHUB}.github.io/{REPO_NAME}/"

def get_data():
    extensions = ('.jpg', '.jpeg', '.png', '.gif')

    cartas = {}
    portadas = []

    # ===== CARTAS (por subcarpeta) =====
    base_cartas = 'Cartas'

    if os.path.exists(base_cartas):
        for subfolder in os.listdir(base_cartas):
            sub_path = os.path.join(base_cartas, subfolder)

            if not os.path.isdir(sub_path):
                continue

            cartas[subfolder] = []

            for file in os.listdir(sub_path):
                if file.lower().endswith(extensions):
                    full_path = os.path.join(sub_path, file)
                    relative = os.path.relpath(full_path)
                    url = urllib.parse.quote(relative.replace(os.sep, '/'))

                    cartas[subfolder].append({
                        "name": file,
                        "url": f"{BASE_URL}{url}"
                    })

            # 🔤 ordenar alfabéticamente
            cartas[subfolder].sort(key=lambda x: x["name"].lower())

    # ===== PORTADAS (galería) =====
    base_portadas = 'Portadas'

    if os.path.exists(base_portadas):
        for file in os.listdir(base_portadas):
            if file.lower().endswith(extensions):
                full_path = os.path.join(base_portadas, file)
                relative = os.path.relpath(full_path)
                url = urllib.parse.quote(relative.replace(os.sep, '/'))

                portadas.append({
                    "name": file,
                    "url": f"{BASE_URL}{url}",
                    "local": relative.replace(os.sep, '/')
                })

        portadas.sort(key=lambda x: x["name"].lower())

    return cartas, portadas




def create_html(cartas, portadas):
    folders_html = ""
    scripts = ""

    for folder, images in cartas.items():
        safe = folder.replace(" ", "_")

        urls = [img["url"] for img in images]

        folders_html += f"""
        <div class="folder" onclick="openModal('{safe}')">
            📁 {folder}
        </div>
        """

        scripts += f"""
        function openModal_{safe}() {{
            const links = {urls};
            showModal("{folder}", links);
        }}
        """

        folders_html = folders_html.replace(
            f"openModal('{safe}')",
            f"openModal_{safe}()"
        )

    # ===== PORTADAS =====
    portadas_html = "".join([f"""
    <div class="card border-2 border-purple-600 p-0 rounded-lg">
        <img src="{img['local']}">
        <div class="name">{img['name']}</div>
        <button class="bg-purple-600 text-white w-full font-bold uppercase rounded-b-lg" onclick="copyText('{img['url']}')" >Copiar URL</button>
    </div>
    """ for img in portadas])

    html = f"""
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<script src="https://cdn.tailwindcss.com"></script>
<script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>

<style>
body {{ background:#1a2634; color:white; font-family:sans-serif; }}

.folder {{
    padding:10px;
    background:#1e2d3d;
    margin:4px;
    cursor:pointer;
    border-radius:6px;
}}

.folder:hover {{ background:#2a3f55; }}

.grid {{
    display:grid;
    grid-template-columns: repeat(auto-fill, minmax(120px,1fr));
    gap:10px;
}}

.card {{
    background:#1e2d3d;
    padding:5px;
    border-radius:6px;
    text-align:center;
}}

.card img {{
    width:100%;  
    aspect-ratio: 2 / 3;
    height:auto;
    object-fit:fill;
    
}}

.name {{
    font-size:12px;
    margin:4px 0;
    word-break:break-all;
}}

.modal {{
    position:fixed;
    top:0; left:0;
    width:100%; height:100%;
    background:rgba(0,0,0,0.8);
    display:none;
    justify-content:center;
    align-items:center;
}}

.modal-content {{
    background:#1e2d3d;
    padding:20px;
    width:80%;
    max-height:80%;
    overflow:auto;
    border-radius:10px;
}}

</style>
</head>

<body class="p-4">

<h1 class="text-xl mb-4">📁 Cartas</h1>
<div>
{folders_html}
</div>

<h1 class="text-xl mt-8 mb-4">🖼 Portadas</h1>
<div class="grid">
{portadas_html}
</div>

<!-- MODAL -->
<div id="modal" class="modal">
    <div class="modal-content relative">
       <button onclick="closeModal()" class="absolute top-2 right-2 bg-red-500 size-8 text-xl  rounded-lg">x</button>
        <h2 id="modal-title" class="text-2xl font-bold uppercase flex justify-center text-sky-500 pb-4"></h2>
        <textarea id="linksArea" style="width:100%; height:400px; color:white; font-family:sans-serif; border:none;" class="bg-gray-900 p-2"></textarea>
        <div class="mt-4 flex justify-center items-center">
            <button onclick="copyAll()" class="bg-sky-600 px-6 py-2  font-bold text-white rounded-lg">COPIAR</button>            
        </div>
    </div>
</div>

<script>

{scripts}

function showModal(title, links) {{
    document.getElementById("modal").style.display = "flex";
    document.getElementById("modal-title").innerText = title;
    document.getElementById("linksArea").value = links.join('\\n');
}}

function closeModal() {{
    document.getElementById("modal").style.display = "none";
}}

const Toast = Swal.mixin({{
  toast: true,
  position: "bottom-end",
  showConfirmButton: false,
  timer: 2000,
  timerProgressBar: true,
  didOpen: (toast) => {{
    toast.onmouseenter = Swal.stopTimer;
    toast.onmouseleave = Swal.resumeTimer;
  }}
}});

function copyAll() {{
    const text = document.getElementById("linksArea").value;
    navigator.clipboard.writeText(text);
    Toast.fire({{ icon: 'success', title: '¡Copiado!' }});
}}

function copyText(text) {{
    navigator.clipboard.writeText(text);
    Toast.fire({{ icon: 'success', title: 'Copiado' }});
}}

</script>

</body>
</html>
"""

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    print("Escaneando imágenes...")

    cartas, portadas = get_data()

    create_html(cartas, portadas)

    total_cartas = sum(len(v) for v in cartas.values())
    total_portadas = len(portadas)

    print(f"Cartas encontradas: {total_cartas}")
    print(f"Portadas encontradas: {total_portadas}")
    print("Se ha generado el archivo 'index.html'.")

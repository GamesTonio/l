import os
import re

# ==========================================
# CONFIGURACIÓN - ASEGÚRATE DE QUE ESTA RUTA SEA CORRECTA
# ==========================================
TARGET_FOLDER = "Cartas/LOL"
# ==========================================

def rename_lol_images():
    if not os.path.exists(TARGET_FOLDER):
        print(f"Error: La carpeta '{TARGET_FOLDER}' no existe. Asegúrate de que la ruta sea correcta.")
        return

    print(f"Iniciando el renombrado de imágenes en '{TARGET_FOLDER}'...")
    for filename in os.listdir(TARGET_FOLDER):
        old_path = os.path.join(TARGET_FOLDER, filename)

        if os.path.isfile(old_path):
            # Expresión regular para encontrar el patrón _XXX_Nombre.ext
            # Captura el "Nombre" y la ".ext"
            match = re.match(r"^_(\d{4})_(.*)(\..+)$", filename)

            if match:
                new_name = match.group(2) + match.group(3) # Combina el nombre y la extensión
                new_path = os.path.join(TARGET_FOLDER, new_name)

                if os.path.exists(new_path):
                    print(f"⚠️ Ya existe un archivo con el nombre '{new_name}', omitiendo el renombrado de '{filename}'.")
                else:
                    os.rename(old_path, new_path)
                    print(f"✔ Renombrado: '{filename}' -> '{new_name}'")
            else:
                print(f"ℹ️ Saltando '{filename}': no coincide con el patrón esperado '_XXX_Nombre.ext'.")
        # Si no es un archivo (ej. es una subcarpeta), simplemente lo ignora.

if __name__ == "__main__":
    rename_lol_images()
    print("Proceso de renombrado terminado.")
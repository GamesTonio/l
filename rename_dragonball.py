import os

# ==========================================
# CONFIGURACIÓN
# ==========================================
TARGET_FOLDER = "Cartas/DragonBall"
# ==========================================

def fix_dragonball_sequence():
    if not os.path.exists(TARGET_FOLDER):
        print(f"Error: La carpeta '{TARGET_FOLDER}' no existe.")
        return

    extensions = ('.jpg', '.jpeg', '.png', '.gif')
    
    # 1. Obtener lista de archivos y ordenarlos alfabéticamente
    # Esto garantiza que '062.jpg' venga antes que '62-2.jpg' o '062-0.jpg'
    files = [f for f in os.listdir(TARGET_FOLDER) if f.lower().endswith(extensions)]
    files.sort()

    print(f"Se encontraron {len(files)} archivos en {TARGET_FOLDER}.")
    print("Iniciando proceso de re-indexación...")

    # 2. Primer paso: Renombrar a nombres temporales
    # Usamos un prefijo "__temp__" para evitar conflictos con archivos existentes
    temp_mapping = []
    for i, filename in enumerate(files, 1):
        ext = os.path.splitext(filename)[1].lower()
        old_path = os.path.join(TARGET_FOLDER, filename)
        
        temp_name = f"__temp_{i:03d}{ext}"
        temp_path = os.path.join(TARGET_FOLDER, temp_name)
        
        os.rename(old_path, temp_path)
        temp_mapping.append((temp_path, f"{i:03d}{ext}"))

    # 3. Segundo paso: Aplicar el nombre final (001, 002, 003...)
    for temp_path, final_name in temp_mapping:
        final_path = os.path.join(TARGET_FOLDER, final_name)
        os.rename(temp_path, final_path)
        print(f"✔ Corregido: {os.path.basename(temp_path)} -> {final_name}")

    print("\n¡Proceso completado!")
    print(f"Ahora tienes una secuencia perfecta del 001 al {len(files):03d}.")

if __name__ == "__main__":
    fix_dragonball_sequence()
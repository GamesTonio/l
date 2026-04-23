import os

BASE_FOLDER = "Cartas"

def pad_number(filename):
    name, ext = os.path.splitext(filename)

    if not name.isdigit():
        return filename  # no tocar si no es número puro

    num = int(name)

    # 3 dígitos (puedes cambiar a 4 si quieres)
    new_name = f"{num:03d}{ext}"
    return new_name


def rename_files():
    for root, dirs, files in os.walk(BASE_FOLDER):
        for file in files:
            old_path = os.path.join(root, file)

            new_file = pad_number(file)

            if new_file == file:
                continue  # ya está bien

            new_path = os.path.join(root, new_file)

            # evitar sobreescribir
            if os.path.exists(new_path):
                print(f"⚠️ Ya existe: {new_file}, se omite")
                continue

            os.rename(old_path, new_path)
            print(f"✔ {file} → {new_file}")


if __name__ == "__main__":
    print("Normalizando nombres...")
    rename_files()
    print("✔ Proceso terminado")
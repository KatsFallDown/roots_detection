# create_folder.py
import os
import sys

def create_folder(folder_name):
    try:
        homework_dir = 'homework'

        full_path = os.path.join(homework_dir, folder_name)
        os.makedirs(full_path, exist_ok=True)  # exist_ok=True не вызовет ошибку, если папка уже существует
        print(f"Папка '{folder_name}' успешно создана в директории '{homework_dir}'!")
    except Exception as e:
        print(f"Ошибка при создании папки: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Ошибка: необходимо указать имя папки как аргумент командной строки.")
        sys.exit(1)
    folder_name = sys.argv[1]
    create_folder(folder_name)

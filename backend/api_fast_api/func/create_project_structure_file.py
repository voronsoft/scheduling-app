import os

# Получаем абсолютный путь к текущему файлу (main.py)
current_file = os.path.abspath(__file__)


# ======================== Создание файла со структурой проекта тип .md
def create_project_structure(root_folder=None, output_file=None):
    """Создание файла со структурой проекта
    
    - Принимает:
        root_folder: -Директорию проекта от которой будет происходить начало построения структуры файлов проекта
        output_file: -Путь к файлу и название для расположения  
    - Результат:
        Создание файла с названием - structure_project.md
        Путь расположения по умолчанию указан в переменной output_file
    """
    # Установка значений по умолчанию, если переменные не переданы.
    root_folder = root_folder or os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    output_file = output_file or os.path.join(root_folder, "structure_project.md")

    with open(output_file, 'w', encoding="utf8") as file:
        file.write("```markdown\n")  # Начало блока кода Markdown

        def walk_directory(folder, indent_level):
            for item in os.listdir(folder):
                item_path = os.path.join(folder, item)
                # Игнорируем папки и их содержимое с названием "__pycache__" и ".venv"
                if item == "__pycache__" or item == ".venv":
                    continue
                if os.path.isdir(item_path):
                    file.write(f"{'│   ' * (indent_level - 1)}├── {item}/\n")
                    walk_directory(item_path, indent_level + 1)
                else:
                    file.write(f"{'│   ' * (indent_level - 1)}├── {item}\n")

            # Добавляем отступы между папками
            file.write(f"{'│   ' * (indent_level - 1)}\n")

        # Получаем имя корневой папки проекта
        root_folder_name = os.path.basename(root_folder)
        file.write(f"{root_folder_name}/\n")
        walk_directory(root_folder, 1)
        file.write("```")  # Завершение блока кода Markdown

import json
import os
from typing import List, TypeVar, Type
from pathlib import Path

T = TypeVar('T')

class JSONService:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)

    def load_data(self, filename: str, model_class: Type[T]) -> List[T]:
        """Загрузка данных из JSON файла"""
        file_path = self.data_dir / filename

        # Если файл не существует, создаем пустой список
        if not file_path.exists():
            self.save_data(filename, [])
            return []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return [model_class.from_dict(item) for item in data]
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Ошибка загрузки данных из {filename}: {e}")
            return []

    def save_data(self, filename: str, data: List[T]):
        """Сохранение данных в JSON файл"""
        file_path = self.data_dir / filename

        try:
            # Преобразуем объекты в словари
            data_dicts = [item.to_dict() for item in data]

            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data_dicts, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения данных в {filename}: {e}")
            raise
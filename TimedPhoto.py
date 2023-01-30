import datetime
import re

# Модель файла фото с атрибутами даты его создания
class TimedPhoto:
    file_name: str

    timestamp: datetime.datetime

    def __init__(self, file_name: str):
        self._validate_file_name(file_name)
        self.file_name = file_name
        self._parseTimestamp()

    # Валидация имени файла по регулярке
    def _validate_file_name(self, file_name: str):
        if not re.match(r'^\d{8}_\d{6}.(jpg|jpeg|png)$', file_name) != None:
            raise Exception(f'Файл имеет некорректное имя "{file_name}"')

    def getNameWithoutExtension(self):
        return self.file_name[0:15]

    # Парсим дату из имени файла
    def _parseTimestamp(self):
        name = self.getNameWithoutExtension()
        self.timestamp = datetime.datetime.strptime(name, '%Y%m%d_%H%M%S')

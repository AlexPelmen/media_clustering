import os
from typing import List
from TimedPhoto import TimedPhoto
from config import DATA_PATH


# класс для получения файлов из папки исходников
class Provider:
    _photos: List[str] = []
    _videos: List[str] = []

    # Геттер для путей фоток
    def getPhotos(self) -> List[str]:
        return self._photos

    # Геттер для путей видео
    def getVideos(self) -> List[str]:
        return self._videos

    # Подгружаем имена файлов из папки
    def loadFiles(self):
        file_names = self.getFileNames()
        self.populatePhotosAndVideos(file_names)

    # Получение списка файлов из директории с фотками
    def getFileNames(self) -> List[str]:
        try:
            return os.listdir(DATA_PATH)
        except:
            print('Не удалось получить файлы по пути' + DATA_PATH)
            exit(1)

    # Заполняем атрибуты класса именами файлов фоток и видосов
    def populatePhotosAndVideos(self, names: List[str]):
        for fullname in names:
            name: str
            ext: str
            name, ext = fullname.split('.')
            if ext in ['jpg', 'jpeg', 'png']:
                self._photos.append(fullname)
            if (ext == 'mp4'):
                self._videos.append(fullname)

    # Создаем модели файлов фоток
    def getPhotoTimedModels(self) -> List[TimedPhoto]:
        return list(map(lambda file_name: TimedPhoto(file_name), self._photos))

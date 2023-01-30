import os
import shutil
from typing import List

from PhotoCluster import PhotoCluster
from config import TARGET_PATH, VIDEO_DIRECTORY, PHOTO_DIRECTORY, DATA_PATH


# класс для сохранения файлов и работы с папками
class Saver:

    def __init__(self):
        if not self._isTargetDirEmpty():
            print('Целевая директория не пустая')
            exit(1)

        self._createFolders()

    # создание папок под фотки и видео
    def _createFolders(self):
        print('Создание директорий под фото и видео')
        photos = TARGET_PATH + '/' + VIDEO_DIRECTORY
        videos = TARGET_PATH + '/' + PHOTO_DIRECTORY
        if not os.path.exists(photos): os.mkdir(photos)
        if not os.path.exists(videos): os.mkdir(videos)

    def _isTargetDirEmpty(self):
        return not bool(os.listdir(TARGET_PATH))

    # Копирует файл в папку с видео
    def saveVideo(self, file_name):
        src = DATA_PATH + '/' + file_name
        destination = '/'.join([TARGET_PATH, VIDEO_DIRECTORY, file_name])
        print(f'Сохранение видео в {destination}')
        shutil.copy(src, destination)

    # Скопировать видео по списку имен
    def saveVideos(self, file_names: List[str]):
        for name in file_names:
            self.saveVideo(name)

    # создание директории под конкретный кластер
    def _createClusterFolder(self, cluster: PhotoCluster):
        path = '/'.join([TARGET_PATH, PHOTO_DIRECTORY, cluster.getName()])
        print(f'Создание директории {path}')
        os.mkdir(path)

    # простое копирование фотки
    def _savePhoto(self, old_path: str, new_path: str):
        print(f'Сохранение изображения в {new_path}')
        shutil.copy(old_path, new_path)

    # сохранение кластера фотографий
    def saveCluster(self, cluster: PhotoCluster):
        print(f'Сохранение кластера {cluster.getName()}')
        self._createClusterFolder(cluster)
        for photo in cluster.photos:
            src =  DATA_PATH + '/' + photo.file_name
            destination = '/'.join([TARGET_PATH, PHOTO_DIRECTORY, cluster.getName(), photo.file_name])
            self._savePhoto(src, destination)

    # сохранение списка кластеров
    def saveClusters(self, clusters: List[PhotoCluster]):
        for cluster in clusters:
            self.saveCluster(cluster)

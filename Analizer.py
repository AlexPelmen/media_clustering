import typing
from typing import List

from DefaultPhotoCluster import DefaultPhotoCluster
from PhotoCluster import PhotoCluster
from TimedPhoto import TimedPhoto
from config import CLUSTER_TIME_THRESHOLD, CLUSTER_MIN_PHOTO_NUMBER


# класс для получения файлов из папки исходников
class Analizer:
    clusters: List[PhotoCluster]

    # последнее фото, которое мы обрабатывали
    _last_photo: typing.Optional[TimedPhoto]

    # текущий кластер, который мы сейчас собираем
    _currentCluster: PhotoCluster

    # Кластер для фоток, которые не попали в осноные кластеры
    _defaultCluster: DefaultPhotoCluster

    def __init__(self):
        self._clear()

    # очистка атрибутов (подготовка к повторному анализу)
    def _clear(self):
        self.clusters = []
        self._last_photo = None
        self._currentCluster = PhotoCluster()
        self._defaultCluster = DefaultPhotoCluster()

    # добавление фотки к текущему кластеру
    # запоминаем ее в буфер как предыдущую
    def _addToCluster(self, photo: TimedPhoto):
        self._currentCluster.add(photo)
        self._last_photo = photo

    # сохраняем старый кластер в коллекцию и создаем новый
    def _storeCluster(self):
        self.clusters.append(self._currentCluster)
        self._currentCluster = PhotoCluster()

    # время между фотками отличается больше определенного порога?
    def _isTimeSeparated(self, photo: TimedPhoto) -> bool:
        if not self._last_photo: return False
        delta: int = int(round(photo.timestamp.timestamp() - self._last_photo.timestamp.timestamp()))
        return delta > CLUSTER_TIME_THRESHOLD

    # Количество фоток в кластере больше порогового значения?
    def _clusterHasEnoughPhotos(self) -> bool:
        return self._currentCluster.getLength() >= CLUSTER_MIN_PHOTO_NUMBER

    # Проверка условия разделения кластеров
    def _needToSplit(self, photo: TimedPhoto) -> bool:
        return self._isTimeSeparated(photo) and self._clusterHasEnoughPhotos()

    # Нужно ли перенести фотки в общий кластер?
    # Если между фотками есть разрыв по времени, но при в кластере недостаточно фоток,
    # то мы просто отправляем все это в общий кластер
    def _needToStoreInCommonCluster(self, photo: TimedPhoto) -> bool:
        return self._isTimeSeparated(photo) and not self._clusterHasEnoughPhotos()

    # Сохраняем фотки из текущего кластера в общем.
    # Текущий кластер пересоздаем
    def _storeInCommonCluster(self):
        self._defaultCluster.addClusterInner(self._currentCluster)
        self._currentCluster = PhotoCluster()

    # разбитие списка фоток на кластеры
    def split_photos_to_clusters(self, photos: List[TimedPhoto]) -> List[PhotoCluster]:
        self._clear()

        for photo in photos:
            if self._needToSplit(photo):
                self._storeCluster()
            if self._needToStoreInCommonCluster(photo):
                self._storeInCommonCluster()
            self._addToCluster(photo)

        self.clusters.append(self._defaultCluster)

        # обрабатываем последний кластер
        if self._clusterHasEnoughPhotos():
            self._storeCluster()
        else:
            self._storeInCommonCluster()

        return self.clusters

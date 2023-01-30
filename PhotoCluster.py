from typing import List
from TimedPhoto import TimedPhoto
from config import CLUSTER_PREFIX


# Кластер фоток
class PhotoCluster:
    photos: List[TimedPhoto]

    def __init__(self):
        self.photos = []

    # Добавить фото к кластеру
    def add(self, photo: TimedPhoto):
        self.photos.append(photo)

    # В постфиксе будут имена первого и последнего файла
    def _getDatePostfix(self):
        if not bool(len(self.photos)): return
        first_photo = self.photos[0].getNameWithoutExtension()
        last_photo = self.photos[-1].getNameWithoutExtension()
        return f'{first_photo}-{last_photo}'

    # Получение названия кластера
    def getName(self):
        return CLUSTER_PREFIX + '_' + self._getDatePostfix()

    # Получить мощность кластера
    def getLength(self):
        return len(self.photos)

    # Добавить фотки из переданного кластера в текущий
    def addClusterInner(self, cluster):
        self.photos = self.photos + cluster.photos

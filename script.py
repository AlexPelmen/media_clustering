from typing import List
from Analizer import Analizer
from Provider import Provider
from Saver import Saver
from TimedPhoto import TimedPhoto

print('Получение списка файлов')
provider: Provider = Provider()
provider.loadFiles()
videos: List[str] = provider.getVideos()
photos: List[TimedPhoto] = provider.getPhotoTimedModels()

print(f'Найдено {len(photos)} фотографий')
print(f'Найдено {len(videos)} видео')

print('Разбиение на кластеры')
analizer: Analizer = Analizer()
clusters = analizer.split_photos_to_clusters(photos)

print('Копирование файлов в целевую директорию')
saver: Saver = Saver()
saver.saveClusters(clusters)
saver.saveVideos(videos)

print('Успешно завершено!')

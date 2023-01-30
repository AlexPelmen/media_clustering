from PhotoCluster import PhotoCluster


# Общий кластер фоток
class DefaultPhotoCluster(PhotoCluster):

    # Получение названия кластера
    def getName(self):
        return 'default'
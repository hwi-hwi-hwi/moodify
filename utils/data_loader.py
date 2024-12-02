import os
from tensorflow.keras.preprocessing.image import ImageDataGenerator


def load_fer2013_data(dataset_path, target_size=(48, 48), batch_size=32, validation_split=0.2):
    """
    FER2013 데이터셋 로드 및 전처리 함수.

    Args:
        dataset_path (str): 데이터셋이 저장된 디렉토리 경로.
        target_size (tuple): 이미지 크기 (가로, 세로).
        batch_size (int): 배치 크기.
        validation_split (float): 검증 데이터 비율.

    Returns:
        train_data (DirectoryIterator): 학습 데이터.
        validation_data (DirectoryIterator): 검증 데이터.
    """
    datagen = ImageDataGenerator(
        rescale=1. / 255,
        validation_split=validation_split
    )

    train_data = datagen.flow_from_directory(
        dataset_path,
        target_size=target_size,
        batch_size=batch_size,
        class_mode='categorical',
        subset='training'
    )

    validation_data = datagen.flow_from_directory(
        dataset_path,
        target_size=target_size,
        batch_size=batch_size,
        class_mode='categorical',
        subset='validation'
    )

    return train_data, validation_data

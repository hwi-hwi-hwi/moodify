import os
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization, Activation
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix

def create_emotion_model(input_shape=(48, 48, 1), num_classes=7):
    """
    감정 인식 CNN 모델 생성 함수.
    """
    model = Sequential()

    model.add(Conv2D(32, kernel_size=(3, 3), padding='same', input_shape=input_shape))
    model.add(BatchNormalization())
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Conv2D(64, (3, 3), padding='same'))
    model.add(BatchNormalization())
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Conv2D(128, (3, 3), padding='same'))
    model.add(BatchNormalization())
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Flatten())
    model.add(Dense(256, activation='relu'))
    model.add(Dropout(0.3))  # Dropout 비율 수정
    model.add(Dense(num_classes, activation='softmax'))

    return model

if __name__ == "__main__":
    base_dir = os.path.join(os.path.dirname(__file__), '..', 'datasets', 'fer2013')
    train_dir = os.path.join(base_dir, 'train')
    test_dir = os.path.join(base_dir, 'test')

    # 데이터 로드 및 증강
    train_datagen = ImageDataGenerator(
        rescale=1.0 / 255.0,
        rotation_range=10,
        width_shift_range=0.1,
        height_shift_range=0.1,
        horizontal_flip=True
    )

    test_datagen = ImageDataGenerator(rescale=1.0 / 255.0)

    train_data = train_datagen.flow_from_directory(
        train_dir,
        target_size=(48, 48),
        batch_size=32,
        class_mode='categorical'
    )

    test_data = test_datagen.flow_from_directory(
        test_dir,
        target_size=(48, 48),
        batch_size=32,
        class_mode='categorical'
    )

    # 모델 생성 및 학습
    model = create_emotion_model(input_shape=(48, 48, 3))
    model.compile(optimizer=Adam(learning_rate=0.0005),  # 학습률 감소
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    # 콜백 설정
    model_checkpoint = ModelCheckpoint('emotion_model.keras', monitor='val_loss', save_best_only=True, verbose=1)
    early_stopping = EarlyStopping(monitor='val_loss', patience=10, verbose=1)
    reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.1, patience=5, verbose=1)

    history = model.fit(
        train_data,
        epochs=25,
        validation_data=test_data,
        callbacks=[model_checkpoint, early_stopping, reduce_lr]
    )

    # 모델 저장
    print("최종 모델 저장 완료: emotion_model.keras")

    # 학습 결과 시각화
    plt.figure(figsize=(12, 6))
    plt.plot(history.history['accuracy'], label='Train Accuracy')
    plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
    plt.legend()
    plt.title('Training vs Validation Accuracy')
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.show()

    # Confusion Matrix 출력
    y_pred = model.predict(test_data)
    y_pred_classes = np.argmax(y_pred, axis=1)
    y_true = test_data.classes

    cm = confusion_matrix(y_true, y_pred_classes)
    print("Confusion Matrix")
    print(cm)

    print("Classification Report")
    print(classification_report(y_true, y_pred_classes))

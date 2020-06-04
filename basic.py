# -*- coding: utf-8 -*-
"""basic.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1SY_3qQIHDtjY1qcFbK4O54SM4zvm251x
"""

#Senior Project
#MustafaGultekin - MertCihangiroglu
import os
import zipfile
import tensorflow as tf
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.preprocessing.image import ImageDataGenerator

base_dir = '/content/drive/My Drive/datasett'
train_dir = os.path.join(base_dir, 'train')
validation_dir = os.path.join(base_dir, 'test')

model = tf.keras.models.Sequential([
    tf.keras.layers.Conv2D(16, (3,3), activation='relu', input_shape=(256, 256, 3)),
    tf.keras.layers.Conv2D(16, (3,3), activation='relu'),
#    tf.keras.layers.Conv2D(16, (3,3), activation='relu'),
    
    tf.keras.layers.MaxPooling2D(2, 2),
#    tf.keras.layers.Dropout((0.5)),
    tf.keras.layers.Conv2D(32, (3,3), activation='relu'),
    tf.keras.layers.Conv2D(32, (3,3), activation='relu'),
#    tf.keras.layers.Conv2D(32, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Flatten(),
#    tf.keras.layers.Dropout((0.5)),
    tf.keras.layers.Dense(20, activation = 'relu'),
#    tf.keras.layers.Dropout((0.2)),
    tf.keras.layers.Dense(7, activation='softmax')
])

model.summary()
model.compile(loss='categorical_crossentropy',
              optimizer="adam",
              metrics=['accuracy'])

# All images will be rescaled by 1./255
train_datagen = ImageDataGenerator(rescale=1./255)
test_datagen = ImageDataGenerator(rescale=1./255)

# Flow training images in batches of 20 using train_datagen generator
train_generator = train_datagen.flow_from_directory(
        train_dir,  # This is the source directory for training images
        target_size=(100, 100),  # All images will be resized
        batch_size=20,
        # Since we use binary_crossentropy loss, we need binary labels
        class_mode='categorical')

# Flow validation images in batches of 20 using test_datagen generator
validation_generator = test_datagen.flow_from_directory(
        validation_dir,
        target_size=(256, 256),
        batch_size=10,
        shuffle = False,
        class_mode='categorical')

history = model.fit(
      train_generator,
      steps_per_epoch=23,  # total images = batch_size * steps
      epochs=30,
      validation_data=validation_generator,
      validation_steps=20  # total images = batch_size * steps
      )

import numpy as np
from sklearn.metrics import classification_report, confusion_matrix
Y_pred = model.predict_generator(validation_generator,6)
y_pred = np.argmax(Y_pred, axis=1)
print('Confusion Matrix')
print(confusion_matrix(validation_generator.classes, y_pred))
print(validation_generator.classes)
print('Classification Report')
target_names = ['Angry', 'Disgust', 'Fear', "Happy", "Neutral", "Sad", "Surprise"]
print(classification_report(validation_generator.classes, y_pred, target_names=target_names))


import tensorflow as tf
#from tfx import v1 as tfx
#print('TFX version: {}'.format(tfx.__version__))
import numpy as py
import datetime
import tensorflow_datasets as tfds
import matplotlib.pyplot as plt


dataset, metadata = tfds.load('wider_face', as_supervised=True, with_info=True)
train_dataset, test_dataset, validation_dataset = dataset['train'], dataset['test'], dataset['validation']

def normalize(images, labels):
  images = tf.cast(images, tf.float32)
  images /= 255
  return images, labels

# The map function applies the normalize function to each element in the train
# and test datasets
train_dataset =  train_dataset.map(normalize)
test_dataset  =  test_dataset.map(normalize)
validation_dataset = validation_dataset.map(normalize)

# The first time you use the dataset, the images will be loaded from disk
# Caching will keep them in memory, making training faster
train_dataset =  train_dataset.cache()
test_dataset  =  test_dataset.cache()
validation_dataset = validation_dataset.cache()

#defining model. Flatten Layer is for converting the image and video to readable data for the model.
#Dense Layer is for processing the data.
#Last Dense Layer creates the output and optimizes the Result
def create_model():
    return tf.keras.models.Sequential([
       tf.keras.layers.Conv2D(32, (3,3), padding='same', activation=tf.nn.relu,
                           input_shape=(28, 28, 1)),
        tf.keras.layers.MaxPooling2D((2, 2), strides=2),
        tf.keras.layers.Conv2D(64, (3,3), padding='same', activation=tf.nn.relu),
        tf.keras.layers.MaxPooling2D((2, 2), strides=2),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(1024, activation=tf.nn.relu),
        tf.keras.layers.Dense(61, activation=tf.nn.softmax)
  ])
    
model = create_model()

#compiles the model and defines the optimizer and loss optimzer.
model.compile(optimizer = 'RMSprop',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

log_dir = "logs/fit" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)



#Set up summary writers to write the summaries to disk in a different logs directory. The folders will be created:
current_time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
train_log_dir = 'logs/gradient_tape/' + current_time + '/train'
test_log_dir = 'logs/gradient_tape/' + current_time + '/test'
validation_log_dir = 'logs/gradient_tape' + current_time + '/validation'
train_summary_writer = tf.summary.create_file_writer(train_log_dir)
test_summary_writer = tf.summary.create_file_writer(test_log_dir)

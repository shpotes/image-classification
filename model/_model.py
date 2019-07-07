import json

import tensorflow as tf
import pandas as pd

from model.dataset import *
from tensorflow.keras.callbacks import *

class _Model:
    def __init__(self, config, overfit_mode=False):
        self.config = config
        self.overfit_mode = overfit_mode
        self.metadata = pd.read_csv(self.config['model']['metadata_path'])
        self.model = self.build_model()
        self.load_data(self.overfit_mode)

    def __str__(self):
        string = [self.__class__.__name__, '']
        self.model.summary(print_fn=lambda x: string.append(x))
        return '\n'.join(string)

    def build_model(self):
        pass
    
    def callbacks(self):
        return []

    def optimizer(self, *args, **kwargs):
        return tf.optimizers.Adam(*args, **kwargs)

    def metrics(self):
        return ['accuracy']

    def loss(self, *args, **kwargs):
        return tf.losses.CategoricalCrossentropy(*args, **kwargs)

    def preprocess(self, img, label):
        size = self.config['model']['input_size']
        num_classes = len(self.config['model']['labels'])
        img = tf.image.resize(img, size)
        img /= 255.0
        y = tf.one_hot(indices=label, depth=num_classes)
        return img, y

    def load_weights(self, weight_path):
        self.model.load_weights(weight_path)

    def load_data(self, overfit_mode):
        self.train_data, self.val_data, self.test_data = create_data(self, overfit_mode)

    def train(self):
        self.load_data(self.overfit_mode)

        LR = self.config['train']['learning_rate']
        NUM_EPOCHS = self.config['train']['over_epochs'] \
            if self.overfit_mode else self.config['train']['num_epochs']

        self.model.compile(loss=self.loss(),
                           optimizer=self.optimizer(LR),
                           metrics=self.metrics())

        return self.model.fit(self.train_data, epochs=NUM_EPOCHS,
                              validation_data=self.val_data,
                              callbacks=self.callbacks())

    def evaluate(self):
        self.load_data(self.overfit_mode)
        print('train')
        self.model.evaluate(self.train_data)
        print('test')
        self.model.evaluate(self.test_data)

    def predict(self, ds):
        return self.model.predict(ds)

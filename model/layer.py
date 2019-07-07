import tensorflow as tf
from tensorflow.keras.layers import add, Layer, BatchNormalization, Conv2D

class ResBlock(Layer):
    def __init__(self, filtes, kernel_size, bottleneck=0):
        super(ResBlock, self).__init__()
        self.bn1 = BatchNormalization()
        self.conv1 = Conv2D(filters, kernel_size, padding='same')
        self.bn2 = BatchNormalization()
        self.conv2 = Conv2D(filters, kernel_size, padding='same')
        
        self.bottleneck = Conv2D(bottleneck, (1, 1), padding='same') \
            if bottleneck else lambda x: x

    def call(self, inputs):
        shortcut = x
        
        x = self.bn1(x)
        x = tf.nn.relu(x)
        x = self.conv1(x)
        x = self.bn2(x)
        x = tf.nn.relu(x)
        x = self.conv2(x)

        self.bottleneck(shortcut)

        x = add([shortcut, x])
        return x

import tensorflow as tf

from model.triplet_model import TripletModel


class ModelV1(TripletModel):

    def __init__(self, config):
        super().__init__(config)


    def model(self, X, is_training, keep_prob):
        # mask = X

        # CONV L1
        X = self.conv2d(X, scope="CONV_1", filter=32, kernel_size=3, strides=1, padding="same", batch_norm=True, activation=tf.nn.relu, is_training=is_training)
        X = tf.layers.max_pooling2d(X, pool_size=2, strides=2)
        # mask = tf.layers.max_pooling2d(mask, pool_size=2, strides=2)
        # X = tf.cast(tf.greater(mask, 0), tf.float32) * X

        # INCEPTION L2
        X = self.inception_v2(input=X, scope="INCEPTION_2a", filters=64, batch_norm=True, activation=tf.nn.relu, is_training=is_training)
        X = self.inception_v2(input=X, scope="INCEPTION_2b", filters=64, batch_norm=True, activation=tf.nn.relu, is_training=is_training)
        X = tf.layers.max_pooling2d(X, pool_size=2, strides=2)
        # mask = tf.layers.max_pooling2d(mask, pool_size=2, strides=2)
        # X = tf.cast(tf.greater(mask, 0), tf.float32) * X

        # INCEPTION L3
        X = self.inception_v2(input=X, scope="INCEPTION_3a", filters=128, batch_norm=True, activation=tf.nn.relu, is_training=is_training)
        X = self.inception_v2(input=X, scope="INCEPTION_3b", filters=128, batch_norm=True, activation=tf.nn.relu, is_training=is_training)
        X = tf.layers.max_pooling2d(X, pool_size=3, strides=2, padding="same")
        # mask = tf.layers.max_pooling2d(mask, pool_size=3, strides=2, padding="same")
        # X = tf.cast(tf.greater(mask, 0), tf.float32) * X

        # INCEPTION L4
        X = self.inception_v2(input=X, scope="INCEPTION_4a", filters=256, batch_norm=True, activation=tf.nn.relu, is_training=is_training)
        X = self.inception_v2(input=X, scope="INCEPTION_4b", filters=256, batch_norm=True, activation=tf.nn.relu, is_training=is_training)
        X = self.inception_v2(input=X, scope="INCEPTION_4c", filters=256, batch_norm=True, activation=self.maxout_activation(128), is_training=is_training)
        X = tf.layers.max_pooling2d(X, pool_size=3, strides=2, padding="same")

        # Ave pool
        X = tf.layers.average_pooling2d(X, pool_size=(9, 3), strides=1)

        # flatten
        X = tf.layers.flatten(X)

        # # FC1
        # X = self.dense(X, name="FC1", units=512, activation=self.maxout_activation(128), keep_prob=keep_prob)

        # Output
        X = tf.nn.l2_normalize(X, axis=-1)
        return X


class Model(ModelV1):
    def __init__(self, config):
        super().__init__(config)

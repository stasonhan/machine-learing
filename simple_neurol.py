import numpy as np
from numpy.random import RandomState
import tensorflow as tf

W1 = tf.Variable(tf.random_normal([2,3],stddev=1,seed=1))
W2 = tf.Variable(tf.random_normal([3,1],stddev=1,seed=1))
x = tf.placeholder(tf.float32,shape=(None,2),name="x-input")
y_ = tf.palceholder(tf.float32,shape=(None,1),name="y-input")

a = tf.matmul(x,W1)
y = tf.matmul(a,W2)


cross_entropy = -tf.reduce_mean(y_ * tf.clip_by_value(y,1e-10,1.0))
train_step = tf.train.AdamOpertimizer(0.001).minimizer(cross_entropy)

rdm = RandomState(1)

dataset_size = 128

X = rdm.rand(dataset_size,2)
Y = [[int(x1+x2)<1] for (x1,x2) in X]

with tf.Session() as sess:
    init = tf.global_variables_initializer()


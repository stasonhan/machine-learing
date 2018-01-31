import numpy as np
from numpy.random import RandomState
import tensorflow as tf

batch_size = 8

W1 = tf.Variable(tf.random_normal([2,3],stddev=1,seed=1))
#W2 = tf.Variable(tf.random_normal([3,1],stddev=1,seed=1))
x = tf.placeholder(tf.float32,shape=(None,2),name="x-input")
y_ = tf.placeholder(tf.float32,shape=(None,1),name="y-input")

#a = tf.matmul(x,W1)
y = tf.matmul(x,W1)

loss_less = 10
loss_more = 1

loss = tf.reduce_sum(tf.where(tf.greater(y,y_),(y-y_)*loss_more,(y_-y)*loss_less))

#cross_entropy = -tf.reduce_mean(y_ * tf.log(tf.clip_by_value(y,1e-10,1.0)))
train_step = tf.train.AdamOptimizer(0.001).minimize(loss)

rdm = RandomState(1)

dataset_size = 128
#generate 128*2 matrix
X = rdm.rand(dataset_size,2)
Y = [[x1 + x2 + rdm.rand()/10.0-0.05] for (x1,x2) in X]

with tf.Session() as sess:
    init = tf.global_variables_initializer()
    sess.run(init)

    STEPS = 5000
    for i in range(STEPS):
        start = (i * batch_size) % dataset_size
        end = min(start + batch_size,dataset_size) 
        sess.run(train_step,feed_dict={x:X[start:end],y_:Y[start:end]})
          
    print sess.run(W1)

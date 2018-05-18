import numpy as np
import tensorflow as tf

input_data = tf.Variable(np.random.rand(1, 3), dtype=tf.float32)
# np.random.rand()传入一个shape,返回一个在[0,1)区间符合均匀分布的array

output = tf.nn.sigmoid_cross_entropy_with_logits(logits=input_data, labels=[[1.0, 0.0, 0.0]])
with tf.Session() as sess:
    init = tf.global_variables_initializer()
    sess.run(init)
    print(sess.run(output))

import numpy as np
import tensorflow as tf
import datetime

#Processing Units logs
log_device_placement = True

#num of multiplications to perform
n = 10
# Example: compute A^n + B^n on 2 GPUs

# Create random large matrix
A = np.random.rand(1000, 1000).astype('float32')
B = np.random.rand(1000, 1000).astype('float32')

# Creates a graph to store results
c1 = []
c2 = []
# Define matrix power
def matpow(M, n):
    if n < 1: #Abstract cases where n < 1
        return M
    else:
        return tf.matmul(M, matpow(M, n-1))
with tf.device('/cpu:0'):
    a = tf.constant(A)
    b = tf.constant(B)
    #compute A^n and B^n and store results in c1
    c1.append(matpow(a, n))
    c1.append(matpow(b, n))
    sum = tf.add_n(c1)
    
t1_1 = datetime.datetime.now()
with tf.Session(config=tf.ConfigProto(log_device_placement=log_device_placement)) as sess:
    # Runs the op.
    sess.run(sum)
t2_1 = datetime.datetime.now()
print "time consum ", str(t2_1-t1_1)


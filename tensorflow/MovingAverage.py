#!/usr/bin/python

import tensorflow as tf

v1 = tf.Variable(0,dtype=tf.float32)

step = tf.Variable(0,trainable=False)
ema = tf.train.ExponentialMovingAverage(0.99,step)
maintain_averages_op = ema.apply([v1])

with tf.Session() as sess:
    # initial all variables
    init_op = tf.global_variables_initializer()
    sess.run(init_op)
    #print "v1 initial value ",sess.run(v1)
    print "v1 initail value,ema.average ",sess.run([v1,ema.average(v1)])
    #v1 set to 5 
    sess.run(tf.assign(v1,5))
    #modify v1 slide value the decay is min{0.99,(1+step)/(10+step)=0.1}=0.1,
    #so the slide value of v1 is modified to 0.1*0+0.9*5=4.5
    sess.run(maintain_averages_op)
    print sess.run([v1,ema.average(v1)])
    
    sess.run(tf.assign(step,10000))
    sess.run(tf.assign(v1,10))
    
    sess.run(maintain_averages_op)
    print sess.run([v1,ema.average(v1)])
    
    sess.run(maintain_averages_op)
    print sess.run([v1,ema.average(v1)])
    
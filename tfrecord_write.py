import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
import numpy as np 

def _int64_feature(value):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))
def _bytes_feature(value):
  return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

mnist = input_data.read_data_sets(
        "/home/dev/code/mnist",dtype=tf.uint8,one_hot=True)
images = mnist.train.images
labels = mnist.train.labels
pixels = images.shape[1]
import pdb;pdb.set_trace()
#print pixels
num_examples = mnist.train.num_examples
filename = "/tmp/out_put.tfrecords"
writer = tf.python_io.TFRecordWriter(filename)
for index in range(num_examples):
    #numpy.ndarry.tostring function
    image_raw = images[index].tostring()
    #print labels[index]
    print  np.argmax(labels[index])
    
    
    
    example = tf.train.Example(features=tf.train.Features(feature={
             'pixels':_int64_feature(pixels),
             'label': _int64_feature(np.argmax(labels[index])),
             'image_raw':_bytes_feature(image_raw)
}))
    writer.write(example.SerializeToString())
writer.close()

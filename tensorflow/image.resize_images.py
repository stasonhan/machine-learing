import tensorflow as tf 
#import matplotlib.pyplot as plt

image_raw_data = tf.gfile.FastGFile("/home/dev/gitcode/transfer_learning/flower_photos/daisy/4654579740_6671a53627_m.jpg",
                                   "r" ).read()
with tf.Session() as sess:
    import pdb;pdb.set_trace()
    img_data = tf.image.decode_jpeg(image_raw_data)
    print img_data.eval().shape
    resized = tf.image.resize_images(img_data,[300,300],method=0)
    print img_data.shape

from tensorflow.examples.tutorials.mnist import input_data

mnist = input_data.read_data_sets("/home/dev/code/mnist",one_hot = True)
print "Training data size: ", mnist.train.num_examples

print "Validation data size: ", mnist.validation.num_examples


#!/usr/bin/python
#-*-coding : utf-8 -*-

import tensorflow as tf
INPUT_NODE = 784
OUTPUT_NODE = 10
LAYEER1_NODE = 500

def get_weight_variable(shape,regularizer):
    weights = tf.get_variable(
	"weights",shape,
	initializer=tf.truncate_normal_initializer(stddev=0.1))
	
	if regularizer != None:
	    tf.add_to_collection('losses',regularizer(weights))
	return weights
	
def inference(input_tensor,regularizer):
    with tf.variables_scope('layer1'):
	    weights=get_weight_variable(
		        [INPUT_NODE,LAYEER1_NODE],regularizer)
		biases = tf.get_variable("biases",[LAYEER1_NODE],
		                        initializer=tf.constant_initilizer(0.0))
		layer1= tf.nn.relu(tf.matmul(input_tensor,weights)+biases)
		
	with tf.variables_scope('layer2'):
	    weights = get_weight_variable(
		        [LAYEER1_NODE,OUTPUT_NODE],regularizer)
		biases = tf.get_variable(
		            "biases",[OUTPUT_NODE],
					initializer=tf.constant_initilizer(0.0))
		layer2 = tf.matmul(layer1,weights) + biases
	return layer2
	

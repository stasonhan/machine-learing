#!/usr/bin/python
#-*-coding : utf-8 -*-

import tensorflow as tf
import os

from tensorflow.examples.tutorials.mnist import input_data

import mnist_inference

BATCH_SIZE = 100

LEARNING_RATE_BASE = 0.8

LEARNING_RATE_DECAY = 0.99

REGULARIZATION_RATE = 0.0001
TRAINING_STEPS = 30000
MOVING_AVERAGE_DECAY = 0.99

MODEL_SAVE_PATH = "/home/dev/save/"
MODEL_NAME = "model.ckpt"

def train(mnist):
    x = tf.placeholder(
	    tf.float32,[None,mnist_inference.INPUT_NODE],name='x-input')
	y_ = tf.placeholder(
	     tf.float32,[None,mnist_inference.OUTPUT_NODE],name='y-input')
	
	regularizer = tf.contrib.layers.l2_regularizer(REGULARIZATION_RATE)
	
	y = mnist_inference.inference(x,regularizer)
	gloa
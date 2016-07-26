#!/usr/bin/python

#-*- codin: utf-8 -*-

"""
This script is a simple example for three layer neural net
"""
import numpy as np

def nonlin(x,deriv=False):
    if (deriv = True):
        return x*(1-x)
    return 1/(1 + np.exp(-X))

X = np.array([[0,0,1],
              [0,1,1],
              [1,0,1],
              [1,1,1]]
             )
y = np.array([[0],
              [1],
              [1],
              [0]
              ])


def train(X,Y,maxCycle):
    """ 
    """
    m,n = X.shape()
    np.random.seed(1)
    #assert(m == Y.shape()[0])
    syn0 = 2*np.random.random((n,m)) - 1 # the first layer param w0*
    syn1 = 2*np.random.random((m,1)) - 1 # the second layer param w1*
    for i in range(maxCycle):
        l0 = X
        l1 = nonlin(np.dot(l0,syn0)) # <x,syn0>
        l2 = nonlin(np.dot(l1,syn1)) #

        l2_error = Y - l2
        if ( i > int(maxCycle/6)):
            print "Error:" + str(np.mean(np.abs(l2_error)))

        l2_delta = l2_error * nonlin(l2,deriv=True)
        l1_error = l2_delta.dot(syn1.T)
        l1_delta = l1_error * nonlin(l1,deriv=True)
        syn1 += l1.T.dot(l1_delta)
        syn0 += l0.T.dot(l1_delta)
    return syn0,syn1


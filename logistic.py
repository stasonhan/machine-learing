#!/usr/bin/python
"""
This script is for logistic 
"""
import numpy as np
import os
def loadData(directory):
    """
    """
    trainfileList = listdir(directory)
    m = len(trainfileList)
    dataArray = np.zeros((m,1024))
    labelArray = np.zeros((m,1))
    for i in range(m):
        returnArray = np.zeros((1,1024))
        filename = trainfileList[i]
        fr = open("%s/%s" % (directory,filename))
        for j in range(32):
            lineStr = fr.readline()
            for k in range(32):
                returnArray[0,j * 32 + k] = lineStr[k]
        dataArray[i,:]=returnArray
        fr.close()
        labelArray[i:]=int(filename.split('_')[0])

    return dataArray,labelArray

def sigmoid(inX):
    """
    """
    return 1.0/(1 + np.exp(-inX))


def gradAscent(dataArray,labelArray,algha,maxCycle):
    """
    """
    dataMat = np.mat(dataArray) # size m * n
    labelMat = np.mat(labelArray)# size m * 1
    m,n = np.shape(dataMat)
    weigh = np.ones((n,1))    #size n* 1
    for i in range(maxCycle):
        h = sigmoid(dataMat * weigh)
        error = labelArray - h
        weigh = weigh + algha * dataMat.transpose()*error
    return weigh
    
def classfy(testdir,weigh):
    dataMat,labelArray = loadData(testdir)
    dataMat = mp.mat(dataArray)
    labelArray = np.mat(labelArray)
    h = sigmoid(dataMat*weigh)
    m = len(h)
    for i in range(m):
        if int(h[i]) > 0.5:
            print int(labelMat[i]),'is classfied as :1'
            if int(labelMat[i]) != 1:
                error += 1
                print 'error'
        else:
            print int(labelMat[i]),'is classfied as :0'
            if int(labelMat[i]) != 0:
                error += 1
                print 'error'
    print 'error rate is : ','%.4f' %(error/m)


import numpy as np
from random import random


class Neural_Network(object):
    def __init__(self, inputSize: int, hiddenSize: int, outputSize: int):
        # parameters
        self.inputSize = inputSize
        self.hiddenSize = hiddenSize
        self.outputSize = outputSize

    def create_random(self):
        # weights
        self.W1 = np.random.randn(self.inputSize, self.hiddenSize)
        self.W2 = np.random.randn(self.hiddenSize, self.outputSize)

    def create_from_parents(self, father, mother, i):
        self.W1 = np.copy(mother.W1 if i % 4 == 1 or i % 4 == 3 else father.W1)
        self.W2 = np.copy(mother.W2 if i % 4 == 1 or i % 4 == 2 else father.W2)

        for x in np.nditer(self.W1, op_flags=['readwrite']):
            x[...] += random() * 2.0 - 1.0 if random() > 0.5 else 0

        for x in np.nditer(self.W2, op_flags=['readwrite']):
            x[...] += random() * 2.0 - 1.0 if random() > 0.5 else 0

    def forward(self, X):
        # forward propagation through our network
        self.z = np.dot(X, self.W1)  # dot product of X (input) and first set of 3x2 weights
        self.z2 = self.sigmoid(self.z)  # activation function
        self.z3 = np.dot(self.z2, self.W2)  # dot product of hidden layer (z2) and second set of 3x1 weights
        o = self.sigmoid(self.z3)  # final activation function
        return o

    def sigmoid(self, s):
        # activation function
        return 1/(1+np.exp(-s))

    def sigmoidPrime(self, s):
        # derivative of sigmoid
        return s * (1 - s)

    def backward(self, X, y, o):
        # backward propgate through the network
        self.o_error = y - o  # error in output
        self.o_delta = self.o_error*self.sigmoidPrime(o)  # applying derivative of sigmoid to error

        self.z2_error = self.o_delta.dot(self.W2.T)  # z2 error: how much our hidden layer weights contributed to output error
        self.z2_delta = self.z2_error*self.sigmoidPrime(self.z2)  # applying derivative of sigmoid to z2 error

        self.W1 += X.T.dot(self.z2_delta)  # adjusting first set (input --> hidden) weights
        self.W2 += self.z2.T.dot(self.o_delta)  # adjusting second set (hidden --> output) weights

    def train(self, X, y):
        o = self.forward(X)
        self.backward(X, y, o)

#   def predict(self):
#     print "Predicted data based on trained weights: ";
#     print "Input (scaled): \n" + str(xPredicted);
#     print "Actual Output: \n" + str((self.forward(xPredicted))*3);
#     print "Rounded Output: \n" + str(round((self.forward(xPredicted))*3));

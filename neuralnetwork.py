import numpy as np
import os.path

class Neural_Network(object):
    def __init__(self, inp=2, hidden=3, out=1):
        # parameters
        self.inputSize = inp
        self.hiddenSize = hidden
        self.outputSize = out

    def randomizeWeights(self):
        # (3x2) weight matrix from input to hidden layer
        self.W1 = np.random.randn(self.inputSize, self.hiddenSize)
        # (3x1) weight matrix from hidden to output layer
        self.W2 = np.random.randn(self.hiddenSize, self.outputSize)


    def forward(self, X):
        # forward propagation through our network
        # dot product of X (input) and first set of 3x2 weights
        self.z = np.dot(X, self.W1)
        self.z2 = self.sigmoid(self.z)  # activation function
        # dot product of hidden layer (z2) and second set of 3x1 weights
        self.z3 = np.dot(self.z2, self.W2)
        o = self.sigmoid(self.z3)  # final activation function
        return o

    def sigmoid(self, s):
        # activation function
        return 1 / (1 + np.exp(-s))

    def sigmoidPrime(self, s):
        # derivative of sigmoid
        return s * (1 - s)

    def backward(self, X, y, o):
        # backward propagate through the network
        self.o_error = y - o  # error in output
        # applying derivative of sigmoid to error
        self.o_delta = self.o_error * self.sigmoidPrime(o)

        # z2 error: how much our hidden layer weights contributed to output error
        self.z2_error = self.o_delta.dot(self.W2.T)
        # applying derivative of sigmoid to z2 error
        self.z2_delta = self.z2_error * self.sigmoidPrime(self.z2)

        # adjusting first set (input --> hidden) weights
        self.W1 += X.T.dot(self.z2_delta)
        # adjusting second set (hidden --> output) weights
        self.W2 += self.z2.T.dot(self.o_delta)

    def train(self, X, y):
        o = self.forward(X)
        self.backward(X, y, o)

    def saveWeights(self, file1, file2):
        np.savetxt(file1, self.W1, fmt="%s")
        np.savetxt(file2, self.W2, fmt="%s")

    def loadWeights(self, file1, file2):
        self.W1 = np.loadtxt(file1)
        self.W2 = np.loadtxt(file2)

    def predict(self):
        print "Predicted data based on trained weights: "
        print "Input (scaled): \n" + str(xPredicted)
        print "Output: \n" + str(self.forward(xPredicted))

def dieAI(ingredients):
    nn = Neural_Network(len(ingredients), len(ingredients)*3, len(ingredients))
    if os.path.isfile(str(len(ingredients)) + "_1.txt"):
        nn.loadWeights(str(len(ingredients)) + "_1.txt", str(len(ingredients)) + "_2.txt")
    else:
        nn.randomizeWeights()

    nn.saveWeights(str(len(ingredients)) + "_1.txt", str(len(ingredients)) + "_2.txt")
    return nn.forward(ingredients)

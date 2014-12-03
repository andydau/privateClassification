# naiveBayes.py
# -------------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

# Note: this is a modified version of the code available from
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html

import util
import classificationMethod
import math

class NaiveBayesClassifier(classificationMethod.ClassificationMethod):
    """
    See the project description for the specifications of the Naive Bayes classifier.

    Note that the variable 'datum' in this code refers to a counter of features
    (not to raw data such as that produced by the loadXXX functions in samples.py).
    """
    def __init__(self, legalLabels, k=1):
        self.legalLabels = legalLabels
        self.k = k # this is the smoothing parameter, ** use it in your train method **

    def train(self, trainingData, trainingLabels):
        """
        Train Naive Bayes classifier.
        """
        # might be useful in your code later...
        # this is a list of all features in the training set.
        features = list(set([ f for datum in trainingData for f in datum.keys() ]));

        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()


    def classify(self, testData):
        """
        Classify the data based on the posterior distribution over labels.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()


    def calculateLogJointProbabilities(self, datum):
        """
        Returns the log-joint distribution over legal labels and the datum.
        Each log-probability should be stored in the log-joint counter, e.g.
        logJoint[3] = <Estimate of log( P(Label = 3, datum) )>

        To get the list of all possible features or labels, use self.features and
        self.legalLabels.
        """
        logJoint = util.Counter()

        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

        return logJoint

    def printDiagnostics(self):
        """
        This function is called after the classifier has been trained.  

        It should print helpful diagnostic information such as an analysis of the features.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

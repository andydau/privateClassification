# mira.py
# -------
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

# Mira implementation
import classificationMethod
import util

class MiraClassifier(classificationMethod.ClassificationMethod):
    """
    Mira classifier.

    Note that the variable 'datum' in this code refers to a counter of features
    (not to raw data such as that produced by the loadXXX functions in samples.py).
    """
    def __init__( self, legalLabels, max_iterations=5, C=0.001):
        self.legalLabels = legalLabels
        self.C = C
        self.max_iterations = max_iterations
        self.initializeWeightsToZero()

    def initializeWeightsToZero(self):
        "Sets the weights of each label to zero vectors"
        self.weights = {}
        for label in self.legalLabels:
            self.weights[label] = util.Counter() # this is the data-structure you should use

    def train(self, trainingData, trainingLabels):
        """
        Train the mira classifier.

        The training loop for mira passes through the training data several
        times and updates the weight vector for each label based on classification errors.
        See the project description for details.

        Use the provided self.weights[label] data structure so that
        the classify method works correctly. Also, recall that a
        datum is a counter from features to values for those features
        (and thus represents a vector a values).
        """
        "*** YOUR CODE HERE ***"
        self.features = trainingData[0].keys() # this could be useful for your code later...

        for iteration in range(self.max_iterations):
            print "Starting iteration ", iteration, "..."
            for i in range(len(trainingData)):
                "*** YOUR CODE HERE ***"
                util.raiseNotDefined()

    def classify(self, data ):
        """
        Classifies each datum as the label that most closely matches the prototype vector
        for that label.  See the project description for details.

        Recall that a datum is a util.counter...
        """
        guesses = []
        for datum in data:
            vectors = util.Counter()
            for l in self.legalLabels:
                vectors[l] = self.weights[l] * datum
            guesses.append(vectors.argMax())
        return guesses


    def printDiagnostics(self):
        """
        For each label, print the 20 features with the greatest weight for that label

        Hint: given a label, self.weights[label] is a util.Counter object, check out 
        the sortedKeys method on Counter objects.
        """
        "*** YOUR CODE HERE ***"

        util.raiseNotDefined()

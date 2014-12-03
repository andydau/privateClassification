# decisionStump.py
# -----------------------
# COSC480 AI, Colgate University

import classificationMethod
import math
import util

class DecisionStumpClassifer(classificationMethod.ClassificationMethod):
    '''
    Decision Stump classifer.

    Note that the variable 'datum' in this code refers to a counter of features
    (not to raw data such as that produced by the loadXXX functions in samples.py).
    '''

    def __init__(self, legalLabels):
        self.legalLabels = legalLabels
        self.splitFeature = None         # the feature this stump uses to classify
        self.valueToLabel = {}           # for each value of splitFeature, the class 
                                         # label that will be assigned
        "*** YOUR CODE HERE ***"
        # initialize any data structures here

    def train(self, trainingData, trainingLabels):
        '''
        Train the decision stump on training data.  Find the one
        feature with highest information gain.

        Split the training data based on this feature and calculate
        the distribution over labels within each split.  
        '''
        # might be useful in your code later...
        # this is a list of all features in the training set.
        features = list(set([ f for datum in trainingData for f in datum.keys() ]));
        "*** YOUR CODE HERE ***"


        

        # find the feature to split on and set self.splitFeature
        # split the trainingData based on the value of this feature
        # for each split, assign the plurality label
        result = util.Counter()
        gain = 0
        counter = util.Counter()
        for i in range(len(trainingData)):
            counter[trainingLabels[i]]+=1
        entropy = 0
        for key in counter.keys():
            temp = float(counter[key])/len(trainingData)
            entropy = entropy + temp*math.log(temp,2)
        entropy = entropy*(-1)
        for feature in features:
            counter = util.Counter()
            for i in range(len(trainingData)):
                counter[trainingData[i][feature]]+=1
            keyEn = 0
            for key1 in counter.keys():
                split = util.Counter()
                for i in range(len(trainingData)):
                    if trainingData[i][feature]==key1:
                        split[trainingLabels[i]]+=1
                tempEntropy = 0
                for key2 in split.keys():
                    temp = float(split[key2])/(counter[key1])
                    tempEntropy += temp*math.log(temp,2)
                tempEntropy = tempEntropy*(-1)
                keyEn += float(counter[key1])/len(trainingData)*tempEntropy
            if gain<(entropy-keyEn):
                gain = entropy-keyEn
                print gain
                self.splitFeature = feature

        counter = util.Counter()
        for i in range(len(trainingData)):
            counter[trainingData[i][self.splitFeature]]+=1
        for key in counter:
            for i in range(len(trainingData)):
                if trainingData[i][self.splitFeature]==key:
                    split[trainingLabels[i]]+=1
            self.valueToLabel[key]=split.argMax()
        # illustrative example of a decision stump hard-coded for restaurant.arff
        # this stump ignores the data and splits on price

    def classify(self, data):
        """
        Classifies each datum.

        Expects data to be a list.  Each datum in list is a feature vector (i.e., a dictionary)
        """
        guesses = []
        for datum in data:
            value = datum[self.splitFeature]
            guess = self.valueToLabel[value]
            guesses.append(guess)
        return guesses
        

    def printDiagnostics(self):
        """
        This function is called after the classifier has been trained.  

        It should print the first five levels of the decision Stump in a nicely 
        formatted way.  
        """
        print 'Decision Stump'
        print 'Classify based on feature: {0}'.format(self.splitFeature)
        for value in self.valueToLabel:
            label = self.valueToLabel[value]
            print '\tif {0}={1}, classify as {2}'.format(self.splitFeature, value, label)


"*** YOUR CODE HERE ***"
"""
You may find it helpful to create additional classes/functions
here
"""

# decisionTree.py
# -----------------------
# COSC480 AI, Colgate University

import classificationMethod
import math
import util
import numpy as np
import pdb
from numpy.random import random_sample

class DiffDecisionTreeClassifer(classificationMethod.ClassificationMethod):
    '''
    Decision tree classifer.

    Note that the variable 'datum' in this code refers to a counter of features
    (not to raw data such as that produced by the loadXXX functions in samples.py).
    '''

    def __init__(self, legalLabels, max_depth=10):  # feel free to change default max_depth
        self.legalLabels = legalLabels
        self.depth = max_depth 
        self.root = None       # training should replace this with root of decision tree!
        "*** YOUR CODE HERE ***"
        self.allLabels = []
        self.values = {}
        self.budget = 20
        self.e = float(self.budget)/(2*(self.depth+1))

    def getNoisy(self, count):
	   return count + np.random.laplace(0,float(1/self.e))

    def train(self, trainingData, trainingLabels):
        '''
        Train the decision tree on training data.
        '''
        # might be useful in your code later...
        # this is a list of all features in the training set.
        features = list(set([ f for datum in trainingData for f in datum.keys() ]));
        "*** YOUR CODE HERE ***"
        for feature in features:
            self.values[feature]=[]
            counter = util.Counter()
            for i in range(len(trainingData)):
                counter[trainingData[i][feature]]+=1
            for key in counter.keys():
                self.values[feature].append(key)
        counter = util.Counter()
        for label in trainingLabels:
            counter[label]+=1
        self.allLabels = counter.sortedKeys()
        root = self.learn(trainingData,trainingLabels,features,None,None,None,0)
        self.root = root

    def getPlularity(self,examples,exampleLabels):
        counter = util.Counter()
        if (examples==None):
            probabilities = [1/float(len(self.allLabels))]*len(self.allLabels)
            result = self.weighted_values(self.allLabels,probabilities)
            return result
        for i in range(len(examples)):
            counter[exampleLabels[i]]+=1
        for key in counter.keys():
            counter[key] = self.getNoisy(counter[key])
        result = counter.argMax()
        return result

    def weighted_values(self,values, probabilities):
        bins = np.add.accumulate(probabilities)
        bin = np.digitize([random_sample()], bins)
        return values[bin[0]]


    def sampleExp(self,examples,features,labels):
        qvalues = []
        for feature in features:
            #pdb.set_trace()
            counter = util.Counter()
            for i in range(len(examples)):
                counter[examples[i][feature]]+=1
            gini = 0
            for key1 in counter.keys():
                split = util.Counter()
                for i in range(len(examples)):
                    if examples[i][feature]==key1:
                        split[labels[i]]+=1
                tempEntropy = 0
                #print feature,split
                for key2 in split.keys():
                    temp = (float(split[key2])/(counter[key1]))
                    temp *= temp
                    tempEntropy += temp
                tempEntropy = 1 - tempEntropy
                gini += float(counter[key1])*tempEntropy
            gini = (-1)*gini/4
            #qvalue = math.exp(self.e*gini)
            qvalues.append(gini)
        minGini = min(qvalues)
        #print qvalues,minGini
        for i in range(len(qvalues)):
            qvalues[i] = qvalues[i]-minGini
            qvalues[i] = math.exp(self.e*qvalues[i])
        sumQ = sum(qvalues)
        #pdb.set_trace()
        for i in range(len(qvalues)):
            #if (sumQ!=0):
            qvalues[i] = qvalues[i]/sumQ
            #else:
                #qvalues[i] = 1/float(len(qvalues))
        return self.weighted_values(features,qvalues)

    def learn(self, examples,labels, features, parent_examples,parent_labels, parent,depth):
        count = self.getNoisy(len(examples))
        maxF = 0
        for feature in features:
            counter = util.Counter()
            for i in range(len(examples)):
                counter[examples[i][feature]]+=1
            featureCount = 0
            for key1 in counter.keys():
                featureCount += 1;
            if featureCount > maxF:
                maxF = featureCount
        labelCounter = util.Counter()
        for label in labels:
            labelCounter[label]+=1
        labelCount = len(labelCounter.sortedKeys())
        if (not examples) or (not features) or ((count/(maxF*labelCount))<(math.sqrt(2)/self.e)) or (depth>=self.depth):
            plularity = self.getPlularity(parent_examples,parent_labels)
            node = DecisionNode(parent,{},True,None,plularity,0.0)
            return node
        else:
            splitFeature = self.sampleExp(examples,features,labels)
            node = DecisionNode(parent,{},False,splitFeature,None,0)
            for value in self.values[splitFeature]:
                nextExamples = []
                nextLabels = []
                newFeatures = features[:]
                newFeatures.remove(splitFeature)
                for i in range(len(examples)):
                    if examples[i][splitFeature]==value:
                        nextExamples.append(examples[i])
                        nextLabels.append(labels[i])
                node.child[value]= self.learn(nextExamples,nextLabels,newFeatures,examples,labels,node,depth+1)
            return node


    def classify(self, data):
        """
        Classifies each datum by passing it through the decision tree.  

        Expects data to be a list.  Each datum in list is a feature vector (i.e., a dictionary)
        """
        "*** YOUR CODE HERE ***"

        guesses = []
        for datum in data:
            currentNode = self.root
            while not currentNode.leaf:
                feature = currentNode.attr
                value = datum[feature]
                #print currentNode.attr,value
                currentNode = currentNode.child[value]
            guesses.append(currentNode.label)
        return guesses


    def printDiagnostics(self):
        """
        This function is called after the classifier has been trained.  

        It should print the first five levels of the decision tree in a nicely 
        formatted way.  
        """
        "*** YOUR CODE HERE ***"
        def printhelper(node,depth):
            if depth>=5:
                return
            else:
                if node.attr!=None:
                    print "\t"*depth+"Split on "+node.attr+" gain="+str(node.gain)
                for key in node.child:
                    print "\t"*(depth+1)+"value="+str(key)+" label="+str(node.child[key].label)
                    printhelper(node.child[key],depth+1)


        current = self.root
        printhelper(current,0)

class DecisionNode:
    def __init__(self, parent, child, leaf, attr,label,gain):
        self.parent = parent
        self.child = child
        self.leaf = leaf
        self.attr = attr
        self.label = label
        self.gain = gain
                                
"*** YOUR CODE HERE ***"
"""
You may find it helpful to create additional classes/functions
such as making a DecisionNode class that represents a single 
node in the decision tree.
"""


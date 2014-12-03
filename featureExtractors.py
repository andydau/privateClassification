import featureExtractorsBasic
import porter2
import re
import samples
import util
import math

'''
-----------------------------
FEATURE EXTRACTORS FOR DIGITS
-----------------------------
'''

class DigitFeatureExtractor(featureExtractorsBasic.FeatureExtractor):
    '''
    Handles digit data.  Expects datum to be of type samples.DigitDatum
    '''
    def extractFeatures(self, datum):
        """
        Returns a set of pixel features indicating whether
        each pixel in the provided datum is white (0) or gray/black (1)
        """
        assert isinstance(datum, samples.DigitDatum), 'Expects datum to be a digit!'
        a = datum.getPixels()

        features = util.Counter()
        for x in range(datum.width):
            for y in range(datum.height):
                if datum.getPixel(x, y) > 0:
                    features[(x,y)] = 1
                else:
                    features[(x,y)] = 0
        return features

class EnhancedDigitFeatureExtractor(DigitFeatureExtractor):

    def extractFeatures(self, datum):
        """
        Your feature extraction playground.

        You should return a dictionary or a util.Counter() of features
        for this datum (datum is of type samples.Datum).
        """
        features =  DigitFeatureExtractor.extractFeatures(self, datum)
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

        "*** [END] YOUR CODE HERE ***"
        return features

'''
-----------------------------
FEATURE EXTRACTORS FOR EMAIL
-----------------------------
'''

def numCaps(s):
    '''
    Counts the number of capital letters in s.
    '''
    all_caps = 0
    for ch in s:
        if ch == ch.upper():
            all_caps += 1
    return all_caps

class EmailFeatureExtractor(featureExtractorsBasic.FeatureExtractor):
    def __init__(self):
        self.capCounts = []
        self.n = 0

    def preProcess(self, datum):
        '''
        Counts number of capitalized letters
        '''
        assert isinstance(datum, str), 'Expects datum to be a string!'
        count = numCaps(datum)
        self.capCounts.append(count)
        self.n += 1

    def finalizeFeatures(self):
        '''
        Analyzes distributions of caps and records the 25%, 50% and 75% percentiles.
        '''
        self.capCounts.sort()
        
        self.capThresholds = (self.capCounts[self.n/4], self.capCounts[self.n/2], self.capCounts[3*self.n/4])
        print 'The 25%, 50%, and 75% percentile number of capitalized letters is', self.capThresholds

    def extractFeatures(self, datum):
        '''
        Assigns a feature based on the number of capitalized letters in the email.

        All features are binary.
        '''
        assert isinstance(datum, str), 'Expects datum to be a string!'
        features = util.Counter()

        count = numCaps(datum)
        p25, p50, p75 = self.capThresholds
        if count <= p25:
            features['fewCaps'] = 1.0
        elif count <= p50:
            features['someCaps'] = 1.0
        elif count <= p75:
            features['manyCaps'] = 1.0
        else:
            features['allCaps'] = 1.0

        return features


def regexprep(text, pattern, repl):
    '''
    Finds occurrences of regular expression pattern 
    in text and replaces them with repl.  Just a 
    wrapper for re.sub but also serves as a hint that 
    this might be a useful thing to use in processing email!
    '''
    return re.sub(pattern, repl, text)


class EnhancedEmailFeatureExtractor(featureExtractorsBasic.FeatureExtractor):
    '''
    Your enhanced email extractor here.

    extractFeatures should return a dictionary or a util.Counter() of features
    for this datum (datum is of type string, representing the body of the email).


    Hint: you might find it handy to use functions regexprep and porter2.stem.
    '''

    def __init__(self):
        "*** YOUR CODE HERE ***"
        self.count = util.Counter()
        self.keys = []
        self.total = 0
        self.dataCount = 0
        self.dataWithWords = util.Counter()
        
    @staticmethod
    def processing(datum):
        datum = regexprep(datum, "<[^<>]+>","")
        datum = regexprep(datum,"(?:http)?/((([A-Za-z]{3,9}:(?:\/\/)?)(?:[\-;:&=\+\$,\w]+@)?[A-Za-z0-9\.\-]+|(?:www\.|[\-;:&=\+\$,\w]+@)[A-Za-z0-9\.\-]+)((?:\/[\+~%\/\.\w\-_]*)?\??(?:[\-\+=&;%@\.\w_]*)#?(?:[\.\!\/\\\w]*))?)/","httpaddr")
        datum = regexprep(datum,"^(((\d{1,3})(,\d{3})*)|(\d+))(.\d+)?$","number")
        datum = regexprep(datum,'(\\$)',"dollar")
        datum = regexprep(datum,'\W+\ ', '')
        datum = datum.lower()
        return datum

    def preProcess(self, datum):

        "*** YOUR CODE HERE ***"
        datum = EnhancedEmailFeatureExtractor.processing(datum)
        words = datum.strip().split()
        uniqueWords = util.Counter()
        for word in words:
            #word = porter2.stem(word)
            self.count[word]+=1
            uniqueWords[word]+=1
        for word in uniqueWords.keys():
            self.dataWithWords[word]+=1
        self.total += 1
        self.dataCount += 1

    def finalizeFeatures(self):

        "*** YOUR CODE HERE ***"
        #weightedCount = util.Counter()
        #for key in self.count.keys():
        #    temp = float(self.dataWithWords[key])/self.dataCount
        #    weightedCount[key]=self.count[key]*math.log(temp)
        sortedKeys = self.count.sortedKeys()

        #You can change the number of features here: with perceptron, 100 gives 89% accuracy, 500 gets 91.4%, 1000 gets about 94.3%
        for i in range(100):
            self.keys.append(sortedKeys[i])



        #for word in self.average.keys():
        #    average = self.count[word]/float(self.total)
        #    self.average[word]=(average/2,average,average+average/2)

    def extractFeatures(self, datum):

        "*** YOUR CODE HERE ***"
        features = util.Counter()
        wordCount = util.Counter()
        datum = EnhancedEmailFeatureExtractor.processing(datum)
        words = datum.strip().split()
        threshold = []
        for word in words:
            #word = porter2.stem(word)
            wordCount[word]+=1
        for word in self.keys:
            #for i in range(2):
                #features[str(i+1)+word]=0
            features[word]=0
        for word in wordCount.keys():
            #word = porter2.stem(word)
            if word in self.keys:
                #for i in range(3):
                    #if wordCount[word]>=self.average[word][i]:
                if features[word]==0:
                    features[word]=1
                        #features["0"+word]=0
                        #break
        return features
        


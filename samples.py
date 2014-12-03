# samples.py
# ----------
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


# Data processing, cleanup and display functions

import re
import os
import random
random.seed(1)
import os
import util
import zipfile


def loadARFFDataFile(filename, n):
    """
    Loads data in a file that meets the Weka ARFF format.
    http://www.cs.waikato.ac.nz/ml/weka/arff.html
    """
    processing_data = False
    attributes = []
    data_and_labels = []
    data = []
    labels = []
    fin = readlines(filename)
    for line in fin:
        line = line.lower()
        if line.startswith('%') or line.strip() == '':
            continue
        elif line.startswith('@attribute'):
            assert not processing_data
            matchObj = re.search(r"@attribute ([\S]+)\s+{\s*(.*\S)\s*}", line)
            if matchObj is None:
                matchObj = re.search(r"@attribute ([\S]+)\s+(real|numeric)", line)
            if matchObj is None:
                print "Can't parse this line", line
                assert matchObj is not None
            attr, legal_values = matchObj.groups()
            if legal_values == 'numeric' or legal_values == 'real':
                legal_values = 'real'
            else:
                legal_values = re.split(r'\s*,\s*', legal_values)
            attributes.append((attr, legal_values))
        elif line.startswith('@data'):
            processing_data = True
            label, legal_labels = attributes[-1]
        elif processing_data:
            values = re.split(r'\s*,\s*', line)
            assert len(values) == len(attributes), str(values) + str(attributes)
            datum = {}
            for i in range(len(attributes) - 1):
                attr = attributes[i][0]
                legal_values = attributes[i][1]
                if legal_values == 'real':
                    datum[attr] = float(values[i])
                else:
                    assert values[i] in legal_values, values[i] + str(legal_values)
                    datum[attr] = values[i]
            data_and_labels.append((datum, values[-1]))
            # data.append(datum)
            # labels.append(values[-1])
    random.shuffle(data_and_labels)
    for datum, label in data_and_labels:
        data.append(datum)
        labels.append(label)
    if len(data) < n:
        print "Truncating at %d examples (maximum)" % len(data)
    return data[:n], labels[:n]


def loadSpamData(dirname, n):
    """
    Loads the spam data.  File orders are preserved so that the ith datum corresponds
    to the ith file in the spam directory.
    """
    rawEmailTexts = []
    filenames = [name for name in os.listdir(dirname) if 'spam' in name or 'ham' in name] # remove system files
    filenames.sort(key=lambda name: int(name.split('.')[0]))  # sort them numerically
    for filename in filenames:
        if 'ham' in filename or 'spam' in filename:
            filename = os.path.join(dirname, filename)
            f = open(filename, 'r')
            text = f.read()
            f.close()
            rawEmailTexts.append(text)
            if len(rawEmailTexts) > n:
                break
    if len(rawEmailTexts) < n:
        print "Truncating at %d examples (maximum)" % len(rawEmailTexts)
    return rawEmailTexts[:n]



## Constants
DATUM_WIDTH = 0 # in pixels
DATUM_HEIGHT = 0 # in pixels

## Module Classes

class DigitDatum:
    """
    A datum is a pixel-level encoding of digits or face/non-face edge maps.

    Digits are from the MNIST dataset and face images are from the
    easy-faces and background categories of the Caltech 101 dataset.


    Each digit is 28x28 pixels, and each face/non-face image is 60x74
    pixels, each pixel can take the following values:
      0: no edge (blank)
      1: gray pixel (+) [used for digits only]
      2: edge [for face] or black pixel [for digit] (#)

    Pixel data is stored in the 2-dimensional array pixels, which
    maps to pixels on a plane according to standard euclidean axes
    with the first dimension denoting the horizontal and the second
    the vertical coordinate:

      28 # # # #      #  #
      27 # # # #      #  #
       .
       .
       .
       3 # # + #      #  #
       2 # # # #      #  #
       1 # # # #      #  #
       0 # # # #      #  #
         0 1 2 3 ... 27 28

    For example, the + in the above diagram is stored in pixels[2][3], or
    more generally pixels[column][row].

    The contents of the representation can be accessed directly
    via the getPixel and getPixels methods.
    """
    def __init__(self, data,width,height):
        """
        Create a new datum from file input (standard MNIST encoding).
        """
        DATUM_HEIGHT = height
        DATUM_WIDTH=width
        self.height = DATUM_HEIGHT
        self.width = DATUM_WIDTH
        if data == None:
            data = [[' ' for i in range(DATUM_WIDTH)] for j in range(DATUM_HEIGHT)]
        self.pixels = util.arrayInvert(convertToInteger(data))

    def getPixel(self, column, row):
        """
        Returns the value of the pixel at column, row as 0, or 1.
        """
        return self.pixels[column][row]

    def getPixels(self):
        """
        Returns all pixels as a list of lists.
        """
        return self.pixels

    def getAsciiString(self):
        """
        Renders the data item as an ascii image.
        """
        rows = []
        data = util.arrayInvert(self.pixels)
        for row in data:
            ascii = map(asciiGrayscaleConversionFunction, row)
            rows.append( "".join(ascii) )
        return "\n".join(rows)

    def __str__(self):
        return self.getAsciiString()


def loadDigitsDataFile(filename, n,width,height):
    """
    Reads n data images from a file and returns a list of DigitDatum objects.

    (Return less then n items if the end of file is encountered).
    """
    DATUM_WIDTH=width
    DATUM_HEIGHT=height
    fin = readlines(filename)
    fin.reverse()
    items = []
    for i in range(n):
        data = []
        for j in range(height):
            data.append(list(fin.pop()))
        if len(data[0]) < DATUM_WIDTH-1:
            # we encountered end of file...
            print "Truncating at %d examples (maximum)" % i
            break
        items.append(DigitDatum(data,DATUM_WIDTH,DATUM_HEIGHT))
    return items

def readlines(filename):
    "Opens a file or reads it from the zip archive data.zip"
    if (os.path.exists(filename)):
        return [l.rstrip('\n') for l in open(filename).readlines()]  
    elif os.path.exists('data.zip'):
        z = zipfile.ZipFile('data.zip')
        return z.read(filename).split('\n')
    else:
        assert False, 'Cannot find file with name {0}'.format(filename)


def loadLabelsFile(filename, n):
    """
    Reads n labels from a file and returns a list of integers.
    """
    fin = readlines(filename)
    labels = []
    for line in fin[:min(n, len(fin))]:
        if line == '':
            break
        labels.append(line.strip())
    return labels

def asciiGrayscaleConversionFunction(value):
    """
    Helper function for display purposes.
    """
    if(value == 0):
        return ' '
    elif(value == 1):
        return '+'
    elif(value == 2):
        return '#'

def IntegerConversionFunction(character):
    """
    Helper function for file reading.
    """
    if(character == ' '):
        return 0
    elif(character == '+'):
        return 1
    elif(character == '#'):
        return 2

def convertToInteger(data):
    """
    Helper function for file reading.
    """
    if type(data) != type([]):
        return IntegerConversionFunction(data)
    else:
        return map(convertToInteger, data)

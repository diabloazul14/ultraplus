#The purpose of this class is to perform any digital signal analsis presented to it.
import math
bpm = 60
noteLength = 16
sampleRate = 44100.0
timeInSecondsPerBlock = .25


def returnBPM():
    return bpm


def getNumCrossingPoints(block):
    numCrossingPoints = 0
    originalState = "Negative"
    if block[0] < 0:
        originalState = "Negative"
    else:
        originalState = "Positive"
    changed = False
    currentState = originalState
    timesChanged = 0
    for sample in block:
        if sample < 0:
            currentState = "Negative"
        else:
            currentState = "Positive"

        if currentState != originalState:
            changed = True
            originalState = currentState
            timesChanged += 1

        if timesChanged == 2:
            timesChanged = 0
            numCrossingPoints += 1
    return numCrossingPoints



def getFrequency(block):
    numCrossingPoints = getNumCrossingPoints(block)
    secondsPerMeasure = bpm / 60.0
    xNoteTimePeriod = secondsPerMeasure / float(noteLength)
    frequency = numCrossingPoints / xNoteTimePeriod
    return frequency


def breakSamplesBySamplingRate(samples, windowSize):
    return math.ceil(len(samples) / float(windowSize))

def sampleWindowSize():
    secondsPerMeasure = bpm / 60.0
    xNoteTimePeriod = secondsPerMeasure / float(noteLength)
    sample_window_size = sampleRate * xNoteTimePeriod
    return sample_window_size

def average(listPassedIn):
    theSum = sum(listPassedIn)
    length = len(listPassedIn)
    return theSum / float(length)

def readFrequencyAdjusterFile():
    guessedFrequency = []
    trueFrequency = []
    theFile = open("frequencyAdjusterList.txt", 'r')
    for line in theFile:
        tempList = line.split()
        guessedFrequency.append(float(tempList[1]))
        trueFrequency.append(float(tempList[0]))
    return guessedFrequency, trueFrequency


def difference(pointOne, pointTwo):
    return abs(pointOne - pointTwo)


def frequencyAdjuster(frequency):
    if frequency < 27 or frequency > 5000:
        return 0.0
    else:
        guessedFrequency, trueFrequency = readFrequencyAdjusterFile()
        #Scan guessedFrequency list for nearest match
        currentdifference = 10000.0
        closestFrequency = 0.0
        for item in guessedFrequency:
            if difference(item, frequency) < currentdifference:
                currentdifference = difference(item, frequency)
                closestFrequency = item

        #return trueFrequency that maps to guessed frequency
        i = len(guessedFrequency) - 1
        for item in reversed(guessedFrequency):
            if item == closestFrequency:
                break
            i -= 1
        return trueFrequency[i]


def findNoteDurationInUnits(adjusted):
    durations = []
    frequencies = []
    k = 1
    for i in range(len(adjusted) - 1):
        if adjusted[i] == adjusted[i + 1]:
            k += 1
        else:
            durations.append(k)
            frequencies.append(adjusted[i])
            k = 1
        if i == len(adjusted) - 2:
            durations.append(k)
            frequencies.append(adjusted[i])
    return durations, frequencies

def convertDurationUnitsToSeconds(durations):
    timeInSeconds = []
    for element in durations:
        timeInSeconds.append(element * timeInSecondsPerBlock)
    return timeInSeconds


def convertFromFrequencyToMidiNoteNumber(frequencies):
    convertedFrequencies = []
    midiNoteList = generateMidiNoteList()
    #find closest match and append index of closest match to convertedFrequencies
    for frequency in frequencies:
        convertedFrequencies.append(findClosestMatch(frequency))
    return convertedFrequencies
    

def generateMidiNoteList():
    midiNoteList = []
    semitoneRatio = 2 ** (1.0/12.0)
    c5 = 220.0 * (semitoneRatio ** 3)
    c0 = c5 * .5 ** 5
    for i in range(128):
        midiNoteList.append(c0 * semitoneRatio ** i)
    return midiNoteList

def findClosestMatch(frequency):
    oldDifference = 10000
    listOfMidiNotes = generateMidiNoteList()
    for note in listOfMidiNotes:
        newDifference = difference(note, frequency)
        if newDifference < oldDifference:
            oldDifference = newDifference
    i = 0
    for note in listOfMidiNotes:
        if oldDifference == difference(note, frequency):
            return i
        i += 1

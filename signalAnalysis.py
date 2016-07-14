#The purpose of this class is to perform any digital signal analsis presented to it.
import math
bpm = 100
noteLength = 8
sampleRate = 44100.0


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

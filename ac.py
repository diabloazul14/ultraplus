#The purpose of this is to run the entire process
import wav
#import midi
import signalAnalysis as sa
import sys
import wave
#import numpy as np
import os
import math

MIN_SAMPLES = 0
GOOD_ENOUGH_CORRELATION = .9
def autocorrelation(buf):
    SIZE = len(buf)
    MAX_SAMPLES = int(math.floor(SIZE/2.0))
    best_offset = -1
    best_correlation = 0
    rms = 0
    foundGoodCorrelation = False
    correlations = [0] * MAX_SAMPLES

    for i in range(SIZE):
        val = buf[i]
        rms += val * val

    rms = math.sqrt(rms / float(SIZE))
    if rms < .01:
        return -1
    
    lastCorrelation = 1
    offset = MIN_SAMPLES
    while (offset < MAX_SAMPLES):
        correlation = 0
        for i in range(MAX_SAMPLES):
            correlation += math.fabs(buf[i] - buf[i + offset])

        correlation = 1 - (correlation / float(MAX_SAMPLES))
        correlations[offset] = correlation
        if ((correlation > GOOD_ENOUGH_CORRELATION) and (correlation > lastCorrelation)):
            foundGoodCorrelation = True
            if (correlation > best_correlation):
                best_correlation = correlation
                best_offset = offset

        elif (foundGoodCorrelation):
            shift = (correlations[best_offset + 1] - correlations[best_offset - 1]) / float(correlations[best_offset])
            return 44100 / float(best_offset + (8 * shift))
        lastCorrelation = correlation
        offset += 1
    if (best_correlation > .01):
        return 44100 / float(best_offset)
    return -1


#Wav file data grabbing
wavFile = wave.open(str(sys.argv[1]), 'rb')
rawsamples = wavFile.readframes(wavFile.getnframes())
hexsamples = []

i = 0
while i < len(rawsamples):
	newsample = rawsamples[i] + rawsamples[i + 1]
	hexsamples.append(newsample.encode('hex'))
	i += 2

presamples = []
for sample in hexsamples:
	presamples.append(wav.littleEndianStringToInteger(sample))

samples = []
if wavFile.getnchannels() == 1:
	samples = presamples
if wavFile.getnchannels() == 2:
	i = 0
	lenPreSamples = len(presamples)
	while i < lenPreSamples:
		samples.append(presamples[i])
		i += 2

#shift the samples into the right range
i = 0
shiftValue = -32767
for sample in samples:
	samples[i] = sample + shiftValue
	i += 1

#Shift to -1 to 1 range
i = 0
for sample in samples:
    samples[i] = sample / 32767.0
    i += 1

regionLength = int(44100 / 4.0) #half second intervals

#Zero padding
numberOfRegions = int(math.ceil(len(samples) / regionLength))
differenceInLenOfSamplesAndLenOfRegion = int((numberOfRegions * regionLength) - len(samples))
for diff in range(differenceInLenOfSamplesAndLenOfRegion):
    samples.append(0)

#Perform autocorrelation on segments
beginning = 0
end = regionLength
frequencies = []
for region in range(numberOfRegions):
    frequencies.append(autocorrelation(samples[beginning:end]))
    beginning += regionLength
    end += regionLength

#Map found frequencies to nearest midi note
midiNoteNumbers = [] 
for frequency in frequencies:
    midiNoteNumbers.append(sa.findClosestMatch(frequency))

#Add duplicates and create duration list
durationList, midiNoteNumbers = sa.addConsecutiveNotesAndGenerateDurationList(midiNoteNumbers)

#Create the midi file
from midiutil.MidiFile import MIDIFile
MyMIDI = MIDIFile(1)
track = 0
time = 0
MyMIDI.addTrackName(track, time, "Sample Track")
MyMIDI.addTempo(track, time, 120)
track = 0
channel = 0
pitch = 60
time = 0
duration = 0

for i in range(len(midiNoteNumbers)):
	track = 0
	channel = 0
	pitch = midiNoteNumbers[i]
	time += durationList[i]
	duration = durationList[i]
	volume = 100
	MyMIDI.addNote(track, channel, pitch, time, duration, volume)

binfile = open("output.mid", 'wb')
MyMIDI.writeFile(binfile)
binfile.close()

#Create the PDF and Display
os.system("mscore output.mid -o output.pdf")
os.system("evince output.pdf")
#The purpose of this is to run the entire process
import wav
import midi
import signalAnalysis as sa
import sys
import wave
import numpy as np
import os

#Wav file data grabbing
# wavFile = wav.wav(str(sys.argv[1]))
# samples = wavFile.parseSamples()
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
		samples.append(wav.average(presamples[i], presamples[i + 1]))
		i += 2

#shift the samples into the right range
i = 0
shiftValue = -32767
for sample in samples:
	samples[i] = sample + shiftValue
	# print(samples[i])
	i += 1

#Analyze the Samples frequencies

samplesPerWindow = sa.sampleWindowSize()
segments = sa.breakSamplesBySamplingRate(samples, samplesPerWindow)

beginning = 0
end = int(samplesPerWindow)
dominantFrequencies = []
for block in range(int(segments) - 1):
	dominantFrequencies.append(sa.getFrequency(samples[beginning:end]))
	beginning += int(samplesPerWindow)
	end += int(samplesPerWindow)

adjusted = []
for frequency in dominantFrequencies:
	adjusted.append(sa.frequencyAdjuster(frequency + 5))
# print("adjusted")
# print(adjusted)

#theAverage = sa.average(dominantFrequencies)
#print(theAverage + 5)
#print(sa.frequencyAdjuster(theAverage + 5))


#Analyze the Samples Length
durations, frequencies = sa.findNoteDurationInUnits(adjusted)
# print("durations")
# print(durations)
# print("frequencies")
# print(frequencies)

durationInSeconds = sa.convertDurationUnitsToSeconds(durations)
# print("durationInSeconds")
# print(durationInSeconds)

midiNoteNumbers = sa.convertFromFrequencyToMidiNoteNumber(frequencies)
# print("midiNoteNumbers")
# print(midiNoteNumbers)

durationInSeconds, midiNoteNumbers = sa.removeTooHighAndTooLowMidiNotes(durationInSeconds, midiNoteNumbers)
# print(durationInSeconds)
# print(midiNoteNumbers)
# print("----------------------------------------------------------------")
durationInSeconds, midiNoteNumbers = sa.removeNoise(durationInSeconds, midiNoteNumbers)
# print(durationInSeconds)
# print(midiNoteNumbers)
# print("----------------------------------------------------------------")
durationInSeconds, midiNoteNumbers = sa.addConsecutiveNotes(durationInSeconds, midiNoteNumbers)
# print(durationInSeconds)
# print(midiNoteNumbers)
# print("----------------------------------------------------------------")


#Convert the samples into midi file
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
	time += durationInSeconds[i]
	duration = durationInSeconds[i]
	volume = 100
	MyMIDI.addNote(track, channel, pitch, time, duration, volume)

binfile = open("output.mid", 'wb')
MyMIDI.writeFile(binfile)
binfile.close()


# #Convert the midi file to a pdf file
os.system("mscore output.mid -o output.pdf")
os.system("evince output.pdf")

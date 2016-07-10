#The purpose of this is to run the entire process, no processing should occur within this file.
import wav
import midi
import signalAnalysis as sa
import sys
import wave
import numpy as np

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

crossingPoints = 0
for sample in samples:
	if sample < 30:
		crossingPoints += 1
print("crossingPoints: " + str(crossingPoints))

#Analyze the Samples
#analyzer = sa.signalAnalysis(samples)
samples = wav.zeroPadSamples(samples)
frequencies = np.fft.fft(samples)
for frequency in frequencies:
	print(frequencies)

#Convert the samples into midi file

#Convert the midi file to a pdf file

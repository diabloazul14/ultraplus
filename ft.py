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

#analyze the samples
from scipy.fftpack import fft
fftList = fft(samples)

#print(fftList)
temp = [""] * len(fftList)

for i in range(len(fftList)):
	temp[i] = str(fftList[i])

print(temp)
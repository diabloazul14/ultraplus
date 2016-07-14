import sys
import math
import cmath #for complex number calculations
from numpy import linalg as LA
import matplotlib.pyplot as plt
from scipy import fftpack as ft_pack

noteFrequencyMap = {'A0' : 27.5, 'A#0' : 29.1352, 'B0' : 30.8677, 'C1' : 32.7032, 'C#1' : 34.6478, 'D1' : 36.7081, 'D#1' : 38.8909, 'E1' : 41.2034, 'F1' : 43.6535, 'F#1' : 46.2493, 'G1' : 48.9994, 'G#1' : 51.9131, 'A1' : 55, 'A1#' : 58.2705, 'B1' : 61.7354, 'C2' : 65.4064, 'C#2' : 69.2957, 'D2' : 73.4162, 'D#2' : 77.7817, 'E2' : 82.4069, 'F2' : 87.3071, 'F#2' : 92.4986, 'G2' : 97.9989, 'G#2' : 103.826, 'A2' : 110.0, 'A#2' : 116.541, 'B2' : 123.471, 'C3' : 130.813, 'C#3' : 138.591, 'D3' : 146.832, 'D#3' : 155.563, 'E3' : 164.814, 'F3' : 174.614, 'F#3' : 184.997, 'G3' : 195.998, 'G#3' : 207.652, 'A3' : 220.0, 'A#3' : 233.082, 'B3' : 246.942, 'C4' : 261.626, 'C#4' : 277.183, 'D4' : 293.665, 'D#4' : 311.127, 'E4' : 329.628, 'F4' : 349.228, 'F#4' : 369.994, 'G4' : 391.995, 'G#4' : 415.305, 'A4' : 440.0, 'A#4' : 466.164, 'B4' : 493.883, 'C5' : 523.251, 'C#5' : 554.365, 'D5' : 587.330, 'D#5' : 662.254, 'E5' : 659.255, 'F5' : 698.456, 'F#5' : 739.989, 'G5' : 783.991, 'G#5' : 830.609, 'A5' : 880.0, 'A#5' : 932.328, 'B5' : 987.767, 'C6' : 1046.50, 'C#6' : 1108.73, 'D6' : 1174.66, 'D#6' : 1244.51, 'E6' : 1318.51, 'F6' : 1396.91, 'F#6' : 1479.98, 'G6' : 1567.98, 'G#6' : 1661.22, 'A6' : 1760.0, 'A#6' : 1864.66, 'B6' : 1975.53, 'C7' : 2093.0, 'C#7' : 2217.46, 'D7' : 2349.32, 'D#7' : 2489.02, 'E7' : 2637.02, 'F7' : 2793.83, 'F#7' : 2959.96, 'G7' : 3135.96, 'G#7' : 3322.44, 'A7' : 3520.0, 'A#7' : 3729.31, 'B7' : 3951.07, 'C8' : 4186.01}
wavFile = open(str(sys.argv[1]), "rb")
##################################################################
#Convert little endian hex string to integer
def littleEndianStringToInteger(littleEndianHexString):
	bigEndianHexString = "0x"
	lengthOfLittleEndianHexString = len(littleEndianHexString)
	i = 0
	while i < lengthOfLittleEndianHexString:
		bigEndianHexString += littleEndianHexString[i + 2]
		bigEndianHexString += littleEndianHexString[i + 3]
		bigEndianHexString += littleEndianHexString[i + 0]
		bigEndianHexString += littleEndianHexString[i + 1]
		i += 4
	i = len(bigEndianHexString)
	while True:
		if bigEndianHexString[i - 1] == "0" and bigEndianHexString[i - 2] == "0":
			bigEndianHexString = bigEndianHexString[:-2]
			i = len(bigEndianHexString)
		else:
			break
	if bigEndianHexString == "0x":
		bigEndianHexString += "00"
	return int(bigEndianHexString, 0)

##################################################################
#find the average of two numbers
def average(leftChannel, rightChannel):
	total = leftChannel + rightChannel
	return float(total) / 2.0
##################################################################
# discrete fourier transform algorithm
def dft(samples):
	N = len(samples)
	out = [0.0] * N
	i = 0
	k = 0
	twopi = 2 * math.acos(-1.0)
	while (k < N):
		out[i] = 0.0
		out[i + 1] = 0.0
		n = 0
		while n < N:
			out[i] += samples[n] * math.cos(k * n * twopi / N)
			out[i + 1] -= samples[n] * math.sin(k * n * twopi / N)
			n += 1
		out[i] /= N
		out[i + 1] /= N
		i = i + 2
		k = k + 1
	return out

##################################################################
#https://jeremykun.com/2012/07/18/the-fast-fourier-transform/
def omega(p, q):
	return cmath.exp((2.0 * cmath.pi * 1j * q) / p)
##################################################################
#https://jeremykun.com/2012/07/18/the-fast-fourier-transform/
def fft(signal):
	n = len(signal)
	if n == 1:
		return signal
	else:
		Feven = fft([signal[i] for i in xrange(0, n, 2)])
		Fodd = fft([signal[i] for i in xrange(1, n, 2)])
		combined = [0] * n
		for m in xrange(n / 2):
			combined[m] = Feven[m] + omega(n, -m) * Fodd[m]
			combined[m + n/2] = Feven[m] - omega(n, -m) * Fodd[m]
		return combined

##################################################################
def sampleWindowSize(bpm, noteLength):
	sampleRate = 44100
	secondsPerMeasure = bpm / 60.0
	xNoteTimePeriod = secondsPerMeasure / float(noteLength)
	sample_window_size = sampleRate * xNoteTimePeriod
	return sample_window_size

##################################################################
def findLargestSample(sampleList):
	largest = 0
	for sample in sampleList:
		if sample >= largest:
			largest = sample
	return largest


##################################################################
#parse wav file format
# parse chunk id: riff tag
byte = wavFile.read(4)
if byte != "RIFF":
	quit()
# else:
# 	print("Chunk ID: " + byte)

# parse chunk size: I don't know what to do with this chunk
byte = wavFile.read(4)
encodedByte = byte.encode('hex')
intEncodedByte = littleEndianStringToInteger(encodedByte)
# print("Chunk Size: " + str(intEncodedByte))

# parse Wav id: It had better say wave
byte = wavFile.read(4)
if byte != "WAVE":
	quit()
# else:
# 	print("Wav ID: " + byte)

##################################################################
# parse format chunk
# parse format chunk id: "fmt "
byte = wavFile.read(4)
if byte != "fmt ":
	quit()
# else:
# 	print("Format Chunk ID: " + byte)

# parse format chunk size: 
byte = wavFile.read(4)
encodedByte = byte.encode('hex')
intEncodedByte = littleEndianStringToInteger(encodedByte)
if intEncodedByte != 16 and intEncodedByte != 18 and intEncodedByte != 40:
	quit()
# else:
# 	print("Format Chunk Size: " + str(intEncodedByte) + " bits")

#add a conversion for ieee to pcm data somewhere in the code
#parse format tag : PCM vs IEEE
formatTag = ""
byte = wavFile.read(2)
encodedByte = byte.encode('hex')
if encodedByte == "0100":
	formatTag = "PCM"
elif encodedByte == "0300":
	formatTag = "IEEE Float"
else:
	print("Sorry, wav must be eithier in PCM or IEEE float format")
	quit()
# print("Format Tag: " + formatTag)

#parse format number of interleaved channels
numChannels = 0
byte = wavFile.read(2)
encodedByte = byte.encode('hex')
intEncodedByte = littleEndianStringToInteger(encodedByte)
numChannels = intEncodedByte
if numChannels != 1 and numChannels != 2:
	print("Can only process mono or stereo sound")
	quit()
# print("interleaved channels: " + str(numChannels))

# parse numper of samples per seconds
samplingRate = 0
byte = wavFile.read(4)
encodedByte = byte.encode('hex')
intEncodedByte = littleEndianStringToInteger(encodedByte)
if intEncodedByte != 44100:
	print("The samplingRate should be 44100 samples/sec")
	quit()
else:
	samplingRate = intEncodedByte
# print("samplingRate: " + str(samplingRate))

# # parse number of average bytes per second or data rate
# #figure out how to convert little endian hex string to integer
# numBytesPerSecond = 0
# byte = wavFile.read(4)
# encodedByte = byte.encode('hex')
# intEncodedByte = littleEndianStringToInteger(encodedByte)
# print("numBytesPerSecond: " + str(intEncodedByte))

# # parse format data block size
# dataBlockSize = 0
# byte = wavFile.read(2)
# encodedByte = byte.encode('hex')
# intEncodedByte = littleEndianStringToInteger(encodedByte)
# dataBlockSize = intEncodedByte
# print("Format data block size: " + str(dataBlockSize))

# # parse format bits per sample
# bitsPerSample = 0
# byte = wavFile.read(2)
# encodedByte = byte.encode('hex')
# intEncodedByte = littleEndianStringToInteger(encodedByte)
# bitsPerSample = intEncodedByte
# print("Format bits per sample: " + str(bitsPerSample))

# # parse size of the extension or cbSize: 0 or 22
# cbSize = 0
# byte = wavFile.read(2)
# encodedByte = byte.encode('hex')
# intEncodedByte = littleEndianStringToInteger(encodedByte)
# cbSize = intEncodedByte
# print("cbsize: " + str(cbSize))

# #parse number of valid bits
# validBitsPerSample = 0
# byte = wavFile.read(2)
# encodedByte = byte.encode('hex')
# intEncodedByte = littleEndianStringToInteger(encodedByte)
# validBitsPerSample = intEncodedByte
# print("validBitsPerSample: " + str(validBitsPerSample))

# #parse speaker position mask
# channelMask = 0
# byte = wavFile.read(4)
# encodedByte = byte.encode('hex')
# intEncodedByte = littleEndianStringToInteger(encodedByte)
# channelMask = intEncodedByte
# print("channelMask: " + str(channelMask))

# #parse the GUID and data format code
# subFormat = ""
# byte = wavFile.read(16)
# encodedByte = byte.encode('hex')

#Don't remove below line for some reason.
byte = wavFile.read(8) #I don't know what these 8 bytes are, as they don't conform to the spec.




#######################################################################################
# parse the actual samples now PCM currently only, not IEEE floating point
samples = []
if numChannels == 1:
	# print("Mono Processing beginning")
	# convert each sample of x bytes into an integer and append to samples list
	if formatTag == "IEEE Float":
		# print("--IEEE Float Sample Collecting")
		# Add step to convert IEEE floating numbers to PCM range for further processing.
		byte = wavFile.read(4)
		if byte == "data":
			dataSize = 0
			byte = wavFile.read(4)
			encodedByte = byte.encode('hex')
			intEncodedByte = littleEndianStringToInteger(encodedByte)
			dataSize = intEncodedByte
			byte = wavFile.read(2)
			while byte != "":				
				encodedByte = byte.encode('hex')
				intEncodedByte = littleEndianStringToInteger(encodedByte)
				# add conversion step here
				samples.append(intEncodedByte)
				byte = wavFile.read(2)

	else:
		# print("--PCM sample collection")
		byte = wavFile.read(4)
		if byte == "data":
			dataSize = 0
			byte = wavFile.read(4)
			encodedByte = byte.encode('hex')
			intEncodedByte = littleEndianStringToInteger(encodedByte)
			dataSize = intEncodedByte
			byte = wavFile.read(2)
			while byte != "":
				encodedByte = byte.encode('hex')
				intEncodedByte = littleEndianStringToInteger(encodedByte)
				samples.append(intEncodedByte)
				byte = wavFile.read(2)
		
else:
	# print("Stereo Processing beginning")
	# convert each left sample into an integer
	# convert each right sample into an integer
	# average the left and the right sample
	# append the average to the samples list
	if formatTag == "IEEE Float":
		# print("--IEEE Float Sample Collecting")
		# Add step to convert IEEE floating numbers to PCM range for further processing.
		byte = wavFile.read(4)
		if byte == "data":
			dataSize = 0
			byte = wavFile.read(4)
			encodedByte = byte.encode('hex')
			intEncodedByte = littleEndianStringToInteger(encodedByte)
			dataSize = intEncodedByte
			byte = wavFile.read(2)
			while byte != "":
				encodedByte = byte.encode('hex')
				leftChannel = littleEndianStringToInteger(encodedByte)
				byte = wavFile.read(2)
				encodedByte = byte.encode('hex')
				rightChannel = littleEndianStringToInteger(encodedByte)				
				theAverage = average(leftChannel, rightChannel)
				#Convert the average here and append it to samples
				byte = wavFile.read(2)

	else:
		# print("--PCM sample collection")
		byte = wavFile.read(4)
		if byte == "data":
			dataSize = 0
			byte = wavFile.read(4)
			encodedByte = byte.encode('hex')
			intEncodedByte = littleEndianStringToInteger(encodedByte)
			dataSize = intEncodedByte
			byte = wavFile.read(2)
			ifStatementHit = False
			while byte != "":
				if byte == "da":
					wavFile.read(2)
					ifStatementHit = True
				else:
					if ifStatementHit == True:
						byte = wavFile.read(2)
						ifStatementHit = False
					encodedByte = byte.encode('hex')
					leftChannel = littleEndianStringToInteger(encodedByte)
					byte = wavFile.read(2)
					encodedByte = byte.encode('hex')
					rightChannel = littleEndianStringToInteger(encodedByte)
					samples.append(int(average(leftChannel, rightChannel)))
					byte = wavFile.read(2)
######################################################################
# Test samples are good.
len_samples = len(samples)

crossingPoint = 0
for sample in samples:
	print(sample)
	if sample < 0:
		crossingPoint += 1
print("crossingPoint: " + str(crossingPoint))

#make sure number of samples is power of 2 for fast fourier transform by zero padding
powerOfTwo = []
powersOfTwoFile = open("powerOfTwo.txt", "r")
for line in powersOfTwoFile:
	powerOfTwo.append(int(line))

powersOfTwoFile.close()


index = 0
while (len_samples >= powerOfTwo[index]):
	index += 1

len_of_zeros_to_pad_with = powerOfTwo[index] - len_samples
for i in range(len_of_zeros_to_pad_with):
	samples.append(0)

# len_samples = len(samples)
# print(str(len_samples))
# for sample in samples:
# 	print(sample)


######################################################################
# find the frequencies from the samples using fft, or another frequency analysis algorithm

minimum = -65535.0
maximum = 65535.0
scaled = []
for sample in samples:
	if sample == 0:
		scaled.append(0)
	elif sample < 0:
		scaled.append(sample / minimum)
	else:
		scaled.append(sample / maximum)


transformed = []
transformed = fft(scaled)
norm = []
for sample in transformed:
	norm.append(LA.norm(sample))


finalSamples = []
len_of_half_the_norms = len(norm) / 2
i = 0
while i <= len_of_half_the_norms:
	finalSamples.append(norm[i])
	i += 1

# logFinalSample = []
# for sample in finalSamples:
# 	logFinalSample.append(math.log(sample))

# iftSamples = ft_pack.ifft(logFinalSample)

#########################################################33
#Now that the fft is complete, start onset detection and note frequency detection
sample_window_size = sampleWindowSize(100, 8)

numberOfSegmentsToAnalyze = math.ceil(len(finalSamples) / float(sample_window_size))
onsetDetected = False
beginning = 0
end = int(sample_window_size)
dominantFrequencies = []
for block in range(int(numberOfSegmentsToAnalyze)):
	# print(len(finalSamples[beginning:end]))
	if block == numberOfSegmentsToAnalyze - 1:
		end = int(len(finalSamples) - 1)
		#dominantFrequencies.append(findLargestSample(finalSamples[beginning:end]))
		dominantFrequencies.append(sum(finalSamples[beginning:end])/float(len(finalSamples[beginning:end])))
	else:
		#dominantFrequencies.append(findLargestSample(finalSamples[beginning:end]))
		dominantFrequencies.append(sum(finalSamples[beginning:end])/float(len(finalSamples[beginning:end])))
	beginning += int(sample_window_size)
	end += int(sample_window_size)

# print(dominantFrequencies)



# for normalized in finalSamples:
	# print(normalized)


# plt.plot(finalSamples)
# plt.show()
#The purpose of this class is deal with wav files and the parsing of wavfiles. Besides wav file processing, no pitch detection or spectral analysis should occur here.
# class wav():
# 	def __init__(self, nameOfWavFile):
# 		self.nameOfWavFile = nameOfWavFile
# 		self.samples = []
# 		self.pcmOrIeee = ""	

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

def average(leftChannel, rightChannel):
	total = leftChannel + rightChannel
	return total / 2.0



	def parseSamples(self):
		wavFile = open(self.nameOfWavFile, "rb")
		#read past the header to the first data block
		byte = wavFile.read(4)
		while byte != "data":
			byte = wavFile.read(4)
		byte = wavFile.read(4)
		#parse data in every datablock into self.samples without reading data blocks
		byteL = wavFile.read(2)
		byteR = wavFile.read(2)
		while byteL != "" and byteR != "":
			if byteL == "da" and byteR == "ta":
				byte = wavFile.read(4) #Reads past data chunk size
			else:
				encodedByteL = byteL.encode('hex')
				encodedByteR = byteR.encode('hex')
				intEncodedByteL = self.littleEndianStringToInteger(encodedByteL)
				intEncodedByteR = self.littleEndianStringToInteger(encodedByteR)
				self.samples.append(self.average(intEncodedByteL, intEncodedByteR))
			byteL = wavFile.read(2)
			byteR = wavFile.read(2)
		wavFile.close()
		#self.zeroPadSamples()
		return self.samples

	def zeroPadSamples(self):
		lenOfSamples = len(self.samples)
		i = 1
		powerOfTwoGreaterThanLenOfSamples = 0
		while powerOfTwoGreaterThanLenOfSamples <= lenOfSamples:
			powerOfTwoGreaterThanLenOfSamples = 2 ** i
			i += 1
		diffInLenOfSamples = powerOfTwoGreaterThanLenOfSamples - lenOfSamples
		for diff in range(diffInLenOfSamples):
			self.samples.append(0)

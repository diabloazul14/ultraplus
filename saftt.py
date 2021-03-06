import math
def computeMagnitudes(fftList):
	magnitudes = []
	for element in fftList:
		magnitudes.append(calcMagnitude(element))
	return magnitudes

def calcMagnitude(element):
	a = element.real
	b = element.imag
	return math.sqrt((a ** 2) + (b ** 2))

def maxFrequency(block):
	theMax = 0
	maxHeight = 4500
	minHeight = 25
	index = 0
	i = 0
	for element in block:
		if element > theMax and element < maxHeight and element > minHeight:
			theMax = element
			index = i
			print("Triggered")
		i += 1

	return theMax, index

def returnSecondLargestFrequency(block, maxFrequency):
	theSecondMax = 0
	maxHeight = 4500
	minHeight = 25
	index = 0
	i = 0
	for element in block:
		if element > theSecondMax and element < maxFrequency and element < maxHeight and element > minHeight:
			theSecondMax = element
			index = i
			print("Triggered")
		i += 1
	return theSecondMax, index
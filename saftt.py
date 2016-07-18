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
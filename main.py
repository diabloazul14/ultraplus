#The purpose of this is to run the entire process, no processing should occur within this file.
import wav
import midi
import signalAnalysis as sa
import sys

#Wav file data grabbing
wavFile = wav.wav(str(sys.argv[1]))
samples = wavFile.parseSamples()

#Analyze the Samples
#analyzer = sa.signalAnalysis(dataBlocks)

#Convert the samples into midi file

#Convert the midi file to a pdf file
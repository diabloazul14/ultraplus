import numpy as N
import wave

class SoundFile:
   def  __init__(self, signal, fileName):
       self.file = wave.open(fileName, 'wb')
       self.signal = signal
       self.sr = 44100

   def write(self):
       self.file.setparams((1, 2, self.sr, 44100*4, 'NONE', 'noncompressed'))
       self.file.writeframes(self.signal)
       self.file.close()

# let's prepare signal
k = 900
while k < 5000:
    k += 1
    duration = 1 # seconds
    samplerate = 44100 # Hz
    samples = duration*samplerate
    frequency = k # Hz
    period = samplerate / float(frequency) # in sample points
    omega = N.pi * 2 / period
    xaxis = N.arange(int(period),dtype = N.float) * omega
    ydata = 16384 * N.sin(xaxis)
    signal = N.resize(ydata, (samples,))
    ssignal = ''
    for i in range(len(signal)):
           ssignal += wave.struct.pack('h',signal[i]) # transform to binary
    fileName = str(frequency) + ".wav"
    f = SoundFile(ssignal, fileName)
    f.write()
    print(str(k))

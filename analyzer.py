import os
i = 1
while i < 10:
    print(i)
    fileName = "sineWaveGenerator/" + str(i) + ".wav"
    os.system("python main.py " + fileName + " > " + str(i) + ".txt")
    i += 1
    

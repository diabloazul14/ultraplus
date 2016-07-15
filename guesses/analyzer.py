import os
i = 1
while i < 10:
    print(i)
    fileName = "/home/matthew/School/ultraplus/sineWaveGenerator/" + str(i) + ".wav"
    os.system("python /home/matthew/School/ultraplus/main.py " + fileName + " > " + str(i) + ".txt")
    i += 1
    

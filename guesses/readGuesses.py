guesses = []
i = 1
while i < 5000:
    fileName = str(i) + ".txt"
    theFile = open(fileName, 'r')
    for line in theFile:
        guesses.append(line)
    theFile.close()
    print(str(i))
    i += 1
fileName = "allGuesses.txt"
theFile = open(fileName, 'w')
for guess in guesses:
    theFile.write(guess)
theFile.close()

theFile = open("allGuesses.txt", 'r')
guesses = []
for line in theFile:
    guesses.append(float(line))
theFile.close()

theFile = open("adjustments.txt", 'w')
i = 1
for guess in guesses:
    theFile.write(str(guess - i))
    theFile.write("\n")
    i += 1
theFile.close()


import os
import re

script_dir = os.path.dirname(__file__)

inputDirectory = os.path.join(script_dir, '../Inputs/INPUTS-Original')
outputDirectory = os.path.join(script_dir, '../Inputs/INPUTS-Trimmed')

# Iterate over the files from the inputDirectory

for file in os.scandir(inputDirectory):
    if file.is_file():
        print(file.name)

        # First, find the following sequence:
        regex = '^.*,0.0,0.0,0,1,0,0.0,0.0$'

        filename = inputDirectory + '/' + file.name

        with open(filename,"r") as fileInput: 

            listLines = fileInput.readlines()

            i = 0
            for item in listLines:
                if re.search(regex,item):
                    break
                i = i + 1

            listIndex = i

        # Second, erase everything above the sequence

        filename = outputDirectory + '/' + file.name.split()[0] + ".txt"

        with open(filename,"w") as fileOutput:

            fileOutput.write("".join(listLines[listIndex:]))


        # Third, we set the correct seconds

        with open(filename,'r') as fileCorrectionInput:

            listLines = fileCorrectionInput.readlines()

            tokens = listLines[0].split(',')
            seconds = round(float(tokens[0]),2)

            for i in range(len(listLines)):
                tokens = listLines[i].split(',')
                correction = str(round(float(tokens[0]) - seconds,2))
                tokens = tokens[1:]
                for token in tokens:
                    correction = correction + "," + token
                listLines[i] = correction

        # Fourth, we implement the corrections

        with open(filename,'w') as fileCorrectionOutput:
            fileCorrectionOutput.write("".join(listLines))
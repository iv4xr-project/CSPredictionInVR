import os
import re

script_dir = os.path.dirname(__file__)

adjustedDirectory = os.path.join(script_dir, '../Inputs/INPUTS-Adjusted')
completeDirectory = os.path.join(script_dir, '../Inputs/INPUTS-Complete')
csvDirectory = os.path.join(script_dir, '../CSV_Data/INPUTS/INPUTS-TRAD')

# Iterate over the files from the adjustedDirectory

# Here we ensure that all input files have easily identifiable integer seconds (0.0, 1.0, 5.0, 500.0, etc)
"""
print("-------------MAKING INPUTS COMPLETE-------------")

for file in os.scandir(adjustedDirectory):
    if file.is_file():
        print(file.name)

        filename = adjustedDirectory + '/' + file.name

        with open(filename,"r") as fileAdjusted: 

            listLines = []

            lines = fileAdjusted.readlines()
        
            counter = -1

            listLines.append("ElapsedSeconds,LJ_X,LJ_Y,RT,A,B,RJ_X,RJ_Y\n")

            foundHalf = False
            for line in lines:
                tokens = line.split(',')
                second = float(tokens[0])
                addHash = False

                if second.is_integer():
                    if int(second) == counter + 1:
                        listLines.append(line)
                        counter += 1
                        addHash = False
                        foundHalf = False
                    else:
                        addHash = True
   
                elif round(second % 1,2) == 0.01 and counter < int(second):
                    second = float(int(second))
                    if int(second) == counter + 1:
                        correction = str(second)
                        for token in tokens[1:]:
                            correction += ',' + token
                        listLines.append(correction)
                        counter += 1
                        addHash = False
                        foundHalf = False
                    else:
                        addHash = True

                #elif round(second % 1,2) <= 0.53 and round(second % 1,2) >= 0.5 and foundHalf == False:
                #    second = float(int(second))+0.5
                #    if second == counter + 0.5:
                #        correction = str(second)
                #        for token in tokens[1:]:
                #            correction += ',' + token
                #        listLines.append(correction)
                #        foundHalf = True

                elif addHash:
                    listLines.append("#")
                    listLines.append(str(second))
                    counter += 2
                    print("HELP")

                else:
                    listLines.append(line)

        # Second, write those changes

        filename = completeDirectory + '/' + file.name

        with open(filename,"w") as fileComplete:

            fileComplete.write("".join(listLines))

            """

# Iterate over files from completeDirectory

print("-------------MAKING INPUTS-TRAD-------------")
for file in os.scandir(completeDirectory):
    if file.is_file():
        print(file.name.split('.')[0] + ".csv")

        # Third, we generate csv data from the input

        # Tokens: 0-7, 8 in total
        # ElapsedSeconds , LJ_X , LJ_Y , RT , A , B , RJ_X , RJ_Y

        filename = completeDirectory + '/' + file.name

        with open(filename,'r') as fileComplete:

            listLines = []
            lines = fileComplete.readlines()

            listLines.append("Minute,NumConfirmPresses,NumBreakPresses,PercentageOfMovement,PercentageOfRoll,PercentageOfThruster,AverageThrusterIntensity")

            minute = 1

            numInputs = 0
            numConfirm = 0
            numBreak = 0
            numMovement = 0
            numRoll = 0
            numThruster = 0
            sumThruster = 0

            A_Pressed = False
            B_Pressed = False

            for line in lines[1:]:
                tokens = line.split(',')
                seconds = float(tokens[0])
                movementX = float(tokens[1])
                movementY = float(tokens[2])
                thruster = float(tokens[3])
                aButton = float(tokens[4])
                bButton = float(tokens[5])
                rollX = float(tokens[6])
                rollY = float(tokens[7])

                numInputs += 1

                if seconds >= minute * 60:
                    if(numInputs > 0):
                        movementPercentage = round((numMovement/numInputs)*100,2)
                        rollPercentage = round((numRoll/numInputs)*100,2)
                        if(numThruster > 0):
                            thrusterPercentage = round((numThruster/numInputs)*100,2)
                            averageThruster = round(sumThruster/numThruster,2)
                        else:
                            thrusterPercentage = 0
                            averageThruster = 0
                    else:
                        movementPercentage = 0
                        rollPercentage = 0
                        thrusterPercentage = 0
                        averageThruster = 0

                    listLines.append(str(minute) + ',' + str(numConfirm) + ',' + str(numBreak) + ',' + str(movementPercentage) + ',' + str(rollPercentage) + ',' + str(thrusterPercentage) + ',' + str(averageThruster))
                    
                    minute += 1
                    
                    # Reset variables
                    numInputs = 0
                    numConfirm = 0
                    numBreak = 0
                    numMovement = 0
                    numRoll = 0
                    numThruster = 0
                    sumThruster = 0
                    A_Pressed = False
                    B_Pressed = False

                # Check confirm presses
                if aButton != 0 and not A_Pressed:
                    A_Pressed = True
                    numConfirm += 1
                
                elif aButton == 0:
                    A_Pressed = False

                # Check break presses
                if bButton != 0 and not A_Pressed:
                    B_Pressed = True
                    numBreak += 1
                
                elif bButton == 0:
                    B_Pressed = False

                # Check movement
                if movementX != 0.0 or movementY != 0.0:
                    numMovement += 1

                # Check roll
                if rollX != 0.0 or rollY != 0.0:
                    numRoll += 1

                # Check thruster
                if thruster != 0:
                    numThruster += 1
                    sumThruster += thruster

        # Fourth, we write the CSV file for that input

        filename = csvDirectory + '/' + file.name.split('.')[0] + ".csv"

        with open(filename,'w') as fileCSV:
            fileCSV.write("\n".join(listLines))

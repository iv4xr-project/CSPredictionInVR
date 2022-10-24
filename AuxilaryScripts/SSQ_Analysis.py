import os

script_dir = os.path.dirname(__file__)

# Calculate the SSQ from the .csv

with open(os.path.join(script_dir, "../CSV_Data/STATS/SSQ.csv"),"r") as fileInput:
    listLines = []
    medianList = []

    lines = fileInput.readlines()
    
    listLines.append("Id,Nausea,Oculomotor,Disorientation,TotalScore")

    for line in lines:
        tokens = line.split(",")
        correction = tokens[0] + ","

        nausea = round((int(tokens[1]) + int(tokens[6]) + int(tokens[7]) + int(tokens[8]) + int(tokens[9]) + int(tokens[15]) + int(tokens[16]))*9.54,2)
        oculomotor = round((int(tokens[1]) + int(tokens[2]) + int(tokens[3]) + int(tokens[4]) + int(tokens[5]) + int(tokens[9]) + int(tokens[11]))*7.58,2)
        disorientation = round((int(tokens[5]) + int(tokens[8]) + int(tokens[10]) + int(tokens[11]) + int(tokens[12]) + int(tokens[13]) + int(tokens[14]))*13.92,2)
        totalScore = round((nausea+oculomotor+disorientation)*3.74,2)

        correction += str(nausea) + "," + str(oculomotor) + "," + str(disorientation) + "," + str(totalScore)
        listLines.append(correction)
        medianList.append(totalScore)

    medianList.sort()
    mid = len(medianList) // 2
    median = (medianList[mid] + medianList[~mid]) / 2

# Write the results in a new file

with open(os.path.join(script_dir, "../CSV_Data/STATS/PROCESSED_SSQ.csv"),"w") as fileOutput:
    fileOutput.write("\n".join(listLines))

# Add group tag

with open(os.path.join(script_dir, "../CSV_Data/STATS/PROCESSED_SSQ.csv"),"r") as fileInput:
    listLines = []

    lines = fileInput.readlines()

    listLines.append(lines[0][:-1] + ",Group")
    lines = lines[1:]
    
    group = ""

    for line in lines:
        tokens = line.split(",")
        if(float(tokens[4]) < median):
            group = "LOW"
        else:
            group = "HIGH"
        listLines.append(line[:-1] + "," + group)

with open(os.path.join(script_dir, "../CSV_Data/STATS/PROCESSED_SSQ.csv"),"w") as fileOutput:
    fileOutput.write("\n".join(listLines))
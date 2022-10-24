import os

script_dir = os.path.dirname(__file__)

# Calculate the MSSQ from the .csv

with open(os.path.join(script_dir, "../CSV_Data/STATS/MSSQ.csv"),"r") as fileInput:
    listLines = []

    lines = fileInput.readlines()
    
    listLines.append("Id,MSA,MSB,MSSQ Raw score")

    medianList = []
    for line in lines:
        tokens = line.split(",")
        correction = tokens[0] + ","
        tokensChild = tokens[1:10]
        tokensAdult = tokens[10:]

        numTChild = 0
        numTAdult = 0
        totalChild = 0
        totalAdult = 0

        for token in tokensChild:
            if(token == "t" or token == "t\n"):
                numTChild += 1
            else:
                totalChild += int(token)
        
        MSA_score = round((totalChild*9)/(9-numTChild),2)
        correction += str(MSA_score) + ","
        
        for token in tokensAdult:
            if(token == "t" or token == "t\n"):
                numTAdult += 1
            else:
                totalAdult += int(token)
        
        MSB_score = round((totalAdult*9)/(9-numTAdult),2)
        correction += str(MSB_score) + ","

        rawScore = round(MSA_score + MSB_score,2)

        medianList.append(rawScore)

        correction += str(rawScore)
        
        listLines.append(correction)
    
    medianList.sort()
    mid = len(medianList) // 2
    median = (medianList[mid] + medianList[~mid]) / 2


# Write the results in a new file

with open(os.path.join(script_dir, "../CSV_Data/STATS/PROCESSED_MSSQ.csv"),"w") as fileOutput:
    fileOutput.write("\n".join(listLines))

# Add group tag

with open(os.path.join(script_dir, "../CSV_Data/STATS/PROCESSED_MSSQ.csv"),"r") as fileInput:
    listLines = []

    lines = fileInput.readlines()

    listLines.append(lines[0][:-1] + ",Group")
    lines = lines[1:]
    
    group = ""

    for line in lines:
        tokens = line.split(",")
        if(float(tokens[3]) < median):
            group = "LOW"
        else:
            group = "HIGH"
        listLines.append(line[:-1] + "," + group)

with open(os.path.join(script_dir, "../CSV_Data/STATS/PROCESSED_MSSQ.csv"),"w") as fileOutput:
    fileOutput.write("\n".join(listLines))
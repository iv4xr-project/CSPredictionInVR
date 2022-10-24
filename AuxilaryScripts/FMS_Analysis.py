from statistics import mean, median

import os

script_dir = os.path.dirname(__file__)

# This function is subject to change and will determine whether or not the current experiment is to be considered - if it's valid
# at the moment, if the subjects had low scores, meaning they felt barely any changes, we check half of the median variation
# median of variation is 6,5
# mean of variation is 8.272727272727273

def checkIfExperimentIsValid(index, variation, groupFMS, groupSSQ):
    print(index,variation,groupFMS, groupSSQ)
    if (groupFMS[0] == "L") or (groupSSQ[0] == "L"):
        return variation >= 4.5
    elif (groupFMS[0] == "L") or (groupSSQ[0] == "L"):
        return variation >= 5.5
    else:
        return variation >= 6.5

# This function is subject to change and will return each of the experiment's values as a tag of 0 or 1
# 1 means there is motion sickness. 0 means there isn't

# Using the medianFMSScore yields a 0:145 and 1:288 split
# Using the meanFMSScore yields a 0:218 and 1:215 split
# Using the halfVariation yields a 0:260 and 1:173 split

# Seems like using the mean yields a better 50/50 split

def createTag(index, line, variation):
    tokens = line.split(",")
    tokens = tokens[1:]
    correction = str(index)

    medianFMSScore = median(medianFMSScoreList[index])
    meanFMSScore = mean(medianFMSScoreList[index])
    halfVariation = variation/2

    for token in tokens:
        value = int(token)
        if value >= halfVariation:
            value = 1
        else:
            value = 0
        correction += "," + str(value)
    return correction

# Start by reading the FMS csv file and start preparing modifications
# We also check for the susceptibility based on the FMS. We check if it's below 6 for LOW and greater than or equal to 6 if it's HIGH,
#   in accordance with a paper we have checking the validty of FMS with the SSQ

with open(os.path.join(script_dir, "../CSV_Data/TAGS/FMS.csv"),'r') as fileInput:
    listLines = []

    lines = fileInput.readlines()
    listSusceptibility = ["LOW"]*22
    
    for i in range(len(lines)):
        tokens = lines[i].split(",")
        baseline = int(tokens[1])
        correction = tokens[0] + ",0"
        tokens = tokens[2:]
        for token in tokens:
            value = int(token)
            if(value >= 6.5):
                listSusceptibility[i] = "HIGH"
            if(value < baseline):
                value = baseline
        for token in tokens:
            value = int(token)
            value -= baseline
            correction+=","+str(value)
        listLines.append(correction)

# Write modifications in a new file

with open(os.path.join(script_dir, "../CSV_Data/TAGS/FMS_Modified.csv"),"w") as fileOutput:
    fileOutput.write("\n".join(listLines))

# Read the modifications and start preparing statistics and the tag

with open(os.path.join(script_dir, "../CSV_Data/TAGS/FMS_Modified.csv"),"r") as fileInput:
    fileSSQ = open(os.path.join(script_dir, "../CSV_Data/STATS/PROCESSED_SSQ.csv"),"r")
    fileMSSQ = open(os.path.join(script_dir, "../CSV_Data/STATS/PROCESSED_MSSQ.csv"),"r")
    linesSSQ = fileSSQ.readlines()[1:]
    linesMSSQ = fileMSSQ.readlines()[1:]
    
    listLinesStatistics = []
    listLinesTag = []
    medianFMSScoreList = [[]] * 22
    totalMedianFMSSCoreList = []
    medianVariationList = []
    meanVariation = 0

    listLinesStatistics.append("ID,MSSQ,FMS,SSQ,Valid?,Baseline,Max,Variation")

    lines = fileInput.readlines()

    for i in range(len(lines)):
        tokens = lines[i].split(',')
        
        baseline = int(tokens[1])
        max = baseline
        medianFMSScoreList[i].append(baseline)

        tokens = tokens[2:]
        for token in tokens:
            value = int(token)
            medianFMSScoreList[i].append(value)
            if value >= max:
                max = value
        variation = max - baseline
        totalMedianFMSSCoreList.append(max)
        
        medianVariationList.append(variation)
        meanVariation += variation

        groupMSSQ = linesMSSQ[i].split(",")[4]
        groupFMS = listSusceptibility[i]
        groupSSQ = linesSSQ[i].split(",")[5]

        isValid = checkIfExperimentIsValid(i, variation, groupFMS, groupSSQ)
        if(isValid):
            listLinesTag.append(createTag(i, lines[i], variation))

        listLinesStatistics.append(groupMSSQ[:-1] + "," + groupFMS + "," + groupSSQ[:-1] + "," + str(i) + "," + str(isValid) + "," + str(baseline) + "," + str(max) + "," + str(variation))

    print("Median:",median(medianVariationList))
    print("Mean:",meanVariation/len(lines))
    print("Median FMS Score:", median(totalMedianFMSSCoreList))
    print(totalMedianFMSSCoreList)

    fileSSQ.close()
    fileMSSQ.close()

# Write the stastistics of the modified file on a new file

with open(os.path.join(script_dir, "../CSV_Data/TAGS/FMS_Statistics.csv"),"w") as fileStatistics:
    fileStatistics.write("\n".join(listLinesStatistics))

# Write the tag in a new file

with open(os.path.join(script_dir, "../CSV_Data/TAGS/FMS_Tag.csv"),"w") as fileOutput:
    fileOutput.write("\n".join(listLinesTag))
import cv2 #OpenCv package
import numpy as np
import os
from matplotlib import pyplot as plt
from scipy.stats import skew
from scipy.stats import kurtosis
import pandas as pd
from skimage.measure import shannon_entropy
import statistics

script_dir = os.path.dirname(__file__)
videosDirectory = os.path.join(script_dir, '../RECORDINGS/LOW_RES')

for file in os.scandir(videosDirectory):
    if file.is_file():
        title = file.name.split('.')[0]
        filename = videosDirectory + '/' + file.name
        video = cv2.VideoCapture(filename)

        frameCount = 0
        frames = video.get(cv2.CAP_PROP_FRAME_COUNT)
        fps = int(video.get(cv2.CAP_PROP_FPS))
        duration = int(frames/fps)
        timestep = 60
        framesPerTimestep = fps * timestep
        
        print(file.name,duration//60,frames)

        width = int(video.get(3))
        height = int(video.get(4))

        # HSV initialization
        hueList = []
        satList = []
        brightList = []

        hue = {}
        [hue.setdefault(i, 0) for i in range(32)] 
        sat = {}
        [sat.setdefault(i, 0) for i in range(32)] 
        bright = {}
        [bright.setdefault(i, 0) for i in range(32)] 

        # Motion Intensity Initialization

        flowList = []
        meanFlowList = []
        stdDevFlowList = []
        skewnessFlowList = []
        kurtosisFlowList = []
        maxFlowList = []
        minFlowList = []
        varianceFlowList = []

        # Contrast Initialization

        contrastList = []
        meanContrastList = []
        stdDevContrastList = []
        skewnessContrastList = []
        kurtosisContrastList = []
        maxContrastList = []
        minContrastList = []
        varianceContrastList = []

        """
        # Smoothness Initialization

        meanSmoothnessList = []
        stdDevSmoothnessList = []
        maxSmoothnessList = []
        minSmoothnessList = []
        varianceSmoothnessList = []

        meanSmoothnessListTemp = []
        stdDevSmoothnessListTemp = []
        maxSmoothnessListTemp = []
        minSmoothnessListTemp = []
        varianceSmoothnessListTemp = []
        """

        # Entropy Initialization

        entropyList = []
        meanEntropyList = []
        stdDevEntropyList = []
        skewnessEntropyList = []
        kurtosisEntropyList = []
        maxEntropyList = []
        minEntropyList = []
        varianceEntropyList = []

        while True:
            elapsedSeconds = frameCount/fps
            #print("frameCount:",frameCount, "  elapsedSeconds: ", elapsedSeconds)

            ret, frameImg = video.read()
            frameCount+=1

            #if(elapsedSeconds > 120): break

            if(elapsedSeconds%timestep == 0 and elapsedSeconds > 0):
                print("     TIMESTEP: ", elapsedSeconds/timestep)

                # HSV statistics
                hueList.append(hue)
                satList.append(sat)
                brightList.append(bright)

                # Motion Intensity statistics
                meanFlowList.append(statistics.mean(flowList))
                stdDevFlowList.append(statistics.stdev(flowList))
                skewnessFlowList.append(skew(flowList))
                kurtosisFlowList.append(kurtosis(flowList))
                maxFlowList.append(max(flowList))
                minFlowList.append(min(flowList))
                varianceFlowList.append(statistics.variance(flowList))

                # Contrast statistics
                meanContrastList.append(statistics.mean(contrastList))
                stdDevContrastList.append(statistics.stdev(contrastList))
                skewnessContrastList.append(skew(contrastList))
                kurtosisContrastList.append(kurtosis(contrastList))
                maxContrastList.append(max(contrastList))
                minContrastList.append(min(contrastList))
                varianceContrastList.append(statistics.variance(contrastList))

                """
                # Smoothness statistics
                meanSmoothnessList.append(np.median(meanSmoothnessListTemp))
                stdDevSmoothnessList.append(np.median(stdDevSmoothnessListTemp))
                maxSmoothnessList.append(np.median(maxSmoothnessListTemp))
                minSmoothnessList.append(np.median(minSmoothnessListTemp))
                varianceSmoothnessList.append(np.median(varianceSmoothnessListTemp))
                """

                # Entropy statistics
                meanEntropyList.append(statistics.mean(entropyList))
                stdDevEntropyList.append(statistics.stdev(entropyList))
                skewnessEntropyList.append(skew(entropyList))
                kurtosisEntropyList.append(kurtosis(entropyList))
                maxEntropyList.append(max(entropyList))
                minEntropyList.append(min(entropyList))
                varianceEntropyList.append(statistics.variance(entropyList))

                # Reset temporary variables

                hue = {}
                [hue.setdefault(i, 0) for i in range(32)] 
                sat = {}
                [sat.setdefault(i, 0) for i in range(32)] 
                bright = {}
                [bright.setdefault(i, 0) for i in range(32)]

                flowList = []
                contrastList = []
                entropyList = []

                """
                meanSmoothnessListTemp = []
                stdDevSmoothnessListTemp = []
                maxSmoothnessListTemp = []
                minSmoothnessListTemp = []
                varianceSmoothnessListTemp = []
                """

            if(elapsedSeconds >= duration): break

            # HSV Capture

            hsv = cv2.cvtColor(frameImg, cv2.COLOR_BGR2HSV)
            h,s,v = cv2.split(hsv)
            for j in range(len(h)):
                for k in range(len(h[j])):
                    hue[h[j][k]//8] += 1
                    sat[s[j][k]//8] += 1
                    bright[v[j][k]//8] += 1

            # Motion Intensity Capture

            if(elapsedSeconds > 0):
                gray = cv2.cvtColor(frameImg, cv2.COLOR_BGR2GRAY)
                flow = cv2.calcOpticalFlowFarneback(prevgray, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
                prevgray = gray

                # We use the mean of the flow because why not and I don't think we should just use the entire flow for all timestep*fps frames
                flowList.append(np.mean(flow))

            else:
                prevgray = cv2.cvtColor(frameImg, cv2.COLOR_BGR2GRAY)

            # Contrast & Entropy Capture
            contrastList.append(prevgray.std()) #RMS contrast
            entropyList.append(shannon_entropy(prevgray)) #Shannon Entropy

            # Display
            #cv2.imshow('frame', hsv)
            #if(elapsedSeconds > 0):
            #    cv2.imshow('flow', draw_flow(gray, flow))
            #    cv2.imshow('flow HSV', draw_hsv(flow))

            if cv2.waitKey(1) == ord("q"):
                break

        # Create Data Frames

        motionDataFrame = pd.DataFrame()
        motionDataFrame['Mean'] = meanFlowList
        motionDataFrame['Std'] = stdDevFlowList
        motionDataFrame['Skweness'] = skewnessFlowList
        motionDataFrame['Kurtosis'] = kurtosisFlowList
        motionDataFrame['Max'] = maxFlowList
        motionDataFrame['Min'] = minFlowList
        motionDataFrame['Var'] = varianceFlowList

        contrastDataFrame = pd.DataFrame()
        contrastDataFrame['Mean'] = meanContrastList
        contrastDataFrame['Std'] = stdDevContrastList
        contrastDataFrame['Skweness'] = skewnessContrastList
        contrastDataFrame['Kurtosis'] = kurtosisContrastList
        contrastDataFrame['Max'] = maxContrastList
        contrastDataFrame['Min'] = minContrastList
        contrastDataFrame['Var'] = varianceContrastList

        entropyDataFrame = pd.DataFrame()
        entropyDataFrame['Mean'] = meanEntropyList
        entropyDataFrame['Std'] = stdDevEntropyList
        entropyDataFrame['Skweness'] = skewnessEntropyList
        entropyDataFrame['Kurtosis'] = kurtosisEntropyList
        entropyDataFrame['Max'] = maxEntropyList
        entropyDataFrame['Min'] = minEntropyList
        entropyDataFrame['Var'] = varianceEntropyList

        hueDataFrame = pd.DataFrame.from_dict(hueList, orient='columns')

        satDataFrame = pd.DataFrame.from_dict(satList, orient='columns')

        brightDataFrame = pd.DataFrame.from_dict(brightList, orient='columns')


        # Write to CSV
        videoStatsDirectory = os.path.join(script_dir, '../CSV_Data/VIDEOS/'+title+'/')

        motionDataFrame.to_csv(videoStatsDirectory+title+"_motion.csv")
        contrastDataFrame.to_csv(videoStatsDirectory+title+"_contrast.csv")
        entropyDataFrame.to_csv(videoStatsDirectory+title+"_entropy.csv")
        hueDataFrame.to_csv(videoStatsDirectory+title+"_hue.csv")
        satDataFrame.to_csv(videoStatsDirectory+title+"_sat.csv")
        brightDataFrame.to_csv(videoStatsDirectory+title+"_bright.csv")

        video.release()
        cv2.destroyAllWindows()

        print("ended at: ", elapsedSeconds,"  Minutes: ", int(elapsedSeconds/60))
        print("----------------------------------------------------------------")
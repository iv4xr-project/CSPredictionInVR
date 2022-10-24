# CSPredictionInVR
This repository contains the work of Tiago Gonçalves for his master theisis. 
A program to generate a machine learning model capable of predicting Cybersickness in VR video recordings


There are two versions of the program. One in the shape of a .py python script and the other in the format belonging to the platform it was intended for, google colabs

The remaining folders have self-explaining names. CSV_DATA contains all the data that was used, most in csv format, with a few exceptions here and there. Both the program and the auxiliary scrips make use of these files for various purposes, not least of which constructing the various models.
RECORDINGS contains the video recordings, already down-sampled into the required format.

The auxiliary scripts folder contains various scripts that were used to generate some of the data files. While a lot of them were reimplemented in the main program, located in the root of the repository, some functionality was not. For instance, SSQ and MSSQ processing, labeling and video down-sampling are among the functionalities that are not present in the main program and must therefore be executed externally so they may do the necessary data processing.

For all the scripts, some modifications might be necessary for them to function on a new system. These mostly comprise of simply changing the directory from which the scripts access the data. I have made this process as painless and well documented as possible but discretion is advised.

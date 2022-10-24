#!/bin/bash

# This script was used to perform the necessary down-sampling
# The videos present in the RECORDINGS folder are already down-sampled
# This script remains purely for educational or adaption purposes 

cd ..
cd RECORDINGS
mkdir LOW_RES
for f in *
do
ffmpeg -i "$f" -vf scale=320:180 LOW_RES/"$f"
done

cd LOW_RES
mkdir LOW_FPS
for f in *
do
ffmpeg -i "$f" -filter:v fps=fps=2 LOW_FPS/"$f" 
done
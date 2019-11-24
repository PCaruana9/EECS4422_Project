import cv2
import numpy as np
import os

f = open("nameList")
nameString = f.read()
nameList = nameString.splitlines()
f.close()

outDir = "HumanMaps/"
inDir = "TestResults/"

for i in range(len(nameList)):
    prefix = nameList[i]
    print("Processing Prefix: " + prefix)
    files = [filename for filename in os.listdir(inDir) if filename.startswith(prefix)]
    combo = np.zeros_like(cv2.imread(inDir+files[0], 0)).astype(float)
    for x in range(len(files)):
        combo += cv2.GaussianBlur(np.array(cv2.imread(inDir+files[x],0)).astype(float), (31,31),10)

    combo *= combo # Squareing for min-maxing
    max = np.max(combo)
    combo = combo/max
    combo *= combo
    combo = cv2.GaussianBlur(combo, (5, 5), 3)
    cv2.imwrite(outDir+prefix+"_map.png", combo*255)
print("Donezo homie")

import cv2
import numpy as np

filename = "TestResults/HANGAR_1450_take1_mmap_ptcp_001.jpg"
img1 = cv2.imread(filename, 0)


filename = "TestResults/BAY_3220_take3_mmap_ptcp_001.jpg"
img2 = cv2.imread(filename, 0)


img1 = np.array(cv2.GaussianBlur(img1, (25, 25), 10)).astype(float)


img2 = np.array(cv2.GaussianBlur(img2, (25, 25), 10)).astype(float)


combo = 3*img1 + 10*img2
combo *= combo #squaring for soft max
max = np.max(combo)
print(max)
combo /= max
combo = cv2.GaussianBlur(combo, (25,25), 10)
cv2.imshow("", combo)
cv2.waitKey(0)
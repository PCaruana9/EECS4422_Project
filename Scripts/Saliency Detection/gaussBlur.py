import cv2
import numpy as np
from math import sqrt

def alphaBlend(img1, img2, mask):
    """ alphaBlend img1 and img 2 (of CV_8UC3) with mask (CV_8UC1 or CV_8UC3)
    """
    if mask.ndim==3 and mask.shape[-1] == 3:
        alpha = mask/255.0
    else:
        alpha = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)/255.0
    blended = cv2.convertScaleAbs(img1*(1-alpha) + img2*alpha)
    return blended

def euclidian_distance(center, point):
	XX = center[1] - point[1]
	YY = center[0] - point[0]
	dist = sqrt((XX*XX) + (YY*YY))
	R=150
	if dist > R:
		return 250
	else:
		return dist

def gradientMask( center, size):
	#compute euclidian distance
	temp = np.zeros((size[1],size[0],1))
	for x in range(0,size[1]):
		for y in range(0,size[0]):
			point = (y,x)
			temp[y,x] =  euclidian_distance(center,point) 
	return temp
	
size = (500,500)
mask = gradientMask((250,250), size)

Imask = np.zeros((500,500,1), np.uint8)
max = np.amax(mask)

mk = 1 - mask/max
mask = 255 - mask/max*255



mask = cv2.GaussianBlur(mask, (101,101), 10)
mask[240:260, 240:260] = 255
mask = cv2.GaussianBlur(mask, (101,101), 10)
mask[240:260, 240:260] = 255
mk = cv2.GaussianBlur(mk, (101,101), 10)
mask = cv2.GaussianBlur(mask, (101,101), 10)

for i in range(0,500):
	for j in range(0,500):
		new = int(mask[i,j]*1.4)
		if (new > 255):
			new = 255
		mask[i,j] = new

mask = cv2.GaussianBlur(mask, (51,51), 10)

Imask = mask.astype(np.uint8)


#cv2.imwrite("PeripheralMask.jpg", Imask)

Imask = cv2.cvtColor(Imask.astype('uint8'), cv2.COLOR_GRAY2RGB)


img = cv2.imread("Firefox_wallpaper.png")
blur = cv2.GaussianBlur(img, (101,101), 10)

blanc = np.zeros((1080,1920,3), np.uint8)
blanc[200:700, 700:1200] = Imask
alpha = blanc/255

b1 = alphaBlend(img, blur, 255 - blanc)


#cv2.imwrite("PeripheralExample.jpg", b1)
















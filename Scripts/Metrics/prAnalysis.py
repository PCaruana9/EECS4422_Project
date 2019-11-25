import cv2
import numpy as np

#Core Functions -------------------------------------------

def roi_score(alpha,beta,R):
    X = R.shape[1]
    Y = R.shape[0]
    # print("X, Y = %d, %d" %(X,Y))
    H = Y - 1
    W = X - 1
    N = X*Y
    #small heuristic, if an element in an integral image is 0, so are all the elements above and left.
    if R[H,W] == 0:
        return 0
    #integral sum, R(H,W) = r(H,W) + r(0,0) + r(H,0) + r(0,W)
    Rs = R[H,W] + R[0,0] - R[H,0] - R[0,W]
    Rs = alpha*Rs - beta*N #no need to multiply by alpha every time.
    return Rs


# Output roi image, with same aspect ratio as input
# returns roi_coords, with format (p, q, w, h)
# p,q are the x,y coords of the box, w,h are the width and height.
# roi_coords[0] = p
# roi_coords[1] = q
# roi_coords[2] = w
# roi_coords[3] = l
def generate_roi(salmap, thresh, alpha, beta):

    roi_coords = None
    bestROI = 0;
    # Format of roi_coords(x,y,w,h) -> (x,y)= top left corner, (w,h)-> width and height of box
    #compute integral image, to speed things up
    retval, threshSalMap = cv2.threshold(salmap,thresh,255,cv2.THRESH_BINARY)
    threshSalMap = threshSalMap/255
    # print(np.max(threshSalMap))
    # disp(threshSalMap)
    intMap = np.array(cv2.integral(threshSalMap))

    W = salmap.shape[1]
    H = salmap.shape[0]
    aspect = H/W


    # Scans areas with proper aspect ratio
    # for a bit of computational speed, I assume aspect ratios smaller than 25x25 wont ever be
    # an roi, because they are too small anyways.
    for i in range(25,W+1):
        x = i
        y = i*aspect
        #if y is a whole number
        if y == int(y):
            y = int(y)
            # print("Testing shape: " + str((y,x)))
            # if (x,y) is proper aspect ratio, scan accross image computing ROI
            for p in range(0, W - x):
                for q in range(0, H - y):
                    # print("p:%d, x:%d, q:%d, y:%d" %(p,x,q,y))
                    rsScore = roi_score(alpha,beta,intMap[q:q+y, p:p+x])

                    if rsScore > bestROI:
                        bestROI = rsScore
                        roi_coords = (p,q,x,y)
                        # suppress prints for use.
                        # print("New record! Best ROI is: " + str(rsScore) + " -> At " + str(roi_coords))




    return roi_coords

def salience_score_roi(map, roi):
    score = 0
    missed = 0
    mapW = map.shape[1] - 1
    mapH = map.shape[0] - 1
    x = roi[0]; xW = x + roi[2];
    y = roi[1]; yH = y + roi[3];
    roiSize = roi[2]*roi[3]
    missSize = map.shape[1]*map.shape[0] - roiSize
    hitSum = int(map[yH, xW] + map[y, x] - map[yH, x] - map[y, xW])
    missedSum = int(map[mapH,mapW] + map[0,0] - map[mapH,0] - map[0,mapW]) - hitSum
    # Sum of entire map minus sum from roi

    score = hitSum/roiSize
    missed = missedSum/missSize
    return score, missed

def mask_score_roi(mask, roi):
    # True Positive: ROI includes pixel which is part of ground truth mask
    # False Negative: Part of the ground truth mask is not included in the ROI
    # False Positive: ROI Includes a pixel outside of the bounding of the mask.

    # precision def: True Positive/(True Positive + False Positive)
    # recall def: True Positive/(True Positive + False Negative)
    precision = 0
    recall = 0

    TPos = 0
    FNeg = 0
    FPos = 0  # True positive, false negative and false positive counts

    maskWid = mask.shape[1]
    maskLen = mask.shape[0]

    for x in range(0, maskWid):
        for y in range(0, maskLen):
            if is_true_pos(x, y, mask, roi):
                TPos += 1
            elif is_false_pos(x, y, mask, roi):
                FPos += 1
            elif is_false_neg(x, y, mask, roi):
                FNeg += 1

    precision = TPos / (TPos + FPos)
    recall = TPos / (TPos + FNeg)

    return precision, recall

#Query Functions---------------------------------------------
	
def is_true_pos(x, y, mask, roi):
    if is_within_roi(x, y, roi):
        if mask[y, x] == 255:
            return True
    return False

def is_false_neg(x, y, mask, roi):
    if not is_within_roi(x, y, roi):
        if mask[y, x] == 255:
            return True
    return False

def is_false_pos(x, y, mask, roi):
    if is_within_roi(x, y, roi):
        if not (mask[y, x] == 255):
            return True
    return False

def is_within_roi(x, y, roi):
    return (x >= roi[0]) and (x < roi[0]+roi[2]) and (y >= roi[1]) and (y < roi[1]+roi[3])
	
# MAIN ------------------------------------------------------

if __name__ == "__main__":

	# import base file names
    f = open("nameList", "r")
    fileString = f.read()
    nameList = fileString.splitlines()
    f.close()
	
	models = ["AWS", "IKN", "GBVS", "DVA", "RARE2012"]
	
	
	
	
	



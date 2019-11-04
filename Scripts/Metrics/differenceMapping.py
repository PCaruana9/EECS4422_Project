import cv2
import numpy as np

def create_heatmap(bin_img):
	#Blue = Similar, Magenta = Different
	img = cv2.applyColorMap(bin_img, cv2.COLORMAP_JET)
	return img

print("Running: differenceMapping.py")
print("Generating heatmap of differences")

dir = "/home/peter/Programming/EECS_4422_Project/Results/Test/AIM/"

for XX in range(0,11):
	index = str(1000+XX)
	file = index +".jpg"
	img_IR = cv2.imread(dir+"/IR_"+index+".jpg",0)
	img_VIS = cv2.imread(dir+"/VIS_"+index+".jpg",0)

	height = img_IR.shape[0]
	width = img_IR.shape[1]
	
	
	diff_img = np.zeros((height,width,1), np.uint8)

	for y in range(0,height):
		for x in range(0,width):
			p_IR = img_IR[y,x]
			p_VIS = img_VIS[y,x]
	
			diff = int(p_IR) - int(p_VIS)
			diff = np.absolute(diff)
			diff = diff
			
			R = diff
			diff_img[y,x] = R	#Red pixel, very different
	
			#print("p_IR=%d, p_VIS=%d, diff=%f, B=%d, R=%d" %(p_IR, p_VIS, diff, B, R))

	output = create_heatmap(diff_img)
	cv2.imwrite(dir+file, output)
	print("Saved " + file)
	
exit()

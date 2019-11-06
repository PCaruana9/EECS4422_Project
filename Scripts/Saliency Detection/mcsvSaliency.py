import cv2
import pygame
import numpy as np
from pygame.locals import *


def alphaBlend(img1, img2, mask):
    """ alphaBlend img1 and img 2 (of CV_8UC3) with mask (CV_8UC1 or CV_8UC3)
    """
    if mask.ndim==3 and mask.shape[-1] == 3:
        alpha = mask/255.0
    else:
        alpha = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)/255.0
    blended = cv2.convertScaleAbs(img1*(1-alpha) + img2*alpha)
    return blended

def compute_blur(mouseLocation, img, blur, mask):
	Smask = np.zeros((866,1300,3))
	W = mouseLocation[0]
	H = mouseLocation[1]
	for X in range(W-250+1,W+250-1):
		for Y in range(H-250+1, H+250-1):
			if(not(X < 0) and not(X > 1300) and not(Y < 0) and not(Y > 1300)):
				Smask[Y,X] = mask[Y-H+250, X-W+250] #Centers mask at cursor
			
	new = alphaBlend(img, blur, 255 - Smask)
	return new
	
	
pygame.init() #Activates pygame


bg = cv2.imread("almonds.jpg",1)
blurBg = cv2.GaussianBlur(bg, (101,101), 10)
mask = cv2.imread("PeripheralMask.jpg")


scale = (bg.shape[1],bg.shape[0])

x = y = 0
running = 1
timeElapsed = 0
clock = pygame.time.Clock()
screen = pygame.display.set_mode(scale)

frame = bg
frame = frame.swapaxes(0,1)
frame = pygame.surfarray.make_surface(frame)
while running:
	event = pygame.event.poll()

	dt = clock.tick()
	timeElapsed += dt
	if(timeElapsed > 2): #only updates every 5ms
		if event.type == pygame.QUIT:
			running = 0
		elif event.type == pygame.MOUSEMOTION:
			print("mouse at (%d, %d)" %(event.pos))

			 
			blurImg = compute_blur(event.pos, bg, blurBg, mask)
			frame = blurImg 
			frame = frame.swapaxes(0,1)
			frame = pygame.surfarray.make_surface(frame) 
			if event.pos == (300,200):
				screen = pygame.display.set_mode(scale)
		timeElapsed = 0
 		


	screen.blit(frame,(0,0))
	
	#screen.fill((0, 0, 0))
	pygame.display.flip()






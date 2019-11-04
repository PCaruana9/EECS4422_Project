import cv2
import pygame
import numpy as np
from pygame.locals import *
from math import sqrt



def compute_blur(mouseLocation, img):
	
	return final
	
	

pygame.init() #Activates pygame

x = y = 0
running = 1
timeElapsed = 0
clock = pygame.time.Clock()
screen = pygame.display.set_mode((720,480))
bg = cv2.imread("/home/peter/Programming/EECS_4422_Project/ImgDatasets/Patio/Patio_take_1/take_1/VIS/VIS_4730.jpg")


scale = (720,480)
frame = bg
frame = frame.swapaxes(0,1)
frame = pygame.surfarray.make_surface(frame)
while running:
	event = pygame.event.poll()

	dt = clock.tick()
	timeElapsed += dt
	if(timeElapsed > 500):
		if event.type == pygame.QUIT:
			running = 0
		elif event.type == pygame.MOUSEMOTION:
			print "mouse at (%d, %d)" % event.pos

			 #only updates every 250ms
			blurImg = compute_blur(event.pos, bg)
			frame = blurImg 
			frame = frame.swapaxes(0,1)
			frame = pygame.surfarray.make_surface(frame) 
			if event.pos == (300,200):
				screen = pygame.display.set_mode((720, 480))
		timeElapsed = 0
 		


	screen.blit(frame,(0,0))
	
	#screen.fill((0, 0, 0))
	pygame.display.flip()






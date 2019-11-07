import cv2
import pygame
import numpy as np
from pygame.locals import *
import time


class saliency_analog:

    def alphaBlend(self, img1, img2, mask):
        """ alphaBlend img1 and img 2 (of CV_8UC3) with mask (CV_8UC1 or CV_8UC3)
        """
        if mask.ndim == 3 and mask.shape[-1] == 3:
            alpha = mask / 255.0
        else:
            alpha = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR) / 255.0
        blended = cv2.convertScaleAbs(img1 * (1 - alpha) + img2 * alpha)
        return blended

    def compute_blur(self, mouseLocation):
        Smask = np.zeros((self.scale[1], self.scale[0], 3))
        W = mouseLocation[0]
        H = mouseLocation[1]
        for X in range(W - 250 + 1, W + 250 - 1):
            for Y in range(H - 250 + 1, H + 250 - 1):
                if (not (X < 0) and not (X > self.scale[0] - 1) and not (Y < 0) and not (Y > self.scale[1] - 1)):
                    Smask[Y, X] = mask[Y - H + 250, X - W + 250]  # Centers mask at cursor

        new = self.alphaBlend(self.bg, self.blurBg, 255 - Smask)
        return new

    def start(self):
        print("Running")
        bg = self.bg
        scale = [bg.shape[1], bg.shape[0]]
        blurBg = self.blurBg
        self.scale = scale
        x = y = 0
        running = 1
        timeElapsed = 0
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode(scale)

        frame = blurBg
        frame = frame.swapaxes(0, 1)
        frame = pygame.surfarray.make_surface(frame)
        count = 1
        while running:
            event = pygame.event.poll()

            dt = clock.tick()
            timeElapsed += dt
            if (timeElapsed > 1):  # only updates every 5ms
                if event.type == pygame.QUIT:
                    running = 0
                elif event.type == pygame.MOUSEMOTION:
                    print("mouse at (%d, %d)" % (event.pos))

                    pos = event.pos
                    self.computeTime = time.time()

                    blurImg = self.compute_blur(pos)

                    self.computeTime = time.time() - self.computeTime
                    self.totalTime += self.computeTime
                    self.avgComputeTime = (self.computeTime + self.totalTime) / count
                    print(">> Avg Compute time: " + str(self.avgComputeTime))
                    count = count + 1
                    frame = blurImg
                    frame = frame.swapaxes(0, 1)
                    frame = pygame.surfarray.make_surface(frame)
                    if event.pos == (300, 200):
                        screen = pygame.display.set_mode(scale)
                timeElapsed = 0

            screen.blit(frame, (0, 0))

            # screen.fill((0, 0, 0))
            pygame.display.flip()

    def __init__(self, img, mask):
        pygame.init()  # Activates pygame
        self.bg = img
        self.mask = mask
        self.blurBg = cv2.GaussianBlur(img, (101, 101), 10)
        self.avgComputeTime = 0
        self.computeTime = 0
        self.totalTime = 0


mask = cv2.imread("PeripheralMask.jpg")
bg = cv2.imread("almonds.jpg", 1)
bg = cv2.cvtColor(bg, cv2.COLOR_BGR2RGB)
bg = cv2.resize(bg, (int(bg.shape[1] * 0.6), int(bg.shape[0] * 0.6)))
game = saliency_analog(bg, mask)
game.start()

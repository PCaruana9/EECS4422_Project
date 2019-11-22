import cv2
import pygame
import numpy as np
from pygame.locals import *
import time
import random
import keyboard


class saliency_analog:

    def fillLine(self, p1, p2):
        self.mouseMap = cv2.line(self.mouseMap, p1, p2, 255, 3)

    def alphaBlend(self, img1, img2, mask):
        """ alphaBlend img1 and img 2 (of CV_8UC3) with mask (CV_8UC1 or CV_8UC3)
        """
        if mask.ndim == 3 and mask.shape[-1] == 3:
            alpha = mask / 255.0
        else:
            alpha = mask / 255.0  # cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR) / 255.0

        blended = cv2.convertScaleAbs(img1 * (1 - alpha) + img2 * alpha)
        blended = cv2.cvtColor(blended,
                               cv2.COLOR_GRAY2RGB)  # pygame throws a fit when you give it a grayscale img, so convert to colour
        return blended

    def compute_blur(self, mouseLocation):
        Smask = cv2.cvtColor(np.zeros((self.scale[1], self.scale[0], 3), np.uint8), cv2.COLOR_RGB2GRAY)
        W = mouseLocation[0]
        H = mouseLocation[1]
        for X in range(W - 180 + 1, W + 180 - 1):  # 180 is the radius of the mask image
            for Y in range(H - 180 + 1, H + 180 - 1):
                if not (X < 0) and not (X > self.scale[0] - 1) and not (Y < 0) and not (Y > self.scale[1] - 1):
                    Smask[Y, X] = mask[Y - H + 180, X - W + 180]  # Centers mask at cursor

        new = self.alphaBlend(self.bg, self.blurBg, 255 - Smask)
        return new

    def start(self):
        print("Running")
        bg = self.bg
        scale = [bg.shape[1], bg.shape[0]]
        blurBg = self.blurBg
        self.scale = scale
        x = y = 0
        running = 0
        screen = pygame.display.set_mode(scale)

        frame = cv2.cvtColor(blurBg, cv2.COLOR_GRAY2RGB)  # opencv throws a goddamn fit when you give it grayscale.
        frame = frame.swapaxes(0, 1)
        frame = pygame.surfarray.make_surface(frame)
        count = 1

        while True:
            running = 0
            event = pygame.event.poll()
            if event.type == pygame.KEYDOWN:
                break
        running = 1

        timeElapsed = 0
        clock = pygame.time.Clock()

        while running:
            event = pygame.event.poll()

            dt = clock.tick()
            timeElapsed += dt

            if True:  # only runs when a key has been pressed
                if event.type == pygame.QUIT:
                    running = 0
                    pygame.display.quit()
                    print("Session ended >> Closed window")
                    break
                if timeElapsed >= (7) * 1000:  # 10 seconds
                    running = 0
                    pygame.display.quit()
                    print("Session ended >> Timeout")
                    break
                elif event.type == pygame.MOUSEMOTION:
                    print("mouse at (%d, %d)" % (event.pos))

                    pos = event.pos
                    if count > 1:
                        self.fillLine(prevPos, pos)
                    prevPos = (pos[0], pos[1])
                    self.mouseMap[pos[1], pos[0]] = 255
                    # Computes time for performance reasons gauging. Comment out for real use.
                    self.computeTime = time.time()

                    blurImg = self.compute_blur(pos)

                    self.computeTime = time.time() - self.computeTime
                    self.totalTime += self.computeTime
                    self.avgComputeTime = (self.computeTime + self.totalTime) / count
                    # print(">> Avg Compute time: " + str(self.avgComputeTime))
                    count = count + 1
                    frame = blurImg
                    frame = frame.swapaxes(0, 1)
                    frame = pygame.surfarray.make_surface(frame)
                    if event.pos == (300, 200):
                        screen = pygame.display.set_mode(scale)

            screen.blit(frame, (0, 0))

            # screen.fill((0, 0, 0))
            pygame.display.flip()

    def __init__(self, img, mask):
        pygame.init()  # Activates pygame
        self.bg = img
        self.mask = mask
        self.blurBg = cv2.GaussianBlur(img, (31, 31), 10)
        self.avgComputeTime = 0
        self.computeTime = 0
        self.totalTime = 0
        self.mouseMap = np.zeros((img.shape[0], img.shape[1], 1), np.uint8)


if __name__ == "__main__":
    ptcp = input("Input Participant ID (###): ")

    f = open("TestSet/nameList", "r")
    fileString = f.read()
    nameList = fileString.splitlines()
    f.close()

    random.shuffle(nameList)  # Randomizes file list
    mask = cv2.imread("PeripheralMask_small.jpg", 0)
    for imgName in nameList:
        imgName.replace(" ", '')
        filename = "TestSet/" + imgName + ".jpg"
        print(filename)
        bg = cv2.imread(filename, 0)
        # bg = cv2.resize(bg, (int(bg.shape[1]), int(bg.shape[0])))
        game = saliency_analog(bg, mask)
        print("Running mcsv on: " + imgName + " - Participant ID = " + str(ptcp))
        game.start()
        saveName = "TestResults/" + imgName + "_mmap_ptcp_" + str(ptcp) + ".jpg"
        cv2.imwrite(saveName, game.mouseMap)
        print("Saved result: " + saveName)

    print("All done! Thanks for helping out :)")

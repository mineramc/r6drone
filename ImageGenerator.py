from PIL import Image
import glob
import os
import random

import numpy as py

currentPath = os.getcwd()
bottleFolder = currentPath + '\\Bottle'
backgroundFolder = currentPath + '\\Classifier\\n'
outputFolder = currentPath + '\\Classifier\\p\\'
bottlePics = glob.glob(bottleFolder + '\\*')
backgroundPics = glob.glob(backgroundFolder + '\\*')
imageCounter = 0

"""for image in backgroundPics:
    background = Image.open(image)
    bottleCounter = 0
    for bottle in bottlePics:
        bottleImg = Image.open(bottle).convert("RGBA")
        size = (1400, 1400)
        background = background.resize(size, Image.ANTIALIAS)
        newSize = tuple(i // 4 for i in bottleImg.size)
        bottleImg = bottleImg.resize(newSize, Image.ANTIALIAS)
        randNum = random.randint(0, 3)
        if randNum == 0:
            background.paste(bottleImg, (700, 700), bottleImg)
        elif randNum == 1:
            background.paste(bottleImg, (100, 150), bottleImg)
        elif randNum == 2:
            bottleImg = bottleImg.rotate(random.randint(0, 360), expand=1)
            background.paste(bottleImg, (400, 400), bottleImg)
        else:
            bottleImg = bottleImg.rotate(random.randint(0, 360), expand=1)
            background.paste(bottleImg, (800, 300), bottleImg)

        background.save(outputFolder + str(imageCounter) + str(bottleCounter) + ".png", "PNG")
        background = Image.open(image)
        bottleCounter += 1
    imageCounter += 1
"""
counter = 0
for bottle in bottlePics:
    for i in range(100):
        bottleImg = Image.open(bottle)
        bottleImg = bottleImg.rotate(random.randint(0, 360), expand=1)
        bottleImg.save(outputFolder + str(counter) + ".png", "PNG")
        counter += 1

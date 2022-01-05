import numpy as np
from PIL import Image, ImageOps
from skimage import color
from skimage import io
from skimage.exposure import histogram
from matplotlib import pyplot as plt
import cv2
import math
from matplotlib.pyplot import bar
from skimage.transform import rescale, resize, downscale_local_mean
from os import listdir
from os.path import isfile, join
import pickle
import os

kernal_width = 3
grid_x = 8
grid_y = 8

megaHistogram = pickle.load(
    open(f"{os.getcwd()}/face_detection/megaHistogram.pkl", 'rb'))

# megaHistogram = pickle.load(open("megaHistogram.pkl", 'rb'))


def ecludianDistance(hists1, hists2):
    dist2 = 0
    for i in range(0, len(hists1)):
        dist2 += cv2.norm(hists1[i][0], hists2[i][0], normType=cv2.NORM_L2)
    #print('euclidean distance2:', dist2)
    return dist2


def formTiles(image):
    tiles = [image[x:x+25, y:y+25]
             for x in range(0, image.shape[0], 25) for y in range(0, image.shape[1], 25)]
    return tiles


def LBPImage(my_image):
    processed_image = np.zeros((my_image.shape[0], my_image.shape[1]))
    for i in range(0, my_image.shape[0]-2):
        for j in range(0, my_image.shape[1]-2):
            binary_str = ''
            for x in range(0, kernal_width):
                for y in range(0, kernal_width):
                    if i+x == i+1 and j+y == j+1:
                        continue
                    if my_image[i+x, j+y] >= my_image[i+1, j+1]:
                        binary_str += '1'
                    else:
                        binary_str += '0'
            processed_image[i+1, j+1] = int(binary_str, 2) / 255

    return processed_image


def calcHistograms2(tiles):
    hists = []
    for i in range(0, 64):
        hists.append(histogram(tiles[i]))
    return hists


def compareFaces(image):
    image = cv2.resize(image, (200, 200))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    processed_image = LBPImage(image)

    tiles = formTiles(processed_image)
    hists = calcHistograms2(tiles)
    distFromEachFace = []
    for i in range(0, len(megaHistogram)):
        dist = 0
        for j in range(0, len(megaHistogram[i][0])):
            dist += ecludianDistance(hists, megaHistogram[i][0][j])
        dist = dist // 8
        distFromEachFace.append([dist, megaHistogram[i][1]])
        # print(dist)
    return min(distFromEachFace)

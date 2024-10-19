# This software is designed to join masks together at points where the resolution is too small to handle them

import os
from PIL import Image

def mask_pixel_joiner():
    print("Starting Mask Pixel Joiner")

    read_images_from_directory("C:\\Users\\Richard\\Documents\\Unreal Projects\\Bibimbap54\\Saved\\Screenshots\\Marker Buoys\\Cardinal Marks\\East")

def read_images_from_directory(directory):

    for file in os.listdir(directory):
        if (file.endswith(".png")):
            print(directory+file)
            print(file)
            read_pixel_values_of_image(directory+"\\"+file)


def read_pixel_values_of_image(image):

    openedImage = Image.open(image)
    imagePixels = openedImage.load()

    for x in range(512):
        for y in range(512):
            if imagePixels[x,y][0] == 255:
                print("RED PIXEL FOUND")
                print("CHANGING TO GREEN")
                imagePixels[x,y] = (0, 255, 0, 255)

    openedImage.save("C:\\Users\\Richard\\Documents\\Unreal Projects\\Bibimbap54\\Saved\\Screenshots\\Marker Buoys\\Cardinal Marks\\East\\changed.png")

mask_pixel_joiner()
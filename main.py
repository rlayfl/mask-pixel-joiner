# This software is designed to join masks together at points where the resolution is too small to handle them

import os
from PIL import Image

def mask_pixel_joiner():
    print("Starting Mask Pixel Joiner")

    read_images_from_directory("C:\\Users\\Richard\\Documents\\Unreal Projects\\Bibimbap54\\Saved\\Screenshots\\Marker Buoys\\Lateral Marks\\Port\\Channel\\A")

def read_images_from_directory(directory):

    for file in os.listdir(directory):
        if (file.endswith(".png")):
            print(directory+file)
            print(file)
            read_pixel_values_of_image(directory, file)


def read_pixel_values_of_image(directory, file):

    openedImage = Image.open(directory+"\\"+file)
    imagePixels = openedImage.load()

    # For every row
    for x in range(512):
        # For every column
        for y in range(512):

            # If the pixel is pure red (might need changing to ensure other values with 255 R value aren't included)
            if imagePixels[x,y][0] == 255:
                print("RED PIXEL FOUND")

                # Check the values around it but one pixel away like this:

                #       # # # # #
                #       #       #
                #       #   #   #
                #       #       #
                #       # # # # #


                # Check the 16 pixels around it 1 layer away to see if they are also red
                # Going clockwise, the pixels are:

                # Row 0 would be checked like:

                # - (x-2, y-2)
                # - (x-1, y-2)
                # - (x, y-2)
                # - (x+1, y-2)
                # - (x+2, y-2)

                #Extend this to check the subsequent rows
                
                if (imagePixels[x-2, y-2][0] == 255) and (imagePixels[x-1, y-1][0] != 255):
                    print("Filling in gap with green")
                    imagePixels[x-1, y-1] = (0, 255, 0, 255)

                for i in range (10):
                    # Vertical gap
                    if (imagePixels[x, y-i][0] == 255) and (imagePixels[x, y-i-1][0] != 255):
                        print("Filling in gap with green")
                        imagePixels[x, y-4] = (0, 255, 0, 255)
                        imagePixels[x, y-3] = (0, 255, 0, 255)
                        imagePixels[x, y-2] = (0, 255, 0, 255)
                        imagePixels[x, y-1] = (0, 255, 0, 255)

                

                

    openedImage.save(directory+"\\changed_"+file)

mask_pixel_joiner()
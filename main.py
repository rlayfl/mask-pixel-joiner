# This software is designed to join masks together at points where the resolution is too small to handle them

import os
from PIL import Image

directories = {
    "BP_CM_East": r"C:\Users\Richard\Documents\Unreal Projects\Bibimbap54\Saved\Screenshots\Marker Buoys\Cardinal Marks\East",
    "BP_CM_North": r"C:\Users\Richard\Documents\Unreal Projects\Bibimbap54\Saved\Screenshots\Marker Buoys\Cardinal Marks\North",
    "BP_CM_South": r"C:\Users\Richard\Documents\Unreal Projects\Bibimbap54\Saved\Screenshots\Marker Buoys\Cardinal Marks\South",
    "BP_CM_West": r"C:\Users\Richard\Documents\Unreal Projects\Bibimbap54\Saved\Screenshots\Marker Buoys\Cardinal Marks\West",
    "BM_IDM_Type_2": r"C:\Users\Richard\Documents\Unreal Projects\Bibimbap54\Saved\Screenshots\Marker Buoys\Isolated Danger Marks\Type 2 Solar Buoy",
    "BP_LM_P_C_A": r"C:\Users\Richard\Documents\Unreal Projects\Bibimbap54\Saved\Screenshots\Marker Buoys\Lateral Marks\Port\Channel\A",
    "BP_LM_P_H_A": r"C:\Users\Richard\Documents\Unreal Projects\Bibimbap54\Saved\Screenshots\Marker Buoys\Lateral Marks\Port\Hand\A",
    "BP_LM_S_C_A": r"C:\Users\Richard\Documents\Unreal Projects\Bibimbap54\Saved\Screenshots\Marker Buoys\Lateral Marks\Starboard\Channel\A",
    "BP_LM_S_H_A": r"C:\Users\Richard\Documents\Unreal Projects\Bibimbap54\Saved\Screenshots\Marker Buoys\Lateral Marks\Starboard\Hand\A",
    "BP_SWM_Type_2": r"C:\Users\Richard\Documents\Unreal Projects\Bibimbap54\Saved\Screenshots\Marker Buoys\Safe Water Marks\Type 2 Solar Buoy",
    "BP_SM_Class_2": r"C:\Users\Richard\Documents\Unreal Projects\Bibimbap54\Saved\Screenshots\Marker Buoys\Special Marks\Class Two Solar Buoy"
}

def mask_pixel_joiner():

    print("Starting Mask Pixel Joiner")

    for buoy, directory in directories.items():

        images_directory = directory + r"\images"
        masked_images_directory = directory + r"\masked"

         # Get sorted lists of files in both directories
        image_files = sorted(os.listdir(images_directory))
        masked_image_files = sorted(os.listdir(masked_images_directory))

        # Check if both directories have the same number of images
        if len(image_files) != len(masked_image_files):
            print("The number of images in the directories do not match.")
        else:
            # Iterate over both lists of files
            for image_file, masked_image_file in zip(image_files, masked_image_files):
                # Full paths to the current image and the new filename
                image_path = os.path.join(images_directory, image_file)
                new_image_path = os.path.join(images_directory, masked_image_file)

                # Rename the file
                os.rename(image_path, new_image_path)
                print(f"Renamed '{image_file}' to '{masked_image_file}'")

            print("All images have been renamed.")

        read_images_from_directory(buoy, masked_images_directory, directory)

def read_images_from_directory(buoy, masked_images_directory, directory):

    for file in os.listdir(masked_images_directory):
        if (file.endswith(".png")):
            print(masked_images_directory+file)
            print(file)
            get_pixels_rows_with_red_pixels(directory, file, buoy)       

def read_pixel_values_of_image(directory, file):

    openedImage = Image.open(directory+"\\"+file)
    imagePixels = openedImage.load()

    # For every row
    for x in range(512):
        # For every column
        for y in range(512):

            # If the pixel is pure red (might need changing to ensure other values with 255 R value aren't included)
            if imagePixels[x,y][0] == 255:

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
                    imagePixels[x-1, y-1] = (255, 0, 0, 255)

                for i in range (50):
                    # Vertical gap
                    if (imagePixels[x, y-i][0] == 255) and (imagePixels[x, y-i-1][0] != 255):
                        imagePixels[x, y-4] = (255, 0, 0, 255)
                        imagePixels[x, y-3] = (255, 0, 0, 255)
                        imagePixels[x, y-2] = (255, 0, 0, 255)
                        imagePixels[x, y-1] = (255, 0, 0, 255)
    
    openedImage.save(directory+"\\filled_"+file)

    get_coordinates_of_bounding_box(directory, "filled_"+file)

def get_pixels_rows_with_red_pixels(directory, file, buoy):

    opened_image = Image.open(directory+"\\masked\\"+file)
    image_pixels = opened_image.load()

    rows_with_red_pixel = []

    # For checking image from left to right
    # For every column
    for y in range(0, 512, 2):

        # For every row
        for x in range(512):

            if image_pixels[x,y][0] == 255:

                print("ROW CONTAINS RED PIXEL")
                rows_with_red_pixel.append([x,y])
                image_pixels[x,y] = (0, 255, 0, 255)
                break

    # For checking image from right to left
    # For every column
    for y in range(511, -1, -2):

        # For every row (bottom to top, reverse order)
        for x in range(511, -1, -1):

            if image_pixels[x, y][0] == 255: 
                print("ROW CONTAINS RED PIXEL FROM RIGHT TO LEFT")
                rows_with_red_pixel.append([x,y])
                image_pixels[x, y] = (0, 0, 255, 255) 
                break

    print(rows_with_red_pixel)
    print("Height of image mask is:")
    print(len(rows_with_red_pixel))

    print("First row is: ")
    print(rows_with_red_pixel[0])

    print("Last row is: ")
    print(rows_with_red_pixel[-1])

    # Uncomment to view the image
    #opened_image.save(directory+"\\masked_"+file)

    #Remove .png from file name
    file = file.replace('.png', '')

    f = open(directory+"\\labels\\"+file+".txt", "w")

    buoy_class = -1

    match buoy:
        case "BP_CM_East":
            buoy_class = 0
        case "BP_CM_North":
            buoy_class = 1
        case "BP_CM_South":
            buoy_class = 2
        case "BP_CM_West":
            buoy_class = 3
        case "BM_IDM_Type_2":
            buoy_class = 4
        case "BP_LM_P_C_A":
            buoy_class = 5
        case "BP_LM_P_H_A":
            buoy_class = 6
        case "BP_LM_S_C_A":
            buoy_class = 7
        case "BP_LM_S_H_A":
            buoy_class = 8
        case "BP_SWM_Type_2":
            buoy_class = 9
        case "BP_SM_Class_2":
            buoy_class = 10

    # Class of buoy
    f.write(str(buoy_class))

    # Normalisation
    for coordinate in rows_with_red_pixel:    

        normalised_x = coordinate[0] / 512
        rounded_normalised_x = round(normalised_x, 5)

        normalised_y = coordinate[1] / 512
        rounded_normalised_y = round(normalised_y, 5)

        f.write(str(rounded_normalised_x) + " ")
        f.write(str(rounded_normalised_y) + " ")

    f.close()
                
def get_coordinates_of_bounding_box(directory, file):

    openedImage = Image.open(directory+"\\"+file)
    imagePixels = openedImage.load()

    # For every column
    for y in range(512):

        # For every row
        for x in range(512):

            if y < 511:

                # Top
                # If the pixel is red and the pixel below is red and the pixel above is not red or green or blue

                if imagePixels[x,y][0] == 255 and imagePixels[x,y-1][0] != 255 and imagePixels[x,y-1][1] != 255 and imagePixels[x,y-1][2] != 255:

                    imagePixels[x,y] = (0, 0, 255, 255)

                # Left
                # If the pixel is red and the pixel to the right is red and the pixel to the left is not red or green or blue

                if imagePixels[x,y][0] == 255 and imagePixels[x+1,y][0] == 255 and imagePixels[x-1,y][0] != 255 and imagePixels[x-1,y][1] != 255 and imagePixels[x-1,y][2] != 255:
                    imagePixels[x,y] = (0, 0, 255, 255)

                # Right
                # If the pixel is red and the pixel to the left is red and the pixel to the right is not red or green or blue
                if imagePixels[x,y][0] == 255 and imagePixels[x-1,y][0] == 255 and imagePixels[x+1,y][0] != 255 and imagePixels[x+1,y][1] != 255 and imagePixels[x+1,y][2] != 255:
                    imagePixels[x,y] = (0, 0, 255, 255)

                # Bottom
                # If the pixel is red and the pixel above is red and the pixel below is not red or green or blue
                if imagePixels[x,y][0] == 255 and imagePixels[x,y+1][0] != 255 and imagePixels[x,y+1][1] != 255 and imagePixels[x,y+1][2] != 255:
                    imagePixels[x,y] = (0, 0, 255, 255)

                # Single pixel width parts
                # If the pixel is red and the pixel above is red and the pixel below is red and the pixel to the left and right are not green or blue
                if imagePixels[x,y][0] == 255 and imagePixels[x,y+1][0] == 255 and imagePixels[x,y-1][0] == 255 and imagePixels[x-1,y][0] != 255 and imagePixels[x-1,y][1] != 255 and imagePixels[x-1,y][2] != 255 and imagePixels[x+1,y][0] != 255 and imagePixels[x+1,y][1] != 255 and imagePixels[x+1,y][2] != 255:
                    imagePixels[x+1,y] = (0, 0, 255, 255)
                    imagePixels[x-1,y] = (0, 0, 255, 255)

    openedImage.save(directory+"\\masked_"+file)

mask_pixel_joiner()
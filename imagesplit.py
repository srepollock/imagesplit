#!/usr/bin/env python
import argparse
import progressbar
import shlex
import subprocess
import time
import os

def image_size(original_image):
    '''
    Gets the image width and height.

    Returns a tuple of int's (width, height)
    '''
    args = 'identify {}'.format(original_image)
    # if (not DEBUG):
    #     print('ImageMagic identify arguments to run:\n{}'.format(args))
    #     return 1024, 1024 # Putting defaults here because eh
    process = subprocess.Popen(shlex.split(args), stdout=subprocess.PIPE)
    data, err = process.communicate()
    if (err):
        sys.exit("There was an error getting the image information.")
    width_height = data.split(" ")[2]
    image_width = int(width_height.split("x")[0])
    image_height = int(width_height.split("x")[1])
    return image_width, image_height

def run_magik(original_image, cell_width, cell_height):
    '''
    Runs the convert command of ImageMagik.
    Creates a new images and denotes them with the offset of the original. 
    It will print out a progress bar for the user to see.
    All are placed into the same folder as the original.

    Returns nothing.
    '''
    path = os.path.dirname(os.path.realpath(original_image))
    image_width, image_height = image_size(original_image)
    width_range = int(round(image_width / cell_width))
    height_range = int(round(image_height / cell_height))
    progress = 0
    print ('Begin Image Splitting:\n')
    with progressbar.ProgressBar(max_value=(width_range * height_range)) as bar:
        for i in range(0, width_range):
            offset_width = i * cell_width
            for j in range(0, height_range):
                offset_height = j * cell_height
                new_image = original_image.split(".png")[0] + "_{offset_width}_{offset_height}.png".format(offset_width=offset_width, offset_height=offset_height)
                args = 'convert -extract {width}x{height}+{offset_width}+{offset_height} {original_image} {new_image}'.format(original_image=original_image, new_image=new_image, width=cell_width, height=cell_height, offset_width=offset_width, offset_height=offset_height)
                process = subprocess.Popen(shlex.split(args), stdout=subprocess.PIPE)
                process.communicate()
                progress += 1
                bar.update(progress)
    return

def get_args():
    '''
    Gets the arguments from the user.

    Returns the arguments from the user.
    '''
    parser = argparse.ArgumentParser(description='Split an image into a grid format based on the image size or specified. If no width & height is specified, then the width and height of the cell is defaulted to 1024x1024. Cell images are saved to the same directory as the original image.', epilog='Created by Spencer Pollock. Note: ImageMagik must be installed on the system to use.')
    parser.add_argument('image', type=str, action='store', help='Image to convert and split.')
    parser.add_argument('--width', type=int, dest='width', action='store', default=1024, help='Width of the cell to split the image by.')
    parser.add_argument('--height', type=int, dest='height', action='store', default=1024, help='Height of the cell to split the image by.')
    # parser.add_argument('--debug', dest='debug', action='store_true', help='Runs debug statements and checks without processing.') # NOTE: to be implemented later
    return parser.parse_args()

def main(args):
    '''
    Main function for running.
    '''
    if (args.debug):
        DEBUG = args.debug
    run_magik(args.image, args.width, args.height)
    return

if __name__ == "__main__":
    args = get_args()
    main(args)
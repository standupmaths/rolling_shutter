from PIL import Image
import argparse
import glob
import os


def rolling_shutter(input_directory, output_directory, extension_type, image_height, image_width, speed):
    
    # Making our blank output frame
    output_image = Image.new('RGB', (image_width, image_height)) 
    
    
    # let us go through the frames one at a time
    
    current_row = 0
     
    for filename in glob.glob(os.path.join(input_directory, "*." + extension_type)):
        frame = Image.open(filename)
        new_line = frame.crop((0, current_row, image_width, current_row + speed))
        output_image.paste(new_line, (0,current_row))
        current_row += speed
    
    # and export the final frame
    if not os.path.exists(output_directory):
            os.makedirs(output_directory)
    output_image.save(os.path.join(output_directory, 'output_image.png'))
    
    return 'DONE'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_directory', required=True, help='Path to directory containing input images.')
    parser.add_argument('-o', '--output-directory', required=True, help='Path to directory to write output image(s) to.')
    parser.add_argument('-s', '--speed', default=1, type=int, help='Speed variable to control how many rows to jump by per frame.')
    parser.add_argument('-x', '--extension-type', default='png', help='Extension type in input/output filename (defaults to png).')
    parser.add_argument('--image-height', default=1080, type=int, help='Height of image in pixels.')
    parser.add_argument('--image-width', default=1920, type=int, help='Width of image in pixels.')
    args = parser.parse_args()
    rolling_shutter(
            args.input_directory,
            args.output_directory,
            extension_type=args.extension_type,
            image_height=args.image_height,
            image_width=args.image_width,
            speed=args.speed)

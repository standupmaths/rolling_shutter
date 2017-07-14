import glob
import os.path

from PIL import Image


def rolling_shutter(folder, speed=1):
    # ENTER YOUR DIRECTORIES AND FILE TYPE HERE
    frame_dir = os.path.join("/Users/mattparker/Documents/rollingshuttervideos/", str(folder))
    frame_file = "png"
    output_dir = "/Users/mattparker/Documents/rollingshuttervideos/"

    width = 1920
    height = 1080

    # Making our blank output frame
    output_image = Image.new('RGB', (width, height))

    # let us go through the frames one at a time

    current_row = 0

    for filename in glob.glob(frame_dir + "*." + frame_file):
        frame = Image.open(filename)
        new_line = frame.crop((0, current_row, width, current_row + speed))
        output_image.paste(new_line, (0, current_row))
        current_row += speed

    # and export the final frame
    output_image.save(os.path.join(output_dir, "output_image.png"))

    return "DONE"

if __name__ == "__main__":
    rolling_shutter("rollingshutter")

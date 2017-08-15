from PIL import Image
import argparse
import glob
import sys

parser = argparse.ArgumentParser(description = 'Fake a rolling shutter effect')
parser.add_argument('folder', help = 'Folder containing image files (named sequentially)')
parser.add_argument('-o', '--output', help = 'Desired output filename (default: out.png)', default = 'out.png')
parser.add_argument('-t', '--type', help = 'Filetype to look for in folder (default: png)', default = 'png')

args = parser.parse_args()

# ENTER YOUR DIRECTORIES AND FILE TYPE HERE
frames = [Image.open(img) for img in glob.glob(args.folder + '/*.' + args.type)]

# Extract size from first frame
width, height = frames[0].size

# Making our blank output frame
output_image = Image.new('RGB', (width, height))

# let us go through the frames one at a time

total_frames = len(frames)
speed = height/total_frames
current_row = 0

for i, frame in enumerate(frames):
    new_line = frame.crop((0, int(current_row), width, int(current_row + speed)))
    output_image.paste(new_line, (0, int(current_row)))
    current_row += speed
    i += 1
    sys.stdout.write('\r{:3d}% [{:73}]'.format(int(i/total_frames*100), '#'*int(i/total_frames*73)))
    sys.stdout.flush()

print()

# and export the final frame
output_image.save(args.output)
print("Saved output to '{}'".format(args.output))

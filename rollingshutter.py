#!/usr/bin/env python3

from PIL import Image
from pathlib import Path


def rs(frame_folder, output_folder, filetype, size, speed=1,):

    frame_dir = Path(frame_folder)
    output_path = Path(output_folder)

    # Making our blank output frame
    output_image = Image.new('RGBA', size)

    # let us go through the frames one at a time
    current_row = 0
    
    for filename in sorted(f for f in frame_dir.iterdir() if f.suffix.endswith(filetype)):
        frame = Image.open(str(filename))
        new_line = frame.crop((0, current_row, size[0], current_row+speed))
        output_image.paste(new_line, (0, current_row))
        current_row += speed

    # and export the final frame
    output_image.save(str(output_path / 'output_image.png'), filetype)

    return 'DONE'

if __name__ == '__main__':
    rs(frame_folder='frames', output_folder='.', filetype='png', size=(1920, 1080), speed=1)

def rolling_shutter(absoluteFolder, speed, outputFolder):
    from PIL import Image
    import glob

    # ENTER YOUR DIRECTORIES AND FILE TYPE HERE
    frame_dir = absoluteFolder
    frame_file = "png"
    output_dir = outputFolder

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
    output_image.save(output_dir + 'output_image.png')

    return 'DONE'

shutter_folder = raw_input("Enter the name of the folder containing pictures to rolling shutter-ify: ")
speed_input = raw_input("Enter the speed (return for default 1): ")
speed = 1 if speed_input == '' else int(speed_input)
folder_input = raw_input("Enter the output directory (return for default): ")
output_folder = "/Users/mattparker/Documents/rollingshuttervideos/" if folder_input == '' else folder_input

rolling_shutter(shutter_folder, speed, output_folder)

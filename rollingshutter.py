def rs(folder, speed=1):
    from PIL import Image
    import glob
    import os

    # start at the user's Document folder, like: /Users/mattparker/Documents
    docs_dir = os.path.join(os.path.expanduser('~'), 'Documents')
    # ENTER YOUR FILE EXTENSION and DIRECTORIES HERE
    file_extension = ".png"  # We will only look for .png files
    # read files from:  /Users/mattparker/Documents/rollingshuttervideos/folder
    input_dir = os.path.join(docs_dir, 'rollingshuttervideos', folder)
    # write our results to:  /Users/mattparker/Documents/rollingshuttervideos
    output_dir = os.path.join(docs_dir, 'rollingshuttervideos')

    width = 1920
    height = 1080

    # Making our blank output frame
    output_image = Image.new('RGB', (width, height))

    # let us go through the frames one at a time
    for i, filename in enumerate(glob.glob(input_dir + "/*" + file_extension)):
        current_row = i * speed
        frame = Image.open(filename)
        new_line = frame.crop((0, current_row, width, current_row + speed))
        output_image.paste(new_line, (0, current_row))
    # and export the final frame
    output_image.save(os.path.join(output_dir, 'output_image.png'))

    return 'DONE'

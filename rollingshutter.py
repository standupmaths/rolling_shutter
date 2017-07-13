from sys import argv

print(__file__)
path = __file__.split("/")[:-1]
path_real = ""
for layer in path:
    path_real += layer + "/"
print(path_real)


options = {"path": "images", "speed": 1, "frame_file": "png", "width": 1920, "height": 1080}
a = argv

for x, i in enumerate(argv):
    if i == "-p":
        try:
            options["path"] = argv[x+1]
        except IndexError:
            print("Error: -p option requires string folder path.")
            exit(1)
    elif i == "-s":
        try:
            options["speed"] = int(argv[x+1])
        except (IndexError, ValueError):
            print("Error: -s option requires integer speed.")
            exit(2)
    elif i == "-f":
        try:
            options["frame_file"] = argv[x+1]
        except IndexError:
            print("Error: -f option requires string frame extension")
            exit(3)
    elif i == "-w":
        try:
            options["width"] = int(argv[x+1])
        except (IndexError, ValueError):
            print("Error: -w option requires integer width.")
            exit(4)
    elif i == "-h":
        try:
            options["height"] = int(argv[x+1])
        except (IndexError, ValueError):
            print("Error: -h option requires integer height.")
            exit(5)
if options == {"path": "images", "speed": 1, "frame_file": "png", "width": 1920, "height": 1080}:
    try:
        options["path"] = argv[1]
        options["speed"] = int(argv[2])
        options["frame_file"] = argv[3]
        options["width"] = int(argv[4])
        options["height"] = int(argv[5])
    except IndexError:
        pass
    except ValueError:
        print("Argument #2, #4 and #5 must be an integer.")
        exit(6)

computed = {"frame_dir": path_real + str(options["path"]) + "/",
            "output_dir": path_real}

print("Local path:      "+options["path"])
print("Global path:     "+computed["frame_dir"])
print("Speed:           "+str(options["speed"]))
print("Frame extension: "+options["frame_file"])
print("Dimensions:      "+str(options["width"])+"x"+str(options["height"]))
print("\n")


def rs(opts, comps):

    from PIL import Image
    import glob

    frame_dir = comps["frame_dir"]
    frame_file = opts["frame_file"]
    output_dir = comps["output_dir"]

    width = opts["width"]
    height = opts["height"]

    # Making our blank output frame
    output_image = Image.new('RGB', (width, height))

    # let us go through the frames one at a time

    current_row = 0

    files = glob.glob(frame_dir + "*." + frame_file)
    for y, filename in enumerate(files):
        percentage = str(y/len(files))
        print("Progress: "+percentage+"%", end="\r")
        frame = Image.open(filename)
        new_line = frame.crop((0, current_row, width, current_row + opts["speed"]))
        output_image.paste(new_line, (0, current_row))
        current_row += opts["speed"]
    print("")

    # and export the final frame
    output_image.save(output_dir + 'output_image.png')

rs(options, computed)

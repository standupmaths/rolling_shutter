from argparse import ArgumentParser

path = __file__.split("/")[:-1]
path_real = ""
for layer in path:
    path_real += layer + "/"

parser = ArgumentParser()
parser.add_argument("path", nargs="?", default="images", help="path folder of images", type=str)
parser.add_argument("speed", nargs="?", default=1, help="speed of rolling shutter", type=int)
parser.add_argument("extension", nargs="?", default="png", help="extension of files", type=str)
parser.add_argument("width", nargs="?", default=1920, help="width of files", type=int)
parser.add_argument("height", nargs="?", default=1080, help="height of files", type=int)

options = vars(parser.parse_args())
computed = {"frame_dir": path_real + str(options["path"]) + "/",
            "output_dir": path_real}

print("Local path:      "+options["path"])
print("Global path:     "+computed["frame_dir"])
print("Speed:           "+str(options["speed"]))
print("Frame extension: "+options["extension"])
print("Dimensions:      "+str(options["width"])+"x"+str(options["height"]))
print("\n")


def rs(opts, comps):

    from PIL import Image
    import glob

    output_image = Image.new('RGB', (options["width"], options["height"]))
    current_row = 0

    files = glob.glob(comps["frame_dir"] + "*." + options["extension"])
    for y, filename in enumerate(files):
        percentage = str(y/len(files))
        print("Progress: "+percentage+"%", end="\r")
        frame = Image.open(filename)
        new_line = frame.crop((0, current_row, options["width"], current_row + opts["speed"]))
        output_image.paste(new_line, (0, current_row))
        current_row += opts["speed"]
    print("")

    # and export the final frame
    output_image.save(comps["output_dir"] + 'output_image.png')

rs(options, computed)

from tkinter import Tk, Grid, Frame, Label, Entry, Spinbox, Button, N, S, E, W


# region Define simulator
def button_pressed():
    options = {"path": path_input.get(),
               "speed": int(speed_input.get()),
               "extension": extension_input.get(),
               "width": int(width_input.get()),
               "height": int(height_input.get())}

    computed = {"frame_dir": path_real + str(options["path"]) + "/",
                "output_dir": path_real}

    print(options)
    print(computed)

    from PIL import Image
    import glob

    output_image = Image.new('RGB', (options["width"], options["height"]))
    current_row = 0

    files = glob.glob(computed["frame_dir"] + "*." + options["extension"])

    for y, filename in enumerate(files):
        percentage = str(int(((y+1)/len(files))*100)) + "%"
        progress_bar.config(text=percentage)
        print("Progress: "+percentage, end="\r")

        frame = Image.open(filename)
        new_line = frame.crop((0, current_row, options["width"], current_row + options["speed"]))
        output_image.paste(new_line, (0, current_row))
        current_row += options["speed"]
    print("")
    output_image.save(computed["output_dir"] + 'output_image.png')
# endregion

# region Get path of running file
path = __file__.split("/")[:-1]
path_real = ""
for layer in path:
    path_real += layer + "/"
# endregion

# region Create components
root = Tk()
root.resizable(False, False)

root.title("Rolling Shutter Simulator")
Grid.rowconfigure(root, 0, weight=1)

Grid.columnconfigure(root, 0, weight=1)
container = Frame(root)

container.grid(row=0, column=0, sticky=N + S + E + W)
path_label = Label(container, text="Input")
speed_label = Label(container, text="Speed")
extension_label = Label(container, text="Ext.")
width_label = Label(container, text="Width")

height_label = Label(container, text="Height")
path_input = Entry(container)
speed_input = Spinbox(container, from_=1, to=1000000000000000000)
extension_input = Entry(container)
width_input = Spinbox(container, from_=1, to=1000000000000000000)

height_input = Spinbox(container, from_=1, to=1000000000000000000)
path_input.insert(0, "images")
extension_input.insert(0, "png")
width_input.insert(1, 920)

height_input.insert(1, "080")
progress_bar = Label(root)

progress_bar.config(text="0%")
perform_simulation = Button(root, text="Perform Simulation", command=button_pressed)
# endregion

# region Place components
path_label.grid(row=0, column=0)

path_input.grid(row=0, column=1)
speed_label.grid(row=1, column=0)

speed_input.grid(row=1, column=1)

extension_label.grid(row=2, column=0)

extension_input.grid(row=2, column=1)
width_label.grid(row=3, column=0)

width_input.grid(row=3, column=1)
height_label.grid(row=4, column=0)

height_input.grid(row=4, column=1)

progress_bar.grid(row=5, column=0)
perform_simulation.grid(row=6, column=0, sticky=E+W)
# endregion

root.mainloop()

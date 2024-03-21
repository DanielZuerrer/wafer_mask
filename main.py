import json
import os
from tkinter import *
from tkinter import ttk, filedialog
from PIL import Image, ImageTk, ImageDraw
from wafer_entry import WaferEntry


root = Tk()
width, height = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry('%dx%d+0+0' % (width,height))

wafer_path = filedialog.askopenfilename()
wafer_dirname = os.path.dirname(wafer_path)
wafer_filename = os.path.basename(wafer_path)
mask_path = os.path.join(wafer_dirname, f'mask_{wafer_filename}.json')

wafer = Image.open(wafer_path)
wafer_resized = wafer.resize((width, int(height/2)))
scale_factor_width = wafer_resized.width / wafer.width
scale_factor_height = wafer_resized.height / wafer.height
wafer_image = ImageTk.PhotoImage(wafer_resized)

canvas = Canvas(root, width=wafer_resized.width, height=wafer_resized.height)
canvas.create_image(0, 0, image=wafer_image, anchor=NW)
canvas.grid(column=0, row=0, columnspan=10)

def draw_grid(grid):
    canvas.delete("grid")
    for x in range(grid["count_x"]):
        for y in range(grid["count_y"]):
            x0 = grid["start_x"] + x * grid["gap_x"] + x * grid["width"]
            y0 = grid["start_y"] + y * grid["gap_y"] + y * grid["height"]
            x1 = x0 + grid["width"]
            y1 = y0 + grid["height"]
            canvas.create_rectangle(x0, y0, x1,y1, tags="grid", outline="red", width=2)

grid = {
    "count_x": 4,
    "count_y": 2,
    "width": 40,
    "height": 20,
    "start_x": 50,
    "start_y": 50,
    "gap_x": 10,
    "gap_y": 10
}

if (os.path.exists(mask_path)):
    with open(mask_path, 'r') as f:
        grid = json.load(f)

draw_grid(grid)

def grid_change(variable, value):
    grid[variable] = value
    draw_grid(grid)

WaferEntry(root, "count_x", 0, 1, lambda count_x: grid_change("count_x", int(count_x)), grid["count_x"])
WaferEntry(root, "start_x", 1, 1, lambda start_x: grid_change("start_x", int(start_x)), grid["start_x"])
WaferEntry(root, "width", 2, 1, lambda width: grid_change("width", int(width)), grid["width"])
WaferEntry(root, "gap_x", 3, 1, lambda gap_x: grid_change("gap_x", int(gap_x)), grid["gap_x"])

WaferEntry(root, "count_y", 0, 3, lambda count_y: grid_change("count_y", int(count_y)), grid["count_y"])
WaferEntry(root, "start_y", 1, 3, lambda start_y: grid_change("start_y", int(start_y)), grid["start_y"])
WaferEntry(root, "height", 2, 3, lambda height: grid_change("height", int(height)), grid["height"])
WaferEntry(root, "gap_y", 3, 3, lambda gap_y: grid_change("gap_y", int(gap_y)), grid["gap_y"])

def save_mask():
    wafer_dirname = os.path.dirname(wafer_path)
    wafer_filename = os.path.basename(wafer_path)
    mask_path = os.path.join(wafer_dirname, f'mask_{wafer_filename}.json')

    with open(mask_path, 'w') as f:
        json.dump(grid, f)

    img = Image.new("RGBA", (wafer.width, wafer.height))
    img1 = ImageDraw.Draw(img)

    for x in range(grid["count_x"]):
        for y in range(grid["count_y"]):
            x0 = grid["start_x"] + x * grid["gap_x"] + x * grid["width"]
            y0 = grid["start_y"] + y * grid["gap_y"] + y * grid["height"]
            x1 = x0 + grid["width"]
            y1 = y0 + grid["height"]

            img1.rectangle([
                        int(x0 / scale_factor_width),
                        int(y0 / scale_factor_height),
                        int(x1 / scale_factor_width),
                        int(y1 / scale_factor_height)
                    ],
                    fill=(255, 255, 255, 255))

    img.save("mask.png")

     
ttk.Button(root, text="Save Mask", command=save_mask).grid(column=0, row=5)

root.mainloop()

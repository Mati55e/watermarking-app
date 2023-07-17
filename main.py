import os.path
from tkinter import Tk, Label, Button, Canvas
from add_watermark import WatermarkEngine
from tkinter import filedialog as fd
from tkinter import ttk


def get_img_path():

    global file_path
    file = fd.askopenfile(mode='r', filetypes=[('PNG Files', '*.png'), ('JPG Files', '.jpg')])
    file_path = file.name

    selected_file_label = Label(frm2, text="Your selected file: " + file_path)
    selected_file_label.pack(side="top", anchor="nw")

    global g_image
    g_image = WatermarkEngine(path=file_path)
    global canvas
    canvas = Canvas(frm2, width=g_image.w, height=g_image.h)
    canvas.pack(anchor="nw")
    display_img()


def save_img():
    save_path = fd.asksaveasfilename()
    g_image.save(path=save_path)


def display_img():
    canvas.create_image(10, 10, anchor="nw", image=g_image.tk_image)


def text_watermark():
    g_image.text_watermark()
    canvas.create_image(10, 10, anchor="nw", image=g_image.tk_image)


def img_watermark():
    select_watermark_img_button = Button(frm, text="Select watermark image")
    g_image.img_watermark()
    canvas.create_image(10, 10, anchor="nw", image=g_image.tk_image)


root = Tk()
root.title("Watermarking App")
root.geometry("900x600")

frm = ttk.Frame(root)
frm2 = ttk.Frame(root)
frm.pack(anchor="nw")
frm2.pack(anchor="nw")

label = Label(frm, text="Add a watermark to your image")
search_file_button = Button(frm, text="Select base image", command=get_img_path)
save_button = Button(frm, text="Save watermarked image", command=save_img)
text_watermark_button = Button(frm, text="Apply text watermark", command=text_watermark)
img_watermark_button = Button(frm, text="Apply watermark with an image", command=img_watermark)

label.pack(anchor="nw")
search_file_button.pack(side="left", anchor="nw")
text_watermark_button.pack(side="left", anchor="nw")
img_watermark_button.pack(side="left", anchor="nw")
save_button.pack(side="top", anchor="nw")

frm.mainloop()


from tkinter import*
import math
from PIL import Image, ImageTk
from tkinter import colorchooser
from tkinter import filedialog

root = Tk()
root.title("alpha particles scattering")
root.geometry("1200x750")
root.config(bg="black")


cw = 900
ch = 600
canvas = Canvas(root, width=cw, height=ch, bg="#262c3d")
canvas.grid(row=0, column=0, rowspan=3, columnspan=5)

# identify the parameter of coordinate system
rx, ry = 5, 5
ox , oy = -100, -60
goldnuclei_r = 35
startvar = StringVar()
startvar.set("start")

# create the xy_grid function
def create_the_xy_grids():
    # craete the x axis
    canvas.create_line(0, ch-(-oy*ry), cw, ch-(-oy*ry), fill="white", tag="grid_lines", width="1.5")
    # craete the y axis
    canvas.create_line(-ox*rx, 0, -ox*rx,  ch,  fill="white", tag="grid_lines", width="1.5")
    # create the x lines
    for i in range(0, int(cw/rx/10)):
        canvas.create_line(i*10*rx, 0, i*10*rx, ch, fill="#323744", tag="grid_lines", width="0.5")
    # craete the y lines
    for j in range(0, int(ch/ry/10)):
        canvas.create_line(0, j*10*rx, cw,  j*10*rx, fill="#323744", tag="grid_lines", width="0.5")

    # draw th egold atom nuclei
    canvas.create_oval((-ox-goldnuclei_r)*rx, ch-(-oy+goldnuclei_r)*ry, (-ox+goldnuclei_r)*rx, ch-(-oy-goldnuclei_r)*ry, fill=None, outline="yellow", width="1.5", tag="gold_nuclei")

images = []
def create_oval(x1, y1, x2, y2, **kwargs):
    if 'alpha' in kwargs:
        alpha = int(kwargs.pop('alpha') * 255)
        fill = kwargs.pop('fill')
        fill = root.winfo_rgb(fill) + (alpha,)
        image = Image.new('RGBA', (int(x2-x1), int(y2-y1)), fill)
        images.append(ImageTk.PhotoImage(image))
        canvas.create_image(x1, y1, image=images[-1], anchor='nw')
    canvas.create_oval(x1, y1, x2, y2, **kwargs)

def update_gold_nuclei(R):
    R = float(R)
    canvas.delete("gold_nuclei")
    # draw th egold atom nuclei
    canvas.create_oval((-ox - R) * rx, ch - (-oy + R) * ry, (-ox + R) * rx,
                       ch - (-oy - R) * ry, outline="yellow", width="1.5", tag="gold_nuclei")

def start_the_motion():
    global path_color
    goldnuclei_r = float(scale_R.get())
    alpha_1 = {
        "x": ox,
        "y": float(scale.get()),
        "vx": float(scale_v.get()),
        "vy": 0,
    }
    startvar.set("start")
    q_alpha = 4
    q_atom = 70
    m_alpah = 2
    delta_t = 0.01
    k = 1000
    while startvar.get() == "start":
        org_x, org_y = alpha_1["x"], alpha_1["y"]

        r_square = pow(alpha_1["x"], 2) + pow(alpha_1["y"], 2)
        if r_square >= pow(goldnuclei_r, 2):
            F_E = k*q_alpha*q_atom/r_square
        elif r_square < pow(goldnuclei_r, 2):
            F_E = k*q_alpha*q_atom*math.sqrt(r_square)/pow(goldnuclei_r, 3)
        # set the alpha particle acclerations
        a_x = F_E * alpha_1["x"]/(math.sqrt(r_square) * m_alpah)
        a_y = F_E * alpha_1["y"] / (math.sqrt(r_square) * m_alpah)

        # set the alpha particle velocities
        alpha_1["vx"] = alpha_1["vx"] + a_x * delta_t
        alpha_1["vy"] = alpha_1["vy"] + a_y * delta_t

        # set the alpha particle (x,y) positions
        alpha_1["x"] = alpha_1["x"] + alpha_1["vx"] * delta_t
        alpha_1["y"] = alpha_1["y"] + alpha_1["vy"] * delta_t

        # update the canvas by new alpha particles positions
        canvas.delete("alpha")
        canvas.create_oval((alpha_1["x"]-ox)*rx-2, (ch-(alpha_1["y"]-oy)*ry)-2, (alpha_1["x"]-ox)*rx+2, (ch-(alpha_1["y"]-oy)*ry)+2, fill="red", outline="red", tag="alpha" )

        canvas.create_line((org_x-ox)*rx, ch-(org_y-oy)*ry, (alpha_1["x"]-ox)*rx, ch-(alpha_1["y"]-oy)*ry, fill=path_color, width="0.5", tag="path")
        # canvas update after 0.01s
        canvas.update()
        canvas.after(10)

def set_position(y):
    canvas.delete("position_marker")
    canvas.create_line(0, ch-(-oy+float(y))*ry, 5, ch-(-oy+float(y))*ry, fill="orange", tag="position_marker")

def automation():
    initial_position = -50
    while initial_position <= 50:
        scale.set(initial_position)

        startvar.set("start")
        start_the_motion()

        if alpha_1["x"] <= 80 or alpha_1["y"] <= 60 or alpha_1["x"] >= -100 or alpha_1["y"] >= -60:
            startvar.set("stop")
        initial_position += 4

def selectimage():
        image_file = filedialog.askopenfilename(title="Open Image", filetypes=(("JPG files","*.jpg"),("PNG files", "*.png")))
        global wallpaper
        wallpaper = ImageTk.PhotoImage(Image.open(image_file).resize((cw,ch),Image.ANTIALIAS))
        canvas.delete("bgimage")
        canvas.create_image(cw/2,ch/2,image=wallpaper,tag="bgimage")
        canvas.lower("bgimage")

        # set bg parameter to full
        # bgvar="full"

def choose_color():
    global path_color
    color = colorchooser.askcolor()[1]
    if color:
        path_color = color

frame1 = Frame(root, bg="green")
frame1.grid(row=0, column=6)
Button(frame1, text="start", bg="green2", font=('Helvetica', 10), width="7", relief=FLAT, command=start_the_motion).grid(row=0, column=0)
Button(frame1, text="stop", bg="red", font=('Helvetica', 10), width="7", relief=FLAT, command=lambda: startvar.set("stop"), borderwidth=0, activebackground="red").grid(row=1, column=0)

Button(frame1, text="automation", bg="red", font=('Helvetica', 10), width="7", relief=FLAT, command=automation).grid(row=2, column=0)

Button(frame1, text="delete paths", bg="red", font=('Helvetica', 10), width="10", relief=FLAT, command=lambda:canvas.delete("path")).grid(row=3, column=0)



global path_color
path_color = "red"
Button(frame1, text="path color", bg="green2", font=('Helvetica', 10), width="10", relief=FLAT, command=choose_color).grid(row=4, column=0)

Button(frame1, text="select bg", bg="blue", font=('Helvetica', 10), width="10", relief=FLAT, command=selectimage).grid(row=5, column=0)

scale = Scale(root, from_=-50, to=50, orient=HORIZONTAL, length="300", command=set_position, relief=FLAT, sliderrelief=FLAT, bg="black", fg="gray")
scale.grid(row=3, column=1)
Label(root, text="Y-position", bg="black", fg="white").grid(row=3, column=0)

scale_v = Scale(root, from_=0, to=500, orient=HORIZONTAL, length="300", relief=FLAT, sliderrelief=FLAT, bg="black", fg="gray")
scale_v.grid(row=4, column=1)
scale_v.set(120)
Label(root, text="speed", bg="black", fg="white").grid(row=4, column=0)

scale_R  =Scale(root, from_=0, to=50, orient=HORIZONTAL, length="300", command=update_gold_nuclei, relief=FLAT,sliderrelief=FLAT, bg="black", fg="gray" )
scale_R.grid(row=5, column=1)
scale_R.set(3)
Label(root, text="size", bg="black", fg="white").grid(row=5, column=0)

# draw the x_y grid in the canvas
create_the_xy_grids()

# identify alpha particle initial parameters
alpha_1 = {
    "x" : ox,
    "y" : 5,
    "vx" : 110,
    "vy" : 0,
}

root.mainloop()
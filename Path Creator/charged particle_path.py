from tkinter import*
import math
from PIL import Image, ImageTk
from tkinter import colorchooser
from tkinter import filedialog

root = Tk()
root.title("motion path under the electric fileds")
root.geometry("1200x750")
root.config(bg="black")


cw = 900
ch = 550
canvas = Canvas(root, width=cw, height=ch, bg="#262c3d", bd=0, highlightthickness=0)
canvas.grid(row=0, column=0, rowspan=3, columnspan=5)

menu = Menu(root)
root.config(menu =menu)
file_menu = Menu(menu)
menu.add_cascade(label="File", menu = file_menu)

# identify the parameter of coordinate system
rx, ry = 5, 5
ox , oy = -100, -55
startvar = StringVar()
startvar.set("start")

atoms = []
magnetic_filed = 0
global num_of_atom
num_of_atom = 0
global clicked_id
clicked_id = False
global velocity_r
velocity_r = 0.5

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

def update_gold_nuclei():
    canvas.delete("gold_nuclei")
    R = 1.2
    for atom in atoms:
        # draw the gold atom nuclei
        if atom[1] == "c":
            canvas.create_oval((-ox - R+ atom[0][0]) * rx, ch - (-oy + R+atom[0][1]) * ry, (-ox + R+ atom[0][0]) * rx,ch - (-oy - R+atom[0][1]) * ry, outline="green2", fill="green2",width="1.5", tag=f"part{atom[0][3]}")
            if atom[0][2]>0:
                canvas.create_text((-ox  + atom[0][0]) * rx, ch - (-oy  + atom[0][1]) * ry,text="+", fill="red", tag=f"part{atom[0][3]}", font=('vedana', 14))
            else:
                canvas.create_text((-ox + atom[0][0]) * rx, ch - (-oy + atom[0][1]) * ry, text="-", fill="red", tag=f"part{atom[0][3]}", font=('verdana', 14))


def get_distance(atom, alpha):
    atom_x , atom_y = atom[0][0], atom[0][1]
    x, y = alpha["x"], alpha["y"]
    # calculate the distance among the atom and alpha particle
    d = math.sqrt(pow(x-atom_x,2)+pow(y-atom_y,2))
    # calculate the sin and cosines for directions
    sine = (y-atom_y)/d
    cosine = (x-atom_x)/d
    # return the distance sine and cosine as list
    return [d, sine, cosine]

def start_the_motion():
    global path_color
    canvas.delete("position_marker", "velocity_marker")
    alpha_1 = {
        "x": float(scalex.get()),
        "y": float(scaley.get()),
        "vx": float(scale_vx.get()),
        "vy": float(scale_vy.get()),
    }
    startvar.set("start")
    q_alpha = 4
    # describe the charged particle as [x,y, charge]
    m_alpah = 4
    delta_t = 0.001
    k = 1000
    while startvar.get() == "start":
        org_x, org_y = alpha_1["x"], alpha_1["y"]

        a_x = 0
        a_y = 0
        for atom in atoms:
            if atom[1]  == "c":
                info = get_distance(atom, alpha_1)
                a = k*q_alpha*atom[0][2]/(info[0]**2*m_alpah)
                a_x += a*info[2]
                a_y += a*info[1]
        # calculate the magnetic foece on the charges
        a_x +=  -magnetic_filed*q_alpha*alpha_1["vy"]/m_alpah
        a_y += magnetic_filed*q_alpha*alpha_1["vx"]/m_alpah

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
        # canvas.after(2)

def set_position_y(y):
    l = 1
    x , y  = float(scalex.get()), float(y)
    canvas.delete("position_marker")
    canvas.create_line((-ox - l + x) * rx, ch - (-oy + y) * ry, (-ox + l + x) * rx,ch - (-oy + y) * ry, fill="orange", tag="position_marker")
    canvas.create_line((-ox + x) * rx, ch - (-oy + l + y) * ry, (-ox + x) * rx,ch - (-oy - l + y) * ry, fill="orange", tag="position_marker")

def set_position_x(x):
    l = 1
    x , y  = float(x), float(scaley.get())
    canvas.delete("position_marker")
    canvas.create_line((-ox - l + x) * rx, ch - (-oy + y) * ry, (-ox + l + x) * rx,ch - (-oy + y) * ry, fill="orange", tag="position_marker")
    canvas.create_line((-ox + x) * rx, ch - (-oy + l + y) * ry, (-ox + x) * rx,ch - (-oy - l + y) * ry, fill="orange", tag="position_marker")

def set_velocity_x(vx):
    global velocity_r
    # get the numericle value for velocity components
    vx, vy = float(vx), float(scale_vy.get())
    # get the position of alpha particle
    X ,Y = float(scalex.get()), float(scaley.get())
    # calculate the summation of velocity
    V = math.sqrt(pow(vx, 2) + pow(vy, 2))
    sin_V, cos_V = vy/V, vx/V
    # velocity line other component
    last_XV, last_YV = X + V*cos_V, Y + V*sin_V
    # create the velocity line in the canvas
    canvas.delete("velocity_marker")
    canvas.create_line((-ox + X)*rx, ch-(-oy + Y)*ry, (-ox + last_XV)*rx, ch-(-oy+last_YV)*ry, fill="blue", tag="velocity_marker", arrow="last")

def set_velocity_y(vy):
    global velocity_r
    # get the numericle value for velocity components
    vx, vy = float(scale_vx.get()), float(vy)
    # get the position of alpha particle
    X ,Y = float(scalex.get()), float(scaley.get())
    # calculate the summation of velocity
    V = math.sqrt(pow(vx, 2) + pow(vy, 2))
    sin_V, cos_V = vy/V, vx/V
    # velocity line other component
    last_XV, last_YV = X + V*cos_V, Y + V*sin_V
    # create the velocity line in the canvas
    canvas.delete("velocity_marker")
    canvas.create_line((-ox + X)*rx, ch-(-oy + Y)*ry, (-ox + last_XV)*rx, ch-(-oy+last_YV)*ry, fill="blue", tag="velocity_marker", arrow="last")



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

def insert_charged_particle():
    global num_of_atom
    if entry_X.get() and entry_Y.get() and entry_mass.get():
        atoms.append([[float(entry_X.get()), float(entry_Y.get()), float(entry_mass.get()), num_of_atom], "c"])
        num_of_atom += 1
    # add the charged particle images to canvas
    update_gold_nuclei()

def remove_item():
   global clicked_id
   if clicked_id >= 0:
       info_atom = atoms[clicked_id][0]
       # update the atoms list for absence of the clicked id atom
       atoms[clicked_id] = [info_atom, "a"]
       # delete the all object in the canvas
       canvas.delete(ALL)
       # create the new grid system
       create_the_xy_grids()
       # create the new particle in the canvas
       update_gold_nuclei()
       # empty the diplay labels
       id_label.config(text="")
       xy_label.config(text="")
       charge_label.config(text="")


def create_new_frame():
    # delete ALL from the canvas
    canvas.delete(ALL)
    # create the new grid system
    create_the_xy_grids()
    # set the atoms list as empty list
    global atoms
    atoms = []

def select_particle(event):
    # get the clicked object on the canvas
    clicked_object = canvas.find_closest(event.x, event.y)[0]
    # get the tag for this object
    clicked_tag = canvas.gettags(clicked_object)[0]
    # check the select tag have charge particle
    if clicked_tag[0:4] == "part":
        # get the id_num  of clicked particle
        global clicked_id
        clicked_id = int(clicked_tag[4:])
        # get the information list from the atoms list
        clicked_info = atoms[clicked_id][0]
        # display the information in the frame
        id_label.config(text=f"ID : {clicked_id}")
        xy_label.config(text=f"X : {clicked_info[0]} | Y : {clicked_info[1]}")
        charge_label.config(text=f"Charge is {clicked_info[2]}")
        # highlight the selected charge particles
        canvas.delete("highlight_circle")
        R = 1.4
        canvas.create_oval((-ox - R + clicked_info[0]) * rx, ch - (-oy + R + clicked_info[1]) * ry, (-ox + R + clicked_info[0]) * rx,ch - (-oy - R + clicked_info[1]) * ry, outline="yellow", fill=None, tag="highlight_circle")

file_menu.add_command(label="New", command=create_new_frame)

frame1 = Frame(root, bg="black")
frame1.grid(row=0, column=6)
Button(frame1, text="start", bg="green2", font=('Helvetica', 10), width="10", relief=FLAT, command=start_the_motion).grid(row=0, column=0, pady=1)
Button(frame1, text="stop", bg="red", font=('Helvetica', 10), width="10", relief=FLAT, command=lambda: startvar.set("stop"), borderwidth=0, activebackground="red").grid(row=1, column=0)

Button(frame1, text="automation", bg="red", font=('Helvetica', 10), width="10", relief=FLAT, command=automation).grid(row=2, column=0, pady=1)

Button(frame1, text="delete paths", bg="red", font=('Helvetica', 10), width="10", relief=FLAT, command=lambda:canvas.delete("path")).grid(row=3, column=0, pady=1)



global path_color
path_color = "red"
Button(frame1, text="path color", bg="green2", font=('Helvetica', 10), width="10", relief=FLAT, command=choose_color).grid(row=4, column=0, pady=1)

Button(frame1, text="select bg", bg="blue", font=('Helvetica', 10), width="10", relief=FLAT, command=selectimage).grid(row=5, column=0, pady=1)

# create the frame for get data of charged particles
frame2 = LabelFrame(frame1, text="charged particles", width="2", bg="black", fg="white")
frame2.grid(row=6, column=0)
Label(frame2, text="X", bg="black", fg="white").grid(row=0, column=0)
Label(frame2, text="Y",  bg="black", fg="white").grid(row=1, column=0)
Label(frame2, text="charge",  bg="black", fg="white").grid(row=2, column=0)

entry_X = Entry(frame2, relief=FLAT, width="10")
entry_X.grid(row=0, column=1)
entry_Y = Entry(frame2, relief=FLAT, width="10")
entry_Y.grid(row=1, column=1)
entry_mass = Entry(frame2, relief=FLAT, width="10", bg="yellow")
entry_mass.grid(row=2, column=1)

Button(frame2, text="insert", bg='green2', relief=FLAT, fg="white", width="15" ,command=insert_charged_particle).grid(row=3, column=0, columnspan=2)

entry_del = Entry(frame2, relief=FLAT , width="7")
entry_del.grid(row=4, column=0)

# scales for set parameters
scaley = Scale(root, from_=-60, to=60, orient=HORIZONTAL, length="600", command=set_position_y, relief=FLAT, sliderrelief=FLAT, bg="black", fg="gray", bd=0, highlightthickness=0, troughcolor="#1e1f21")
scaley.grid(row=3, column=1)
Label(root, text="Y-position", bg="black", fg="white").grid(row=3, column=0)

scalex = Scale(root, from_=-100, to=80, orient=HORIZONTAL, length="600", relief=FLAT, sliderrelief=FLAT, bg="black", fg="gray", command=set_position_x, bd=0, highlightthickness=0, troughcolor="#1e1f21")
scalex.grid(row=4, column=1)
Label(root, text="X-position", bg="black", fg="white").grid(row=4, column=0)

scale_vx = Scale(root, from_=-500, to=500, orient=HORIZONTAL, length="600", relief=FLAT, sliderrelief=FLAT, bg="black", fg="gray", command=set_velocity_x, bd=0, highlightthickness=0, troughcolor="#323744")
scale_vx.grid(row=5, column=1)
scale_vx.set(20)
Label(root, text="speed of x", bg="black", fg="white").grid(row=5, column=0)

scale_vy = Scale(root, from_=-500, to=500, orient=HORIZONTAL, length="600", relief=FLAT, sliderrelief=FLAT, bg="black", fg="gray", command=set_velocity_y, bd=0, highlightthickness=0, troughcolor="#323744")
scale_vy.grid(row=6, column=1)
scale_vy.set(20)
Label(root, text="speed of y", bg="black", fg="white").grid(row=6, column=0)

# create the frame for displaying clicked particle in canvas
frame_display = LabelFrame(root, bg="black", text="information", fg="white", bd=1)
frame_display.grid(row=3, column=2, rowspan=3, padx=2)
# label for dispalying id number of particle
id_label = Label(frame_display, bg="black", fg="white", font=('Fira Code', 11), width="20")
id_label.grid(row=0, column=0)
# label for dispalying coordinates of particles
xy_label = Label(frame_display, bg="black", fg="white", font=('Fira Code', 11), width="20")
xy_label.grid(row=1, column=0)
# label for display charge of particle
charge_label = Label(frame_display, bg="black", fg="white", font=("Fira Code", 11), width="20")
charge_label.grid(row=2, column=0)
# Button for remove selected particle
Button(frame_display, text="remove", bg="red", width="20", relief=FLAT,command=remove_item).grid(row=3, column=0)

# draw the x_y grid in the canvas
create_the_xy_grids()

update_gold_nuclei()

# bind the canvas
canvas.bind("<Button-1>", select_particle)


# identify alpha particle initial parameters
alpha_1 = {
    "x" : ox,
    "y" : 5,
    "vx" : 110,
    "vy" : 0,
}

root.mainloop()
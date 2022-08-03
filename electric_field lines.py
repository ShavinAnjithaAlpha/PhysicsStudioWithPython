from tkinter import*
import math
from PIL import Image, ImageTk
from tkinter import colorchooser
from tkinter import filedialog
from tkinter import ttk

root = Tk()
root.title("electric field line creator")
root.geometry("1200x750")
root.config(bg="black")


cw = 900
ch = 560
canvas = Canvas(root, width=cw, height=ch, bg="#262c3d")
canvas.grid(row=0, column=0, rowspan=3, columnspan=5)

menu = Menu(root)
root.config(menu =menu)
file_menu = Menu(menu)
menu.add_cascade(label="File", menu = file_menu)

# identify the parameter of coordinate system
rx, ry = 10, 10
ox , oy = -45, -28
startvar = StringVar()
startvar.set("start")

atoms = []
global skip_regions
skip_regions = []
global num_of_atom
num_of_atom = 0
global clicked_id
clicked_id = False
global velocity_r
velocity_r = 0.5
global R
R = 1.0

# create the xy_grid function
def create_the_xy_grids():
    # craete the x axis
    canvas.create_line(0, ch-(-oy*ry), cw, ch-(-oy*ry), fill="white", tag="grid_lines", width="1.5")
    # craete the y axis
    canvas.create_line(-ox*rx, 0, -ox*rx,  ch,  fill="white", tag="grid_lines", width="1.5")
    # create the x lines
    for i in range(0, int(cw/rx)):
        if (ox+i)%5 == 0:
            canvas.create_line(i*rx, 0, i*rx, ch, fill="#323744", tag="grid_lines", width="0.5")
    # craete the y lines
    for j in range(0, int(ch/ry)):
        if (oy+j) % 5 == 0:
            canvas.create_line(0, j*ry, cw,  j*ry, fill="#323744", tag="grid_lines", width="0.5")


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

def display_x_and_y(event):
    # claculate the x, y to display
    x, y = ox + event.x/rx, oy + (ch-event.y)/ry
    # display the x. y as the string
    label_x.config(text=f"X : {round(x,2)}")
    label_y.config(text=f"Y : {round(y,2)}")


def update_gold_nuclei():
    global R
    canvas.delete("gold_nuclei")
    for atom in atoms:
        # draw the gold atom nuclei
        if atom[1] == "c":
            canvas.create_oval((-ox - R+ atom[0][0]) * rx, ch - (-oy + R+atom[0][1]) * ry, (-ox + R+ atom[0][0]) * rx,ch - (-oy - R+atom[0][1]) * ry, outline="green2", fill="green2",width="1.5", tag=f"part{atom[0][3]}")
            if atom[0][2]>0:
                canvas.create_text((-ox  + atom[0][0]) * rx, ch - (-oy  + atom[0][1]) * ry,text="+", fill="red", tag=f"part{atom[0][3]}", font=('vedana', 14))
            else:
                canvas.create_text((-ox + atom[0][0]) * rx, ch - (-oy + atom[0][1]) * ry, text="-", fill="red", tag=f"part{atom[0][3]}", font=('verdana', 14))

def update_skipregion():
    global skip_regions
    skip_regions = []
    for item in atoms:
        # check the particle is removed or consists
        if item[1] == "c":
            skip_regions.append([item[0][3]])
        print(skip_regions)

def insert_charged_particle():
    global num_of_atom
    if entry_charge.get():
        atoms.append([[float(scalex.get()), float(scaley.get()), float(entry_charge.get()), num_of_atom], "c"])
        num_of_atom += 1
        # update the skip region list for new situation
        update_skipregion()
    # add the charged particle images to canvas
    update_gold_nuclei()

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

def return_angle(sin, cos):
    if sin >= 0 and cos >= 0:
        return math.degrees(math.acos(cos))
    elif sin >= 0 and cos < 0:
        return math.degrees(math.acos(cos))
    elif sin < 0 and cos < 0:
        return 180 + math.degrees(math.acos(abs(cos)))
    else:
        return 360+math.degrees(math.asin(sin))

def set_twovalues(x1,x2,x3):
    return [min(x1,x2,x3),max(x1,x2,x3)]

def check_in_the_particle(x,y):
    global R, skip_regions
    op = []
    for p in atoms:
        px, py = p[0][0], p[0][1]
        distance_p = math.sqrt(pow(x-px, 2) + pow(y-py,2))
        if p[1] == "c":
            if distance_p < R:
                op.append("True")
                # calculate the angle
                sin ,cos = (y-py)/distance_p, (x-px)/distance_p
                angle, i = return_angle(sin, cos), p[0][3]
                # insert angle to the skip region list by checking
                print(f"skip regions is {skip_regions}")
                if len(skip_regions[i]) < 3:
                    skip_regions[i].append(angle)
                else:
                    x1, x2, x3 = skip_regions[i][1], skip_regions[i][2], angle
                    append_values = set_twovalues(x1, x2, x3)
                    skip_regions[i][1] = append_values[0]
                    skip_regions[i][2] = append_values[1]

            else:
                op.append("False")
    # return True or False by io list have True or not
    if "True" in op:
        return True
    else:
        return False

def up_to_charges():
    for i in range(0,len(atoms)):
        canvas.lift(f"part{i}")

def start_the_motion(l):
    global path_color
    canvas.delete("position_marker", "velocity_marker")
    startvar.set("start")
    # describe the charged particle as [x,y, charge]
    delta_l = l
    k = 1000
    while startvar.get() == "start":
        if startvar.get() == "stop":
            canvas.update()

        a_x = 0
        a_y = 0
        for atom in atoms:
            if atom[1]  == "c":
                info = get_distance(atom, alpha_1)
                a = k*atom[0][2]/(info[0]**2)
                a_x += a*info[2]
                a_y += a*info[1]
        # calculate the sin and cos
        a = math.sqrt(pow(a_x, 2)+ pow(a_y, 2))
        sin_of_tangent = a_y/a
        cos_of_tangent = a_x/a
         # calculate the last x,y
        last_x = alpha_1["x"] + delta_l*cos_of_tangent
        last_y = alpha_1["y"] + delta_l*sin_of_tangent


        canvas.create_line((alpha_1["x"]-ox)*rx, ch-(alpha_1["y"]-oy)*ry, (last_x-ox)*rx, ch-(last_y-oy)*ry, fill=path_color, width="0.5", tag="path")
        alpha_1["x"] = last_x
        alpha_1["y"] = last_y
        # check the line goes pass the boundary
        if (last_x < ox or last_y < oy or last_x > -ox or last_y > -oy) or check_in_the_particle(last_x, last_y):
            startvar.set("stop")
            break
        # canvas update after 0.01s
        canvas.update()

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

def automation():
    R = 1.2
    for particle in atoms:
        ox, oy = particle[0][0], particle[0][1]
        id_num = particle[0][3]
        theta = 0
        while theta < 360:
            alpha_1["x"] = ox + R*math.cos(math.radians(theta))
            alpha_1["y"] = oy + R*math.sin(math.radians(theta))
            startvar.set("start")
            if particle[1] == "c":
                try:
                    angle1, angle2 = skip_regions[id_num][1], skip_regions[id_num][2]
                except:
                    angle1 = False
                    angle2 = False
                if not(angle1 and angle2) or not(theta >= angle1 and theta <= angle2):
                    if particle[0][2] < 0:
                        start_the_motion(-0.4)
                    else:
                        start_the_motion(0.4)
            theta += int(line_density.get())
        up_to_charges()

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
       # update the skip region list
       update_skipregion()

def create_new_frame():
    # delete ALL from the canvas
    canvas.delete(ALL)
    # create the new grid system
    create_the_xy_grids()
    # set the atoms list as empty list
    global atoms
    atoms = []
    # set the count variable to zero
    global  num_of_atom
    num_of_atom = 0
    # set the skip region list as the empty list
    update_skipregion()

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

    # rest of function for display the electric fiels magnitude and directions
    # calculate the electric field intencity in the clicked position
    a_x = 0
    a_y = 0
    k=100
    x, y = ox + (event.x/rx), oy + (ch-event.y)/ry
    for atom in atoms:
        if atom[1] == "c":
            info = get_distance(atom, {"x": x, "y" : y})
            a = k * atom[0][2] / (info[0] ** 2)
            a_x += a * info[2]
            a_y += a * info[1]
    # calculate the sin and cos
    a = math.sqrt(pow(a_x, 2) + pow(a_y, 2))
    if a != 0:
        sin_of_tangent = a_y / a
        cos_of_tangent = a_x / a
        end_x = 60*cos_of_tangent + canvas_info_w/2
        end_y = -60*sin_of_tangent + canvas_info_h/2
        # draw the direction fiels arrow in the canvas
        canvas_info.delete("electric_arrow")
        canvas_info.create_line(canvas_info_w/2, canvas_info_h/2, end_x, end_y, tag="electric_arrow", fill="blue", arrow="last", width="2")
        # display the magbitude of elec tric field intemsity
        angle = return_angle(sin_of_tangent, cos_of_tangent)
        if angle <= 180:
            canvas_info.delete("a")
            canvas_info.create_text(canvas_info_w/2, canvas_info_h/2 + 20, text=f"intensity = {round(a, 3)}", tag="a", fill="white", font=('verdana', 10))
            canvas_info.create_text(canvas_info_w / 2, canvas_info_h / 2 + 35, text=f"angle = {round(angle,3)}",
                                    tag="a", fill="white", font=('verdana', 10))
        else:
            canvas_info.delete("a")
            canvas_info.create_text(canvas_info_w / 2, canvas_info_h / 2 - 20, text=f"intensity = {round(a, 3)}", tag="a" , fill="white", font=('verdana', 10))
            canvas_info.create_text(canvas_info_w / 2, canvas_info_h / 2 - 35, text=f"angle = {round(angle,3)}",
                                    tag="a", fill="white", font=('verdana', 10))

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

# create the frame for display position by (x,y) in the frame
frame2 = LabelFrame(frame1, text="charged particles", width="2", bg="black", fg="white")
frame2.grid(row=6, column=0)

# create the Label for x and y
label_x = Label(frame2, bg="black", fg="white", font=('verdana', 10))
label_x.grid(row=0, column=0)
label_y = Label(frame2, bg="black", fg="white", font=('verdana', 10))
label_y.grid(row=1, column=0)



# scales for set parameters
scaley = Scale(root, from_=-27, to=27, orient=HORIZONTAL, length="300", command=set_position_y, relief=FLAT, sliderrelief=FLAT, bg="black", fg="gray")
scaley.grid(row=3, column=1)
Label(root, text="Y-position", bg="black", fg="white").grid(row=3, column=0)

scalex = Scale(root, from_=-45, to=45, orient=HORIZONTAL, length="300", relief=FLAT, sliderrelief=FLAT, bg="black", fg="gray", command=set_position_x)
scalex.grid(row=4, column=1)
Label(root, text="X-position", bg="black", fg="white").grid(row=4, column=0)
# get the sensitivity for draw the electric field lines
line_density = ttk.Spinbox(root, from_=1, to=20)
line_density.grid(row=4, column=2, rowspan=2)
line_density.set(10)
# entry box for the insert charge
Label(root, text="Charge", bg="black", fg="white").grid(row=5, column=0)
entry_charge = Entry(root, relief=FLAT, width="20", font=('verdana', 12), bg="#1e1f21", fg="white")
entry_charge.grid(row=5, column=1)

Button(root, text="insert", bg='green2', relief=FLAT, fg="white", width="15",borderwidth=0,font=('verdana', 11) ,command=insert_charged_particle).grid(row=5, column=2)


# create the frame for displaying clicked particle in canvas
frame_display = LabelFrame(root, bg="black", text="information", fg="white")
frame_display.grid(row=3, column=3, rowspan=3, padx=2)
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

# frame for diplay electric field intensity image
frame_info = Frame(root, bg="black")
frame_info.grid(row=3, column=4, rowspan=3, padx=1)

# create the canvas for display the electric fiels directions and magnitude
canvas_info_w = 150
canvas_info_h = 150
canvas_info = Canvas(frame_info, width=canvas_info_w, height=canvas_info_h, bg="black", relief=FLAT, borderwidth=0)
canvas_info.grid(row=0, column=0)
# create the main line for mesure the direction relative to main line
canvas_info.create_line(canvas_info_w/2, canvas_info_h/2, canvas_info_w, canvas_info_h/2, fill="white", width="1.5")

# draw the x_y grid in the canvas
create_the_xy_grids()

update_gold_nuclei()

# bind the canvas
canvas.bind("<Button-1>", select_particle)
canvas.bind("<Motion>", display_x_and_y)

# identify alpha particle initial parameters
alpha_1 = {
    "x" : ox,
    "y" : 5,
    "vx" : 110,
    "vy" : 0,
}

root.mainloop()
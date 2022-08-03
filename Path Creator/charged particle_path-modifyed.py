from tkinter import*
import math
from PIL import Image, ImageTk
from tkinter import colorchooser
from tkinter import filedialog


class motion_path(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.master.title("motion under the electric field")
        self.master.geometry("800x800")
        self.master.config(bg="black")
        self.grid(row=0, column=0)

        # defined the screen width and height
        self.w = 800
        self.h = 550
        self.cw = 1000
        self.ch = 700
        self.path_color = "red"
        self.bgcolor = "black"
        # creat ehte frame for pack the canvas and its components
        self.frame_canvas = Frame(self, bg=self.bgcolor)
        self.frame_canvas.grid(row=0, column=0)
        # create the canvas object
        self.canvas = Canvas(self.frame_canvas, width=self.w, height=self.h, bg="#262c3d", highlightthickness=0, scrollregion=(0,0, self.cw, self.ch))
        self.canvas.grid(row=0, column=0)
        # create the scroll bar for canvas
        self.scroll_x = Scrollbar(self.frame_canvas, orient=HORIZONTAL, command=self.canvas.xview)
        self.scroll_x.grid(row=1 ,column=0, sticky=EW)
        self.scroll_y = Scrollbar(self.frame_canvas, orient=VERTICAL, command=self.canvas.yview)
        self.scroll_y.grid(row=0, column=1, sticky=NS)
        # attch the scrollbar to the canvas
        self.canvas.config(xscrollcommand=self.scroll_x.set, yscrollcommand=self.scroll_y.set)


        # create the men items
        self.menu = Menu(self)
        self.master.config(menu =self.menu)
        self.file_menu = Menu(self.menu)
        self.menu.add_cascade(label="File", menu = self.file_menu)
        # add the command to menu
        self.file_menu.add_command(label="New", command=self.create_new_frame)
        self.file_menu.add_command(label="path color", command=self.set_pathcolor)
        self.file_menu.add_command(label="select bg image", command=self.select_bgimage)

        # identify the parameter of coordinate system
        rx, ry = 5, 5
        ox , oy = -100, -55
        self.startvar = StringVar()
        self.startvar.set("start")


        self.atoms = []
        self.magnetic_filed = 0
        self.num_of_atom = 0
        self.clicked_id = False
        self.velocity_r = 0.5

        # identify motioned particle initial parameters
        self.particle = {
            "x": ox,
            "y": 5,
            "vx": 110,
            "vy": 0,
        }

        self.frame_main = Frame(self, bg=self.bgcolor)
        self.frame_main.grid(row=0, column=1)
        Button(self.frame_main, text="start", bg="green2", font=('Helvetica', 10), width="10", relief=FLAT,
               command=None).grid(row=0, column=0, pady=1)
        Button(self.frame_main, text="stop", bg="red", font=('Helvetica', 10), width="10", relief=FLAT,
               command=None, borderwidth=0, activebackground="red").grid(row=1, column=0, pady=1)

        # Button(frame1, text="automation", bg="red", font=('Helvetica', 10), width="10", relief=FLAT,
          #      command=automation).grid(row=2, column=0, pady=1)

        Button(self.frame_main, text="delete paths", bg="red", font=('Helvetica', 10), width="10", relief=FLAT,
               command=None).grid(row=3, column=0, pady=1)


        # create the frame for get data of charged particles
        self.frame2 = LabelFrame(self.frame_main, text="charged particles", width="2", bg=self.bgcolor, fg="white")
        self.frame2.grid(row=6, column=0)
        Label(self.frame2, text="X", bg="black", fg="white").grid(row=0, column=0)
        Label(self.frame2, text="Y", bg="black", fg="white").grid(row=1, column=0)
        Label(self.frame2, text="charge", bg="black", fg="white").grid(row=2, column=0)

        self.entry_X = Entry(self.frame2, relief=FLAT, width="10")
        self.entry_X.grid(row=0, column=1)
        self.entry_Y = Entry(self.frame2, relief=FLAT, width="10")
        self.entry_Y.grid(row=1, column=1)
        self.entry_mass = Entry(self.frame2, relief=FLAT, width="10", bg="yellow")
        self.entry_mass.grid(row=2, column=1)

        Button(self.frame2, text="insert", bg='green2', relief=FLAT, fg="white", width="15",
               command=None).grid(row=3, column=0, columnspan=2)

        self.entry_del = Entry(self.frame2, relief=FLAT, width="7")
        self.entry_del.grid(row=4, column=0)

        # create the frame for pack the velocity widget components
        self.frame_tool = Frame(self, bg=self.bgcolor)
        self.frame_tool.grid(row=1, column=0)
        # create the frame for pack the scale widgets
        self.frame_scale = LabelFrame(self.frame_tool, text="velocity and position", bg=self.bgcolor, fg="white")
        self.frame_scale.grid(row=0, column=0, pady=8)

        # scales for set parameters
        self.scaley = Scale(self.frame_scale, from_=-60, to=60, orient=HORIZONTAL, length="600", command=None, relief=FLAT,sliderrelief=FLAT, bg="black", fg="gray", bd=0, highlightthickness=0, troughcolor="#1e1f21")
        self.scaley.grid(row=3, column=1)

        Label(self.frame_scale, text="Y-position", bg="black", fg="white").grid(row=3, column=0)

        self.scalex = Scale(self.frame_scale, from_=-100, to=80, orient=HORIZONTAL, length="600", relief=FLAT, sliderrelief=FLAT, bg="black", fg="gray", command=None, bd=0, highlightthickness=0,troughcolor="#1e1f21")
        self.scalex.grid(row=4, column=1)

        Label(self.frame_scale, text="X-position", bg="black", fg="white").grid(row=4, column=0)

        self.scale_vx = Scale(self.frame_scale, from_=-500, to=500, orient=HORIZONTAL, length="600", relief=FLAT, sliderrelief=FLAT, bg="black", fg="gray", command=None, bd=0, highlightthickness=0,troughcolor="#323744")
        self.scale_vx.grid(row=5, column=1)
        self.scale_vx.set(20)

        Label(self.frame_scale, text="speed of x", bg="black", fg="white").grid(row=5, column=0)

        self.scale_vy = Scale(self.frame_scale, from_=-500, to=500, orient=HORIZONTAL, length="600", relief=FLAT, sliderrelief=FLAT, bg="black", fg="gray", command=None, bd=0, highlightthickness=0,troughcolor="#323744")
        self.scale_vy.grid(row=6, column=1)
        self.scale_vy.set(20)

        Label(self.frame_scale, text="speed of y", bg="black", fg="white").grid(row=6, column=0)

        # create the frame for displaying clicked particle in canvas
        self.frame_display = LabelFrame(self.frame_tool, bg=self.bgcolor, text="information", fg="white", bd=1)
        self.frame_display.grid(row=0, column=1)
        # label for dispalying id number of particle
        self.id_label = Label(self.frame_display, bg="black", fg="white", font=('Fira Code', 11), width="20")
        self.id_label.grid(row=0, column=0)
        # label for dispalying coordinates of particles
        self.xy_label = Label(self.frame_display, bg="black", fg="white", font=('Fira Code', 11), width="20")
        self.xy_label.grid(row=1, column=0)
        # label for display charge of particle
        self.charge_label = Label(self.frame_display, bg="black", fg="white", font=("Fira Code", 11), width="20")
        self.charge_label.grid(row=2, column=0)
        # Button for remove selected particle
        Button(self.frame_display, text="remove", bg="red", width="20", relief=FLAT, command=None).grid(row=3,
                                                                                                          column=0)

        # draw the x_y grid in the canvas
        # create_the_xy_grids()

        # update_gold_nuclei()

        # bind the canvas
        # canvas.bind("<Button-1>", select_particle)

    # create the xy_grid function
    def create_the_xy_grids():
        # craete the x axis
        self.canvas.create_line(0, ch-(-oy*ry), cw, ch-(-oy*ry), fill="white", tag="grid_lines", width="1.5")
        # craete the y axis
        self.canvas.create_line(-ox*rx, 0, -ox*rx,  ch,  fill="white", tag="grid_lines", width="1.5")
        # create the x lines
        for i in range(0, int(cw/rx/10)):
            self.canvas.create_line(i*10*rx, 0, i*10*rx, ch, fill="#323744", tag="grid_lines", width="0.5")
        # craete the y lines
        for j in range(0, int(ch/ry/10)):
            self.canvas.create_line(0, j*10*rx, cw,  j*10*rx, fill="#323744", tag="grid_lines", width="0.5")




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


    def create_new_frame(self):
        # delete ALL from the canvas
        self.canvas.delete(ALL)
        # create the new grid system
        self.create_the_xy_grids()
        # set the atoms list as empty list
        self.atoms = []

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

    def set_pathcolor(self):
        self.path_color = colorchooser.askcolor()[0]

    def select_bgimage(self):
        # ask the file name for wallpaper
        self.wallpaper_path = filedialog.askopenfilename(title="background image", filetypes=(("JPG files", "*.jpg"),("PNG files", "*.png")))
        # load the wallpaper as image
        self.wallpaper = ImageTk.PhotoImage(Image.open(self.wallpaper_path).resize((self.cw, self.ch), Image.ANTIALIAS))

        # create the image in the canvas
        self.canvas.delete("wallpaper")
        self.canvas.create_image(0, 0, image=self.wallpaper, anchor="nw", tag="wallpaper")
        # set the image to lower frame in the canvas
        self.canvas.lower("wallpaper")






def main():
    motion_path().mainloop()

if __name__ == "__main__":
    main()

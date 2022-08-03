from tkinter import*
from tkinter import colorchooser
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image
import math

class path_creator(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.master.title("path creator in the electric filed")
        self.master.geometry("1050x800+0+0")
        self.config(bg="black")
        self.grid(row=0, column=0)
        self.master.iconbitmap("pathcreator_logo.ico")

        # identify the theme parameter
        self.path_color = "red"
        self.wallpaper_path = False

        # defined the main data and information of the program that use for calculates and processes
        self.static_particles = []
        self.R = 10
        self.R2 = 12
        self.dt = 0.005
        self.clicked_id = False
        self.start_stop_var = StringVar()
        self.start_stop_var.set("start")
        # define the motioned particle in the program
        self.motion_particle = {}
        # list of the plots
        self.plot_xdata = []
        self.plot_vdata = []
        self.current_wires = []
        self.k = 1000
        self.moveM = 4
        self.moveQ = 4

        # create the menu items
        self.menu = Menu(self)
        self.master.config(menu=self.menu)
        self.file_menu = Menu(self.menu)
        self.info_menu = Menu(self.menu)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.menu.add_cascade(label="info", menu=self.info_menu)
        # add the command to menu
        self.file_menu.add_command(label="New", command=self.new_frame)
        self.file_menu.add_command(label="path color", command=self.set_pathcolor)
        self.file_menu.add_command(label="select bg image", command=self.select_bgimage)
        # add command to info menu
        self.info_menu.add_command(label="set the motion particle info", command=self.set_qandm)

        # defined the screen width and height
        self.w = 750
        self.h = 550
        self.cw = 1000
        self.ch = 700
        self.bgcolor = "black"
        # create the frame for pack the canvas and its components
        self.frame_canvas = Frame(self, bg=self.bgcolor)
        self.frame_canvas.grid(row=0, column=0, padx=0)
        # create the canvas object
        self.canvas = Canvas(self.frame_canvas, width=self.w, height=self.h, bg="#262c3d", highlightthickness=0,
                             scrollregion=(0, 0, self.cw, self.ch))
        self.canvas.grid(row=0, column=0)
        # create the scroll bar for canvas
        self.scroll_x = Scrollbar(self.frame_canvas, orient=HORIZONTAL, command=self.canvas.xview)
        self.scroll_x.grid(row=1, column=0, sticky=EW)
        self.scroll_y = Scrollbar(self.frame_canvas, orient=VERTICAL, command=self.canvas.yview)
        self.scroll_y.grid(row=0, column=1, sticky=NS)
        # attch the scrollbar to the canvas
        self.canvas.config(xscrollcommand=self.scroll_x.set, yscrollcommand=self.scroll_y.set)


        # create the frame for pack the velocity widget components
        self.frame_tool = Frame(self, background=self.bgcolor)
        self.frame_tool.grid(row=1, column=0)
        # create the frame for pack the scale widgets
        self.frame_scale = LabelFrame(self.frame_tool, text="velocity and position", bg=self.bgcolor, fg="white")
        self.frame_scale.grid(row=0, column=0, pady=10, padx=5)

        # scales for set parameters
        self.scaley = Scale(self.frame_scale, from_=-60, to=60, orient=HORIZONTAL, length="500", command=self.motion_particle_y,relief=FLAT, sliderrelief=FLAT, bg="black", bd=0, highlightthickness=0,troughcolor="#1e1f21", resolution=0.1, width="10", showvalue=0)
        self.scaley.grid(row=3, column=1, pady=10)

        Label(self.frame_scale, text="Y-position", bg="black", fg="white").grid(row=3, column=0)

        self.scalex = Scale(self.frame_scale, from_=-100, to=80, orient=HORIZONTAL, length="500", relief=FLAT,
                            sliderrelief=FLAT, bg="black", command=self.motion_particle_x, bd=0, highlightthickness=0, troughcolor="#1e1f21", resolution=0.1, width="10", showvalue=0)
        self.scalex.grid(row=4, column=1, pady=10)

        Label(self.frame_scale, text="X-position", bg="black", fg="white").grid(row=4, column=0)

        self.scale_vx = Scale(self.frame_scale, from_=-500, to=500, orient=HORIZONTAL, length="500", relief=FLAT, sliderrelief=FLAT, bg="black", command=self.display_vx, bd=0, highlightthickness=0,
                              troughcolor="#323744", width="10", showvalue=0)
        self.scale_vx.grid(row=5, column=1, pady=10)
        self.scale_vx.set(20)

        Label(self.frame_scale, text="speed of x", bg="black", fg="white").grid(row=5, column=0)

        self.scale_vy = Scale(self.frame_scale, from_=-500, to=500, orient=HORIZONTAL, length="500", relief=FLAT,
                              sliderrelief=FLAT, bg="black", command=self.display_vy, bd=0, highlightthickness=0,
                              troughcolor="#323744", width="10", showvalue=0)
        self.scale_vy.grid(row=6, column=1, pady=10)
        self.scale_vy.set(20)

        Label(self.frame_scale, text="speed of y", bg="black", fg="white").grid(row=6, column=0)
        # value showing label in scales
        self.label_x = Label(self.frame_scale, text="    ", bg=self.bgcolor, fg="white" ,font=("Helvetica", 11), width="4")
        self.label_x.grid(row=4, column=2, padx=2)
        self.label_y = Label(self.frame_scale, text="    ", bg=self.bgcolor, fg="white", font=("Helvetica", 11))
        self.label_y.grid(row=3, column=2, padx=2)
        self.label_vx = Label(self.frame_scale, text="    ", bg=self.bgcolor, fg="white", font=("Helvetica", 11))
        self.label_vx.grid(row=5, column=2, padx=2)
        self.label_vy = Label(self.frame_scale, text="    ", bg=self.bgcolor, fg="white", font=("Helvetica", 11))
        self.label_vy.grid(row=6, column=2, padx=2)


        # create the frame for displaying clicked particle in canvas
        self.frame_display = LabelFrame(self.frame_tool, bg=self.bgcolor, text="information", fg="white", bd=1)
        self.frame_display.grid(row=0, column=1)
        # label for dispalying id number of particle
        self.id_label = Label(self.frame_display, bg="black", fg="white", font=('Fira Code', 11), width="16")
        self.id_label.grid(row=0, column=0)
        # label for dispalying coordinates of particles
        self.xy_label = Label(self.frame_display, bg="black", fg="white", font=('Fira Code', 11), width="16")
        self.xy_label.grid(row=1, column=0)
        # label for display charge of particle
        self.charge_label = Label(self.frame_display, bg="black", fg="white", font=("Fira Code", 11), width="16")
        self.charge_label.grid(row=2, column=0)
        # Button for remove selected particle
        Button(self.frame_display, text="remove", bg="red", width="20", relief=FLAT, command=self.remove_particle).grid(row=3,column=0)

        # create the frame for pack the buttons
        self.frame_main = Frame(self, bg=self.bgcolor)
        self.frame_main.grid(row=0, column=1, sticky=NS, padx=25)

        # create the main buttons
        Button(self.frame_main, text="start", bg="green2", font=('Helvetica', 10), width="18", relief=FLAT,
               command=self.create_path).grid(row=0, column=0, pady=1)
        Button(self.frame_main, text="stop", bg="red", font=('Helvetica', 10), width="18", relief=FLAT,
               command=lambda : self.start_stop_var.set("stop"), borderwidth=0, activebackground="red").grid(row=1, column=0, pady=1)

        Button(self.frame_main, text="delete paths", bg="red", font=('Helvetica', 10), width="18", relief=FLAT,
               command=lambda : self.canvas.delete("path")).grid(row=3, column=0, pady=1)

        # create the tab frame for get grid info and electric filed info
        self.tab_menu = ttk.Notebook(self.frame_main)
        self.tab_menu.grid(row=4, column=0, pady=0)

        self.tab_1 = Frame(self.tab_menu, bg="#1e1f21", bd=0, highlightthickness=0)
        self.tab_2 = Frame(self.tab_menu, bg="#1e1f21", bd=0, highlightthickness=0)

        self.tab_menu.add(self.tab_1, text="grid info")
        self.tab_menu.add(self.tab_2, text="electric field info")

        # create the tab_1 components
        Label(self.tab_1, text="x", bg="#1e1f21", fg="white", font=("Helvetica", 13)).grid(row=0, column=0)
        Label(self.tab_1, text="y", bg="#1e1f21", fg="white", font=("Helvetica", 13)).grid(row=1, column=0)

        self.entry_x1 = Entry(self.tab_1, relief=FLAT, width="10", bg="#323744", fg="white")
        self.entry_x1.grid(row=0, column=1, padx=2)
        self.entry_x2 = Entry(self.tab_1, relief=FLAT, width="10", bg="#323744", fg="white")
        self.entry_x2.grid(row=0, column=2)

        self.entry_y1 = Entry(self.tab_1, relief=FLAT, width="10", bg="#323744", fg="white")
        self.entry_y1.grid(row=1, column=1, pady=5)
        self.entry_y2 = Entry(self.tab_1, relief=FLAT, width="10", bg="#323744", fg="white")
        self.entry_y2.grid(row=1, column=2, padx=2)

        self.initial_xy_value = [(self.entry_x1, -10), (self.entry_x2, 10), (self.entry_y1, -10), (self.entry_y2, 10)]
        for item in self.initial_xy_value:
            item[0].insert(0, item[1])

        self.x1 , self.x2 = float(self.entry_x1.get()), float(self.entry_x2.get())
        self.y1, self.y2 = float(self.entry_y1.get()), float(self.entry_y2.get())
        self.rx, self.ry = self.cw/(self.x2-self.x1), self.ch/(self.y2-self.y1)

        Label(self.tab_1, text="scroll region of x view", bg="#1e1f21", fg="white", font=("Helvetica", 10), anchor="nw").grid(row=2, column=0, columnspan=3)
        # scale for set the scrollregion of the canvas
        self.scale_scrollx = Scale(self.tab_1, from_=1.0, to=4.0, orient=HORIZONTAL, length="150", bd=0, highlightthickness=0, sliderrelief=FLAT, resolution=0.1, bg="black", troughcolor="black", fg="white")
        self.scale_scrollx.grid(row=3, column=0, columnspan=3)

        Label(self.tab_1, text="scroll region of y view", bg="#1e1f21", fg="white", font=("Helvetica", 10),
              anchor="nw").grid(row=4, column=0, columnspan=3)
        # scale for set the scrollregion of the canvas
        self.scale_scrolly = Scale(self.tab_1, from_=1.0, to=4.0, orient=HORIZONTAL, length="150", bd=0,highlightthickness=0, sliderrelief=FLAT, resolution=0.1, bg="black",troughcolor="black", fg="white")
        self.scale_scrolly.grid(row=5, column=0, columnspan=3)


        # create the update button
        Button(self.tab_1, text='update', bd=0, bg="orange", font=("Helvetica", 13), fg="white", width="15",command=self.update_canvas_grid).grid(row=6, column=0, columnspan=3, pady=10)

        # Button for the change the frame
        Button(self.frame_main, text="<", bd=0, bg="#1e1f21", fg="white",command=lambda e=0:self.change_frame(e), width="7").grid(row=0, column=1, rowspan=5, sticky=NS)
        # create the pop up frame
        self.create_plotframe()


        # create the frame for insert particle information
        Label(self.tab_2, text="X", bg="#1e1f21", fg="white", font=("Helvetica", 10), anchor="nw").grid(row=0, column=0)
        Label(self.tab_2, text="Y", bg="#1e1f21", fg="white", font=("Helvetica", 10), anchor="nw").grid(row=0, column=1)
        # create the scale for get the particle coordinates
        self.scale_infox = Scale(self.tab_2, from_=self.x1, to=self.x2, length="250", orient=VERTICAL, width="5",highlightthickness=0, bg="black", sliderrelief=FLAT, showvalue=0, sliderlength="20", activebackground="red", resolution=0.1, command=self.update_scale_infox, bd=0)
        self.scale_infox.grid(row=1, column=0, padx=35)
        self.scale_infoy = Scale(self.tab_2, from_=self.y1, to=self.y2, length="250", orient=VERTICAL, width="5",highlightthickness=0, bg="black", sliderrelief=FLAT, showvalue=0, sliderlength="20", activebackground="red", resolution=0.1, command=self.update_scale_infoy, bd=0)
        self.scale_infoy.grid(row=1, column=1, padx=35, pady=5)

        self.infox_label = Label(self.tab_2, text="", bg="#1e1f21", fg="white", font=("Helvetica", 11), anchor="nw")
        self.infox_label.grid(row=3, column=0)
        self.infoy_label = Label(self.tab_2, text="", bg="#1e1f21", fg="white", font=("Helvetica", 11),anchor="nw")
        self.infoy_label.grid(row=3, column=1)
        # entry vox for insert the particle charge
        Label(self.tab_2, text="charge", bg="#1e1f21", fg="white", font=("Helvetica", 10), anchor="nw").grid(row=4, column=0)
        self.entry_charge = Entry(self.tab_2, bd=0, bg="orange", font=("Helvetica", 13), width="10")
        self.entry_charge.grid(row=5, column=0, columnspan=2, padx=5)

        Button(self.tab_2, text="insert", bd=0, bg="blue", fg="white", font=("Helvetica", 12), command=self.insert_new_particle).grid(row=6, column=0, columnspan=2, sticky=EW, padx=3, pady=5)

         # frame for display the velocities
        self.frame_velocity = Frame(self, bg="#1e1f21")
        self.frame_velocity.grid(row=1, column=1)
        # create the canvas for display rhe velocity lines
        self.wv = 170
        self.hv = 150
        self.canvas_v = Canvas(self.frame_velocity ,width=self.wv, height=self.hv, bg="#323744", highlightthickness=0, bd=0)
        self.canvas_v.grid(row=0, column=0, padx=0)
        # draa the mid lines
        self.canvas_v.create_line(0, self.hv/2, self.wv, self.hv/2, fill="white")
        self.canvas_v.create_line(self.wv/2, 0, self.wv/2, self.hv, fill="white")


        # update the canvas by draw the grid
        self.update_canvas_grid()
        # binding the canvas
        self.canvas.bind("<Button-1>", self.mouse_clicked)
        self.canvas.bind("<Motion>", self.mouse_moving)


    def mouse_moving(self, event):
        # first check the if self.current direction_var is 1
        if self.current_wire_var.get():
            self.create_current_wire(self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))

    def create_current_wire(self, x, y):
        # first delete previous wire
        self.canvas.delete("current_wire")
        # create the new wire in new position
        gr = math.tan(math.radians(float(self.angle_spinbox.get())))
        xa = x - (self.ch - y)/gr
        yb = y - gr*(self.cw - x)
        # create the line for current wire
        self.canvas.create_line(xa, self.ch, self.cw, yb, fill="blue", width="2.0", tag="current_wire")
        # enter the xa in the entry box
        self.initial_position_cw.delete(0, END)
        self.initial_position_cw.insert(0, self.x1 + xa/self.rx)


    def update_canvas_grid(self):
        # first set the scroll regions of canvas
        ratio_x, ratio_y = float(self.scale_scrollx.get()), float(self.scale_scrolly.get())
        self.cw = self.w * ratio_x
        self.ch = self.h * ratio_y
        self.canvas.config(scrollregion=(0,0 ,self.cw, self.ch))
        # set the wallpaper to the new size if the wallpaper is being
        if self.wallpaper_path:
            self.canvas.delete("wallpaper")
            self.wallpaper = ImageTk.PhotoImage(Image.open(self.wallpaper_path).resize((int(self.cw), int(self.ch)), Image.ANTIALIAS))
            self.canvas.create_image(0,0 ,image=self.wallpaper, anchor="nw", tag="wallpaper")

        # create the grid system
        self.canvas.delete("grid")
        # set the values for the function parameters
        self.x1, self.x2 = float(self.entry_x1.get()), float(self.entry_x2.get())
        self.y1, self.y2 = float(self.entry_y1.get()), float(self.entry_y2.get())
        self.rx = self.cw / (self.x2 - self.x1)
        self.ry = self.ch / (self.y2 - self.y1)

        # draw the grid system in the canvas
        mrx, mry = self.return_grid_range(self.x1, self.x2), self.return_grid_range(self.y1, self.y2)
        # create the grid for y
        for i in range(0, int(self.x2 - self.x1)):
            if (self.x1 + i) % mrx == 0:
                self.canvas.create_line(i * self.rx, 0, i * self.rx, self.ch, fill="#323744", tag="grid",width="0.5")
        for j in range(0, int(self.y2 - self.y1)):
            if (j + self.y1) % mry == 0:
                self.canvas.create_line(0, self.ch - (j * self.ry), self.cw, self.ch - (self.ry * j), fill="#323744",tag="grid", width="0.5")

        # draw the x and y axis
        self.canvas.create_line(0, self.y2 * self.ry, self.cw, self.y2 * self.ry, fill="white", tag="grid")
        self.canvas.create_line(-self.x1 * self.rx, 0, -self.rx * self.x1, self.ch, fill="white", tag="grid")

        # update the range of scale widgets
        self.scale_infox.config(from_=self.x1, to=self.x2)
        self.scale_infoy.config(from_=self.y1, to=self.y2)
        self.scalex.config(from_=self.x1, to=self.x2)
        self.scaley.config(from_=self.y1, to=self.y2)

        # if partilces is being update the particles positions
        if len(self.static_particles) > 0:
            self.display_the_static_particles()

    def return_grid_range(self, x1, x2):
        if (x2-x1) <= 60:
            return 1
        elif (x2-x1) <= 120:
            return 2
        elif (x2-x1) <= 200:
            return 5
        else:
            return 10

    def set_pathcolor(self):
        self.path_color = colorchooser.askcolor()[0]

    def select_bgimage(self):
        # ask the file name for wallpaper
        self.wallpaper_path = filedialog.askopenfilename(title="background image",
                                                         filetypes=(("JPG files", "*.jpg"), ("PNG files", "*.png")))
        # load the wallpaper as image
        self.wallpaper = ImageTk.PhotoImage(Image.open(self.wallpaper_path).resize((int(self.cw), int(self.ch)), Image.ANTIALIAS))

        # create the image in the canvas
        self.canvas.delete("wallpaper")
        self.canvas.create_image(0, 0, image=self.wallpaper, anchor="nw", tag="wallpaper")
        # set the image to lower frame in the canvas
        self.canvas.lower("wallpaper")

    def update_scale_infox(self, x):
        # update the scale label for display the x value
        self.infox_label.config(text=f"{x}")
        # show the arrow position on the canvas
        self.canvas.delete("arrow")
        x, y = float(x), float(self.scale_infoy.get())
        px, py = (x-self.x1)*self.rx , self.ch-(y-self.y1)*self.ry
        self.canvas.create_line(px-5, py, px+5, py, fill="red", tag="arrow")
        self.canvas.create_line(px, py-5, px, py+5, fill="red", tag="arrow")

    def update_scale_infoy(self, y):
        # update the scale label for display the y value
        self.infoy_label.config(text=f"{y}")
        # show the arrow position on the canvas
        self.canvas.delete("arrow")
        x, y = float(self.scale_infox.get()), float(y)
        px, py = (x-self.x1)*self.rx , self.ch-(y-self.y1)*self.ry
        self.canvas.create_line(px-5, py, px+5, py, fill="red", tag="arrow")
        self.canvas.create_line(px, py-5, px, py+5, fill="red", tag="arrow")

    def insert_new_particle(self):
        # insert the particle info to main list as new particle
        if self.entry_charge.get():
            self.static_particles.append([float(self.scale_infox.get()), float(self.scale_infoy.get()), float(self.entry_charge.get())])
        # update the canvas
        self.display_the_static_particles()

    def display_the_static_particles(self):
        # first delete the all particle in the canvas
        self.delete_canvas_particles()
        i = 0
        for particle in self.static_particles:
            # draw the particle in the canvas
            self.canvas.create_oval((-self.x1+particle[0])*self.rx-self.R, self.ch+self.R-(-self.y1+particle[1])* self.ry, (-self.x1+particle[0])*self.rx+self.R, self.ch-self.R-(-self.y1+particle[1])*self.ry, outline="green2",fill="green2", width="1.5", tag=f"part{i}")
            if particle[2] > 0:
                self.canvas.create_text((-self.x1 + particle[0]) * self.rx, self.ch - (-self.y1 + particle[1]) * self.ry, text="+", fill="red",tag=f"part{i}", font=('vedana', 14))
            else:
                self.canvas.create_text((-self.x1 + particle[0]) * self.rx, self.ch - (-self.y1 + particle[1]) * self.ry, text="-", fill="red",tag=f"part{i}", font=('verdana', 14))
            i += 1

    def delete_canvas_particles(self):
        for i in range(0, len(self.static_particles)):
            self.canvas.delete(f"part{i}")
        self.canvas.delete("highlight_circle")

    def mouse_clicked(self, event):
        # run function selected particle
        self.selected_particle(self.canvas.canvasx(event.x), self.canvas.canvasy(event.y))

        # if self_current_direction_var is on run set_wire function
        self.set_wire(self.canvas.canvasx(event.x) , self.canvas.canvasy(event.y))

    def set_wire(self ,x ,y):
        # first delete previous wire
        self.canvas.delete("current_wire")
        # create the new wire in new position
        gr = math.tan(math.radians(float(self.angle_spinbox.get())))
        xa = x - (self.ch - y) / gr
        yb = y - gr * (self.cw - x)
        # insert the wire to current_wires_list
        self.current_wires.append([float(self.angle_spinbox.get()), (self.x1 + xa/self.rx)])
        # create the line for current wire
        self.canvas.create_line(xa, self.ch, self.cw, yb, fill="blue", width="2.0", tag=f"current_wire{len(self.current_wires)}")
        # set the self.current_wire_var to off
        self.current_wire_var.set(0)


    def selected_particle(self, x, y):
        # get the clicked object on the canvas
        clicked_object = self.canvas.find_closest(x, y)[0]
        # get the tag for this object
        clicked_tag = self.canvas.gettags(clicked_object)[0]
        # check the select tag have charge particle
        if clicked_tag[0:4] == "part":
            # get the id_num  of clicked particle
            self.clicked_id = int(clicked_tag[4:])
            # get the information list from the atoms list
            clicked_info = self.static_particles[self.clicked_id]
            # display the information in the frame
            self.id_label.config(text=f"ID : {self.clicked_id}")
            self.xy_label.config(text=f"X : {clicked_info[0]} | Y : {clicked_info[1]}")
            self.charge_label.config(text=f"Charge is {clicked_info[2]}")
            # highlight the selected charge particles
            self.canvas.delete("highlight_circle")
            self.canvas.create_oval((-self.x1+clicked_info[0])*self.rx-self.R2, self.ch+self.R2-(-self.y1+clicked_info[1])*self.ry,(-self.x1+clicked_info[0])*self.rx+self.R2, self.ch-self.R2-(-self.y1+clicked_info[1])*self.ry,
                               outline="yellow", fill=None, tag="highlight_circle")

    def rearrange_particles(self, id):
        new_list = []
        for i in range(0, len(self.static_particles)):
            if i != id:
                new_list.append(self.static_particles[i])
        print(new_list)
        return new_list

    def remove_particle(self):
        # rearrange the particle list by removing selected particle
        self.static_particles = self.rearrange_particles(self.clicked_id)
        # update the canvas by remove the selected particle
        self.display_the_static_particles()
        # set the clicked_id variable to False
        self.clicked_id = False

    def get_distance(self, static_particle, motion_particle):
        atom_x, atom_y = static_particle[0], static_particle[1]
        x, y = motion_particle["x"], motion_particle["y"]
        # calculate the distance among the atom and alpha particle
        d = math.sqrt(pow(x - atom_x, 2) + pow(y - atom_y, 2))
        # calculate the sin and cosines for directions
        sine = (y - atom_y) / d
        cosine = (x - atom_x) / d
        # return the distance sine and cosine as list
        return [d, sine, cosine]

    def create_path(self):
        # empty the plot lists
        self.plot_xdata = []
        self.plot_vdata = []
        # get the value for motioned particle in the program
        self.motion_particle = {
            "x" : float(self.scalex.get()),
            "y" : float(self.scaley.get()),
            "vx" : float(self.scale_vx.get()),
            "vy" : float(self.scale_vy.get()),
            "q" : self.moveQ,
            "m" : self.moveM,
        }
        t = 0
        self.start_stop_var.set("start")
        # start the while loop for display the path of particle
        while self.start_stop_var.get() == "start":
            t += self.dt
            # get the  initial conditions of the particle
            org_x ,org_y = self.motion_particle["x"], self.motion_particle["y"]
            # create the acceration variables to x,y direction
            a_x = 0
            a_y = 0
            # collect the accerelation of static particles
            for particle in self.static_particles:
                info = self.get_distance(particle, self.motion_particle)
                a = self.k * self.motion_particle["q"] * particle[2] / (info[0] ** 2 * self.motion_particle["m"])
                a_x += a * info[2]
                a_y += a * info[1]

            # update the motion_particle info
            # set the alpha particle velocities
            self.motion_particle["vx"] += a_x * self.dt
            self.motion_particle["vy"] += a_y * self.dt

            # set the alpha particle (x,y) positions
            self.motion_particle["x"] += self.motion_particle["vx"] * self.dt
            self.motion_particle["y"] += self.motion_particle["vy"] * self.dt

            # update the canvas by new alpha particles positions
            self.canvas.delete("particle")
            self.canvas.create_oval((self.motion_particle["x"] - self.x1) * self.rx - 2, (self.ch - (self.motion_particle["y"] - self.y1) * self.ry) - 2,
                                   (self.motion_particle["x"] - self.x1) * self.rx + 2, (self.ch - (self.motion_particle["y"] - self.y1) * self.ry) + 2, fill="red",outline="red", tag="particle")

            self.canvas.create_line((org_x - self.x1) * self.rx, self.ch - (org_y - self.y1) * self.ry, (self.motion_particle["x"] - self.x1) * self.rx,self.ch - (self.motion_particle["y"] - self.y1) * self.ry, fill=self.path_color, width="0.5", tag="path")
            # check the if plot var is the on and collect data for plotting
            self.checkplotandcollect(t)
            # canvas update after 0.005s
            self.canvas.update()
            self.canvas.after(int(self.dt*1000))

    def motion_particle_x(self, x):
        # show the value in the label
        self.label_x.config(text=f"{x}")
        # show the arrow position on the canvas
        self.canvas.delete("particle_position")
        x, y = float(x), float(self.scaley.get())
        px, py = (x - self.x1) * self.rx, self.ch - (y - self.y1) * self.ry
        self.canvas.create_line(px - 10, py, px + 10, py, fill="green2", tag="particle_position")
        self.canvas.create_line(px, py - 10, px, py + 10, fill="green2", tag="particle_position")

    def motion_particle_y(self, y):
        # show the value in the label
        self.label_y.config(text=f"{y}")
        # show the arrow position on the canvas
        self.canvas.delete("particle_position")
        x, y = float(self.scalex.get()), float(y)
        px, py = (x-self.x1)*self.rx , self.ch-(y-self.y1)*self.ry
        self.canvas.create_line(px-10, py, px+10, py, fill="green2", tag="particle_position")
        self.canvas.create_line(px, py-10, px, py+10, fill="green2", tag="particle_position")

    def display_vx(self, vx):
        # display the velocity x in the label
        self.label_vx.config(text=f"{vx}")
        # display the velocity in the velocity screen
        vx, vy = float(vx), float(self.scale_vy.get())
        # display the info in the canvas
        self.display_velocity_and_info(vx, vy)


    def display_vy(self, vy):
        # display the velocity y in the label
        self.label_vy.config(text=f"{vy}")
        # display the velocity in the velocity screen
        vx, vy = float(self.scale_vx.get()), float(vy)
        # display the info in the canvas
        self.display_velocity_and_info(vx, vy)

    def return_angle(self, sin, cos):
        if sin >= 0 and cos >= 0:
            return math.degrees(math.acos(cos))
        elif sin >= 0 and cos < 0:
            return math.degrees(math.acos(cos))
        elif sin < 0 and cos < 0:
            return 180 + math.degrees(math.acos(abs(cos)))
        else:
            return 360 + math.degrees(math.asin(sin))

    def  display_velocity_and_info(self, vx, vy):
        v = math.sqrt(vx**2 + vy**2)
        l = 50
        lx, ly = self.wv / 2 + l * vx / v, self.hv / 2 - l * vy / v
        # create the velocity line in the canvas
        self.canvas_v.delete("velocity_marker")
        self.canvas_v.create_line(self.wv / 2, self.hv / 2, lx, ly, fill="green2", tag="velocity_marker", cap=ROUND,
                                  width="2.0", arrow="last")
        # create the text about the velocity
        velocity_text = f"v  = {round(v,3)}\n" \
                        f"vx = {vx}\n" \
                        f"vy = {vy}"
        self.canvas_v.create_text(self.wv / 2, 40, text=velocity_text, fill="yellow", font=('verdana', 10),
                                  tag="velocity_marker")
        # display the angle in the canvas
        angle = self.return_angle(vy/v , vx/v)
        self.canvas_v.create_text(self.wv/2, 130 ,text=f"angle  = {round(angle , 2)}", tag="velocity_marker", fill="red", font=('verdana', 10))

    def new_frame(self):
        # claer the canvas by the particles
        self.canvas.delete(ALL)
        self.update_canvas_grid()
        # set the static particle list is the empty
        self.static_particles = []

    def set_qandm(self):
        # create the top level window
        self.top_info = Toplevel(self, bg="black")
        self.top_info.geometry("320x150+250+250")
        self.top_info.overrideredirect(True)

        Label(self.top_info, text="charge", bg="black", fg="white").grid(row=0, column=0)
        Label(self.top_info, text="mass", bg="black", fg="white").grid(row=1, column=0)
        self.entry_infocharge = Entry(self.top_info, bd=0, bg="#323744", fg="white", width="25", font=('verdana', 12))
        self.entry_infocharge.grid(row=0, column=1, padx=5, pady=10)

        self.entry_infomass = Entry(self.top_info, bd=0, bg="#323744", fg="white", width="25", font=('verdana', 12))
        self.entry_infomass.grid(row=1, column=1, padx=5)
        self.entry_infocharge.insert(0, self.moveQ)
        self.entry_infomass.insert(0, self.moveM)

        Button(self.top_info, text="ok", bd=0, bg="#1e1f21", fg="white", font=('Helvetica', 11), width="8", command=self.collect_data_move).grid(row=2, column=0, columnspan=2, sticky=EW, pady=20, padx=10)

    def collect_data_move(self):
        try:
            # set the charge and mass to given values
            self.moveQ = float(self.entry_infocharge.get())
            self.moveM = float(self.entry_infomass.get())
            # destroy the top level window
            self.top_info.destroy()
        except:
            messagebox.showwarning(title="data type error", message="please insert the valid data types!")

    def create_plotframe(self):
        self.plot_frame = Frame(self, bg="black")
        self.plot_frame.grid(row=0, column=1)

        # button for the change frame
        Button(self.plot_frame, text="<", bd=0, fg="white",bg="#1e1f21", command=lambda e=1:self.change_frame(e),  width="10").grid(row=0, column=0, sticky=EW)
        # frame for plottings
        self.vxplot_frame = LabelFrame(self.plot_frame, bg="black", width="20", text="plot", fg="white", bd=1)
        self.vxplot_frame.grid(row=1, column=0, padx=0)
        # tk variablr for plot velocity and positions
        self.plot_v = IntVar()
        self.plot_x = IntVar()
        # checkbutton for append the variable
        Checkbutton(self.vxplot_frame, text="plot of x", bd=0, width="20", bg="black", fg="white", variable=self.plot_x).grid(row=0, column=0)
        Checkbutton(self.vxplot_frame, text="plot of v", bd=0, width="20",bg="black", fg="white", variable=self.plot_v).grid(row=1, column=0)

        Button(self.vxplot_frame, text="plot of x", bd=0, bg="green2", width="20", command=self.plot_positionx).grid(row=2, column=0, pady=5)
        Button(self.vxplot_frame, text="plot of v" , bd=0, bg="green2", width="20").grid(row=3, column=0, pady=5)

        # create the magenetic field frame
        self.wire_frame = LabelFrame(self.plot_frame, text="current wire creater", fg="white", bg="black", bd=1)
        self.wire_frame.grid(row=2, column=0, pady=5)

        Label(self.wire_frame, text="angle/degree", bg="black", fg="white").grid(row=0, column=0, padx=5)
        self.angle_spinbox = ttk.Spinbox(self.wire_frame, from_=0, to=180, width="7")
        self.angle_spinbox.grid(row=0, column=1)
        Label(self.wire_frame, text="direction", bg="black", fg="white").grid(row=1, column=0, padx=5)
        self.current_direction = StringVar()
        self.current_direction_get = ttk.Combobox(self.wire_frame, width="8", textvariable=self.current_direction, state="readonly")
        self.current_direction_get.grid(row=1, column=1)
        self.current_direction_get['values'] = ["top", "bottom"]

        self.initial_position_cw = Entry(self.wire_frame, bd=0, bg="green2", font=('Helvetica', 12), width="7")
        self.initial_position_cw.grid(row=2, column=0, columnspan=2, pady=3)

        # defined the variable to create the wire
        self.current_wire_var = IntVar()
        Button(self.wire_frame, text="create the wire", bg="purple", font=('Helvetica', 11), bd=0, command=lambda :self.current_wire_var.set(1)).grid(row=3, column=0, columnspan=2, padx=5, sticky=EW, pady=5)

        # frame for the electric field regions
        self.frame_elecregion = LabelFrame(self.plot_frame, text="electrric fields", fg="white", bg="black", bd=1)
        self.frame_elecregion.grid(row=3, column=0, pady=5, padx=5)

        # components of electric field frame
        Label(self.frame_elecregion, text="E of x direction", bg="black", fg="white").grid(row=0, column=0, padx=0, pady=2)
        Label(self.frame_elecregion, text="E of y direction", bg="black", fg="white").grid(row=1, column=0, padx=0,pady=2)
        # entry box for ex and ey
        self.entryEx = Entry(self.frame_elecregion, bd=0, bg="orange", font=('Helvetica', 12), width="15")
        self.entryEx.grid(row=0, column=1, pady=5, columnspan=2, padx=3)
        self.entryEy = Entry(self.frame_elecregion, bd=0, bg="orange", font=('Helvetica', 12), width="15")
        self.entryEy.grid(row=1, column=1, pady=5, columnspan=2, padx=3)
        # spin box for get region
        Label(self.frame_elecregion, text="region", bg="black", fg="white").grid(row=3, column=0, padx=3, pady=5)

        self.spinEx1 = ttk.Spinbox(self.frame_elecregion, from_=self.x1, to=self.x2, width="5")
        self.spinEx1.grid(row=3, column=1)
        self.spinEx2 = ttk.Spinbox(self.frame_elecregion, from_=self.x1, to=self.x2, width="5")
        self.spinEx2.grid(row=3, column=2)
        self.spinEy1 = ttk.Spinbox(self.frame_elecregion, from_=self.y1, to=self.y2, width="5")
        self.spinEy1.grid(row=4, column=1)
        self.spinEy2 = ttk.Spinbox(self.frame_elecregion, from_=self.y1, to=self.y2, width="5")
        self.spinEy2.grid(row=4, column=2)
        # button to view the region
        Button(self.frame_elecregion, text="view", bg="green2", bd=0, font=('Helvetica', 12)).grid(row=5, column=1, pady=2 ,columnspan=2,sticky=EW)

        ttk.Separator(self.frame_elecregion, orient=HORIZONTAL).grid(row=6, column=0, columnspan=3, pady=3, sticky=EW)

        Label(self.frame_elecregion, text="E", bg="black", fg="white").grid(row=7, column=0, sticky=EW)
        Label(self.frame_elecregion, text="angle", bg="black", fg="white").grid(row=7, column=1, columnspan=2)

        self.entryE = Entry(self.frame_elecregion, bd=0, bg="orange", font=('Helvetica', 12), width="8")
        self.entryE.grid(row=8, column=0, sticky=EW)
        self.angleE = ttk.Spinbox(self.frame_elecregion, from_=0, to=360, width="13")
        self.angleE.grid(row=8, column=1, columnspan=2)
        # first ex, ey insert 0
        self.entryEx.insert(0, 0)
        self.entryEy.insert(0, 0)

        # first grid forget the plot frame
        self.plot_frame.grid_forget()


    def change_frame(self, i):
        if i:
            self.frame_main.grid(row=0, column=1)
            self.plot_frame.grid_forget()
        else:
            self.frame_main.grid_forget()
            self.plot_frame.grid(row=0, column=1)

    def checkplotandcollect(self, t):
        # first check the x plot
        if self.plot_x.get():
            self.plot_xdata.append([t , self.motion_particle["x"]])
        if self.plot_v.get():
            self.plot_vdata.append([t, self.motion_particle["vx"]])

    def plot_positionx(self):
        # create the top level window
        self.plotx_window = Toplevel(self)
        self.plotx_window.config(bg="black")
        # create the canvas
        canvas_plotx = Canvas(self.plotx_window, width="700", height="500", bd=0, bg="#323744", highlightthickness=0)
        canvas_plotx.grid(row=0, column=0)

        # rearrange the lists
        new_xt = []
        for i in self.plot_xdata:
            new_xt.append(i[0]*100)
            new_xt.append(250-i[1]*10)
        canvas_plotx.create_line(new_xt, smooth=True, fill="red", width="0.5", cap=ROUND)

    def setEandangle(self, i):
        Ex , Ey = float(self.entryEx.get()), float(self.entryEy.get())
        # calculate the result E
        E = math.sqrt(Ex**2 + Ey**2)
        # insert the E in the correct entry box
        self.entryE.delete(0, END)
        self.entryE.insert(0, round(E, 4))

def main():
    path_creator().mainloop()

if __name__ == "__main__":
    main()
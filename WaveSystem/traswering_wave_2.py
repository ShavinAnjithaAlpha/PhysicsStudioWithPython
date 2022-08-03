from tkinter import *
from tkinter import ttk
import math
from function_value import get_function_only
from derivative_cofficient import derivative_cofficient

root = Tk()
root.title("Waves creator -ShavMind Produnction ")
root.config(bg="#1e1f21")

start_stop = StringVar()
start_stop.set("start")
global wave_function
wave_function = []

def calculate_y(function, x, a):
    y = 0
    for f in function:
        if f[1] == "sin":
            y += f[0]*math.sin(derivative_cofficient([f[2], x, 0]) + a)
        else:
            y += f[0] * math.cos(derivative_cofficient([f[2], x, 0]) + a)

    return y

def draw_wave_graph2(xf, a, calc_function):
    global wave_function
    # remove the old wave line from the canvas
    canvas.delete("wave")
    i = 0.2
    global xr
    xr = 15
    num_of_x = w / xr
    x = 0
    # insert xf  value in the boxes
    ent_x.delete(0, END)
    ent_x.insert(0, round(xf, 2))
    if not (xf >= num_of_x):
        # create empty list for the storage point(x, y) data
        x_and_y = [0, h/2]
        while x <= xf:
            x += i
            # claculate the y value fro the x value
            y1 = calculate_y(wave_function, x, a)
            # append the x and y1 value to the list as point coordinates
            x_and_y.append(x* xr)
            x_and_y.append(h/2 - y1)
        # draw the wavw line used the x_and_y list
        canvas.create_line(x_and_y, fill="red", width="1.2", tag="wave", smooth=True, capstyle=ROUND)
    else:
        # create the list for the storage point (x, y) data
        x_and_y = [0, h/2]
        while x <= num_of_x:
            x += i
            # calculate the  y claue from the x value
            y1 = calculate_y(wave_function ,x, a)
            # append the x and y1 value to the list as point coordinates
            x_and_y.append(x* xr)
            x_and_y.append(h/2- y1)
        # draw the wave used the x_and_y list
        canvas.create_line(x_and_y, fill="red", width="1.2", tag="wave", smooth=True)
        
def draw_wave_graph(xf, a, A):
    canvas.delete("wave")
    i = 0.1
    xr = 15
    num_of_x = w / xr
    x = 0
    sinef = entry_sinfunc1.get()
    cosf  = entry_sinfunc2.get()
    if not (xf >= num_of_x):
        while x <= xf:
            x += i
            y1 = A[0] * pow(math.sin(derivative_cofficient([sinef, x, 0])+a), A[2]) + A[1] * pow(math.sin(derivative_cofficient([cosf, x, 0])+ a), A[3])
            y2 = A[0] * pow(math.sin(derivative_cofficient([sinef, x-i, 0])+a ), A[2]) + A[1] * pow(math.sin(derivative_cofficient([cosf, x-i, 0])+ a), A[3])
            canvas.create_line(x * xr, h / 2 - y1, (x - i) * xr, h / 2 - y2, fill="red", width="1.5", tag="wave", capstyle=ROUND)
    else:
        while x <= num_of_x:
            x += i
            y1 = A[0] * pow(math.sin(derivative_cofficient([sinef, x, 0]) + a), 1) + A[1] * pow(
                math.cos(derivative_cofficient([cosf, x, 0]) + a), 3)
            y2 = A[0] * pow(math.sin(derivative_cofficient([sinef, x - i, 0]) + a), 1) + A[1] * pow(
                math.cos(derivative_cofficient([cosf, x - i, 0]) + a), 3)
            canvas.create_line(x * xr, h / 2 - y1, (x - i) * xr, h / 2 - y2, fill="red", width="1.5", tag="wave")


def start():
    start_stop.set("start")
    v = float(ent_v.get())
    t = 0
    dt = 0.005
    alpha = 0
    k = float(entry_k.get())
    #identify the sin and cosine function's amplitudes
    wave_function = entry_function.get()
    calc_function = get_function_only(wave_function)
    x = 0
    while True:
        if start_stop.get() == "stop":
            break
        draw_wave_graph2(x, alpha, calc_function)
        t += dt
        # insert time value in the time box
        ent_time.delete(0, END)
        ent_time.insert(0, round(t, 2))
        x += v * dt
        alpha += k
        canvas.update()
        canvas.after(5)

def draw_xy_rulers():
    global xr
    xr = 15
    # draw the x ruler
    for i in range(0, int(w/xr)):
        if (i%10  == 0):
            canvas.create_line(i* xr, 0, i*xr, 20, fill="white")
            canvas.create_text(i*xr, 28, text=i, font=('verdana', 10), fill="white")
        elif (i%5 == 0):
            canvas.create_line(i*xr, 0, i*xr, 15, fill="white")
        else:
            canvas.create_line(i*xr, 0, i*xr, 10, fill="white")

def add_function():
    global wave_function
    function = get_function_only(entry_function.get())
    wave_function.append([float(entry_amp.get()), function_type.get(), function])

    # display the function in the canvas_eq
    # first create the wave equation string
    wave_eq_text = "y(x) = "
    for item in wave_function:
        if wave_function.index(item) != 0:
            wave_eq_text += f" + {item[0]}*{function_type.get()}({function})"
        else:
            wave_eq_text += f"{item[0]}*{function_type.get()}({function})"

    # dispaly the function text in the canvas
    canvas_eq.delete("wave_eq")
    canvas_eq.create_text(w/2, 25, text=wave_eq_text, fill="#545a56", font=('Helvetica', 18), tag="wave_eq")


w = 900
h = 400
canvas = Canvas(root, width=w, height=h, bg="#262c3d", bd=0, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=3)

# draw the middle line in the canvas
canvas.create_line(0, h/2, w, h/2, fill="orange", width="2")
# draw the x and y ruler
draw_xy_rulers()

# create the other canvas for display the wave equation
canvas_eq = Canvas(root, width=w, height=50, bg="#323744", bd=0, highlightthickness=0)
canvas_eq.grid(row=1, column=0, columnspan=3)

frame_1 = LabelFrame(root, text="source", bg="#1e1f21", fg="white", bd=1)
frame_1.grid(row=2, column=0, ipadx=15)

Button(frame_1, text="start", bg="black", fg="white", relief=FLAT, width="20", \
       bd=0 ,command=start).grid(row=0, column=0, pady=2, columnspan=3, padx=5, sticky=EW)
Button(frame_1, text="stop", bg="black", fg="white", relief=FLAT, width="20", \
       bd=0 ,command=lambda: start_stop.set("stop")).grid(row=1, column=0, columnspan=3, sticky=EW, padx=5)

Label(frame_1, text="wave speed", bg="#1e1f21", fg="white").grid(row=2, column=0)
Label(frame_1, text="k", bg="#1e1f21", fg="white").grid(row=3, column=0)
Label(frame_1, text="amplitude", bg="#1e1f21", fg="white").grid(row=4, column=0)
Label(frame_1, text="tri type", bg="#1e1f21", fg="white").grid(row=4, column=1)
Label(frame_1, text="function", bg="#1e1f21", fg="white").grid(row=4, column=2)

ent_v = Entry(frame_1, relief=FLAT, font=('verdana', 10), bg="#2b2f2f", fg="white", width="15")
ent_v.grid(row=2, column=1, columnspan=2)
ent_v.focus()

entry_k = Entry(frame_1, bd=0, bg="#474c49", fg="white", width="15", font=('Helvetica', 11))
entry_k.grid(row=3, column=1, columnspan=2)

entry_amp = Entry(frame_1, bd=0, fg="white", bg="#2b2f2f", font=('Helveica', 11), width="5")
entry_amp.grid(row=5, column=0, sticky=EW, padx=2)


function_type = StringVar()
tri_type = ttk.Combobox(frame_1, width="10", textvariable=function_type)
tri_type["values"] = ["sin", "cos"]
tri_type.grid(row=5, column=1, padx=2)

entry_function = Entry(frame_1, bd=0, bg="#535a56", font=('Helveica', 11), fg="white")
entry_function.grid(row=5, column=2, sticky=EW, padx=2, pady=3)

add_btn = Button(frame_1, text="Add", bd=0, width="10", bg="#0fef63", command=add_function)
add_btn.grid(row=5, column=3, padx=5)


ent_v.bind("<Return>", lambda e:entry_k.focus())
entry_k.bind("<Return>", lambda e:entry_amp.focus())
entry_amp.bind("<Return>", lambda e: tri_type.focus())
tri_type.bind("<Return>", lambda e:entry_function.focus())
entry_function.bind("<Return>", lambda e:add_btn.focus())

# function to the draw the standing wave
def draw_stand_wave_graph(A):
    canvas.delete("wave")
    i, xr = 0.5, 50
    w_lambda = xr/float(ent_length.get())
    xf = math.pi * int(ent_nodes.get())/w_lambda
    x = 0
    x_and_y = []
    while x <= xf + i/2:
        y1 = A * pow(math.sin(w_lambda * x), 1)
        x_and_y.append(x* xr)
        x_and_y.append(h/2 - y1)
        x += i
    canvas.create_line(x_and_y, fill="red", tag="wave", smooth=True, width="1.5")


def start2():
    start_stop.set("start")
    f = float(ent_fs.get())
    dt = 0.01
    amp = float(ent_as.get())
    ak = 2 * math.pi * f * dt
    A = amp
    t = 0
    while True:
        if start_stop.get() == "stop":
            break
        draw_stand_wave_graph(A)
        A = amp * math.cos(t * f)
        t += 0.1
        canvas.update()
        canvas.after(10)


frame_2 = LabelFrame(root, text="standing wave", bg="#1e1f21", fg="white", bd=1)
frame_2.grid(row=2, column=1, ipadx=7, ipady=15)

Button(frame_2, text="start", bg="black", fg="white", relief=FLAT, width="10", \
       command=start2).grid(row=0, column=0, pady=2, columnspan=2, sticky=EW, padx=5)
Button(frame_2, text="stop", bg="black", fg="white", relief=FLAT, width="10", \
       command=lambda: start_stop.set("stop")).grid(row=1, column=0, columnspan=2, sticky=EW, padx=5)

Label(frame_2, text="frequency", bg="#1e1f21", fg="white").grid(row=3, column=0)
Label(frame_2, text="amplitude", bg="#1e1f21", fg="white").grid(row=4, column=0)
Label(frame_2, text="Number of Nodes", bg="#1e1f21", fg="white").grid(row=5, column=0)
Label(frame_2, text="wave length", bg="#1e1f21", fg="white").grid(row=6, column=0)

# entry boc for get standing wave frequency
ent_fs = Entry(frame_2, bd=0)
ent_fs.grid(row=3, column=1)
# entry box for get the standing wave amolitude
ent_as = Entry(frame_2, bd=0)
ent_as.grid(row=4, column=1)
# entry box for get the number of nodes
ent_nodes = Entry(frame_2, bd=0)
ent_nodes.grid(row=5, column=1)
ent_nodes.insert(0, 2)
# entry box for get the wave length
ent_length = Entry(frame_2, bd=0)
ent_length.grid(row=6, column=1)


# frame of the x. y and time parameter presented
frame_xyt = LabelFrame(root, text="x,y and time", fg="white", bg="#1e1f21", bd=1)
frame_xyt.grid(row=2, column=2, ipadx=7, ipady=25)

Label(frame_xyt, text="X :", bg="#1e1f21", font=('verdana', 9), fg="white").grid(row=0, column=0)
Label(frame_xyt, text="Y :", bg="#1e1f21", font=('verdana', 9), fg="white").grid(row=0, column=2)
Label(frame_xyt, text="time ", bg="#1e1f21", font=('verdana', 9), fg="white").grid(row=1, column=0)

ent_x = Entry(frame_xyt, relief=FLAT, bg="black", fg="white", width="10", font=('Helvetica', 11))
ent_y = Entry(frame_xyt, relief=FLAT, fg="white", bg="black", width="10", font=(':Helvetica', 11))
ent_time = Entry(frame_xyt, relief=FLAT ,fg="white", bg="black", width="10", font=('Helvetica', 11))

ent_x.grid(row=0, column=1)
ent_y.grid(row=0, column=3)
ent_time.grid(row=1, column=1, pady=5)


root.mainloop()
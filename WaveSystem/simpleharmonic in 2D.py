from tkinter import*
import math


root = Tk()
root.title("Simple Harmonic Oscilation in 2D")
root.config(bg="black")

w = 600
h = 500
hx = 500
h_display = 100
rx = 10
ryg = 10
dy2 = h/(2*ryg)
rx2 = 10
dx1 = -w/(rx*2)
ry = 10
ryv = 0.5
ryv5 = 10
t = float()
state_var = StringVar()
state_var.set("start")

canvas_frame = Frame(root, bg="black")
canvas_frame.grid(row=0, column=0)
canvas_1 = Canvas(canvas_frame, width=w, height=h, bg="#262c3d", relief=FLAT, bd=0, highlightthickness=0)
canvas_1.grid(row=0, column=0, pady="2")

canvas_2 = Canvas(canvas_frame, width=w, height=h_display, scrollregion=(0 ,0, w, hx),bg="#262c3d", relief=FLAT, bd=0, highlightthickness=0)
canvas_2.grid(row=1, column=0)
# set the scroll bar to the canvas_2
scroll_y2 = Scrollbar(canvas_frame, orient=VERTICAL, command=canvas_2.yview)
scroll_y2.grid(row=1, column=1, sticky=NS)

canvas_3 = Canvas(canvas_frame, width=w, height=h_display, scrollregion=(0 ,0, w, hx), bg="#262c3d", relief=FLAT, bd=0, highlightthickness=0)
canvas_3.grid(row=2, column=0, pady=5)
# set the scroll bar to the canvas_2
scroll_y3 = Scrollbar(canvas_frame, orient=VERTICAL, command=canvas_3.yview)
scroll_y3.grid(row=2, column=1, sticky=NS)

# bind the scroll var to the canvases
canvas_2.config(yscrollcommand=scroll_y2.set)
canvas_3.config(yscrollcommand=scroll_y3.set)

def setruler(event):
    canvas_1.delete("rulerlinex", "rulertextx", "rulerliney", "rulertexty")
    canvas_1.create_line(event.x,0,event.x,h,fill="orange", width="0.5",tag="rulerlinex", dash=(3, 3))
    canvas_1.create_line(0,event.y,w,event.y,tag="rulerliney",fill="orange", dash=(3 ,3))
    rulertextx=str((event.x+dx1*rx)/rx)
    rulertexty=str((h/2-event.y)/ryg)
    canvas_1.create_text(event.x,20,text=rulertextx,font=("verdana",8),fill="white",tag="rulertextx")
    canvas_1.create_text(20,event.y,text=rulertexty,font=("verdana",8),fill="white",tag="rulertexty")

def setrulerx(event):
    canvas_2.delete("rulerlinex","rulertextx","rulerxy","textx")
    canvas_2.create_line(event.x,0,event.x,hx,fill="red",width="0.5",tag="rulerlinex")
    canvas_2.create_line(0,event.y,w,event.y,tag="rulerxy",fill="red")
    canvas_3.delete("rulerlinev","rulertextv")
    canvas_3.create_line(event.x,0,event.x,hx,fill="red",width="0.5",tag="rulerlinev")
    rulertextx=str((event.x)/rx2)
    textx=str((hx/2-event.y)/ry)
    canvas_2.create_text(event.x,20,text=rulertextx,font=("verdana",8),fill="white",tag="rulertextx")
    canvas_2.create_text(650,event.y,text=textx,font=("verdana",8),fill="white",tag="textx")

def setrulerv(event):
    canvas_2.delete("rulerlinex","rulertextx")
    canvas_2.create_line(event.x,0,event.x,hx,fill="red",width="0.5",tag="rulerlinex")
    canvas_3.delete("rulerlinev","rulertextv","rulerxy","textv")
    canvas_3.create_line(event.x,0,event.x,hx,fill="red",width="0.5",tag="rulerlinev")
    canvas_3.create_line(0,event.y,w,event.y,tag="rulerxy",fill="red")
    rulertextx=str((event.x)/rx2)
    textv=str((hx/2-event.y)/ryv)
    canvas_2.create_text(event.x,20,text=rulertextx,font=("verdana",8),fill="white",tag="rulertextx")
    canvas_3.create_text(650,event.y,text=textv,font=("verdana",8),fill="white",tag="textv")

def setvar():
    if state_var.get()=="start":
        state_var.set("stop")


def startanim():
    state_var.set("start")
    canvas_2.delete("graphx")
    canvas_3.delete("graphv")
    canvas_1.delete("path")
    org_vx = float(entryvx.get())
    org_vy = float(entryvy.get())
    x = float(entryx.get())
    y = float(entryy.get())
    ox = float(entryx.get())
    oy = float(entryy.get())
    vx = org_vx
    vy = org_vy
    org_yx = hx/2-x*ry
    org_yv = hx/2-vx*ryv
    t = 0
    kx = float(entrykx.get())
    ky = float(entryky.get())
    org_x = t*rx2
    f = float(entrykx.get())
    
    while True:
        if state_var.get() == "stop":
            break
        # calculate the accerlerations
        ax = -kx*x
        ay = -ky*y
        # calculate the current velocities
        vx = vx + ax*0.005
        vy = vy + ay*0.005
        # calculate the current position displacement
        x = x + vx*0.005
        y = y + vy*0.005
        # time up by 0.01 second
        t += 0.005
        
        cx = (-dx1+x)*rx
        cy = (dy2-y)*ryg
        canvas_1.delete("object")
        canvas_2.delete("time")
        # create the path on the canvas
        canvas_1.create_oval(cx-4, cy-4, cx+4, cy+4, fill="green2", tag="object", outline="green2")
        canvas_1.create_line((-dx1+ox)*rx, (dy2-oy)*ryg, cx, cy,fill="red",tag="path", width="1.5")
        canvas_2.create_text(650, 30, text=("t="+str(round(t,2))),font=('verdana',10),fill="white",tag="time")
        
        ox = x
        oy = y
        canvas_2.create_line(org_x,org_yx,t*rx2,hx/2-x*ry,fill="blue",width="0.5",tag="graphx")
        canvas_3.create_line(org_x,org_yv,t*rx2,hx/2-vx*ryv,fill="red",width="0.2",tag="graphv")
        org_yx = hx/2 - x*ry
        org_x = t*rx2
        org_yv = hx/2 - vx*ryv
        
        canvas_1.update()
        # canvas_1.after(10)

framemain = LabelFrame(root, bg="black", bd=1, text="parameters", fg="white")
framemain.grid(row=0, column=1, padx=10)
# label for dislay the parameter types
Label(framemain, text="velocity  X",width="15", bg="black", fg="white", anchor="e").grid(row=0,column=1)
Label(framemain, text="          Y",width="15", bg="black", fg="white", anchor="e").grid(row=1,column=1)
Label(framemain, text="acc. cofficient  X", width="15", bg="black", fg="white", anchor="e").grid(row=2,column=1)
Label(framemain, text="                 Y", width="15", bg="black", fg="white", anchor="e").grid(row=3,column=1)
Label(framemain, text="initial position  X", width="15", bg="black", fg="white", anchor="e").grid(row=4,column=1)
Label(framemain, text="                  Y", width="15", bg="black", fg="white", anchor="e").grid(row=5,column=1)

# entry boxes fo rget the initial velocity components 
entryvx = Entry(framemain, width="10", fg="black", bd=0, font=('verdana',10))
entryvx.grid(row=0, column=2, pady=2)
entryvx.insert(0, "0")
entryvy = Entry(framemain, width="10", fg="black", relief=FLAT, font=('verdana',10))
entryvy.grid(row=1, column=2, pady=2)
entryvy.insert(0, "30")
# entr boxes for get the k values for both x and y motions
entrykx = Entry(framemain, width="10", fg="black", relief=FLAT, font=('verdana',10))
entrykx.grid(row=2, column=2, pady=2)
entryky = Entry(framemain, width="10", fg="black", relief=FLAT, font=('verdana',10))
entryky.grid(row=3, column=2, pady=2)
entrykx.insert(0, 10)
entryky.insert(0, 10)
# entry boxes for get the initial x and y positions
entryx = Entry(framemain, width="10", fg="black", relief=FLAT, font=('verdana',10))
entryx.grid(row=4, column=2, pady=2)
entryx.insert(0, 0)
entryy = Entry(framemain, width="10", fg="black", relief=FLAT, font=('verdana',10))
entryy.grid(row=5, column=2, padx=3, pady=2)
entryy.insert(0, 0)

# buttons for start and the stop the motion
Button(framemain, text="start", bg="purple", fg="white", font=('verdana',10), relief=FLAT, command=startanim).grid(row=6, column=1, columnspan=2, sticky=EW, padx=3)
Button(framemain, text="stop", bg="red", fg="white", font=('verdana',10), relief=FLAT, command=setvar).grid(row=7, column=1, columnspan=2, sticky=EW, padx=3, pady=3)

# create gris in the canvas_1
for i1 in range(0, int(w/rx)):
    canvas_1.create_line(i1*rx,0,i1*rx,h, fill="#323744", width="0.5")
for j1 in range(0, int(h/ry)):
    canvas_1.create_line(0, j1*ry, w, j1*ry, fill="#323744", width="0.5")
# create grid in hte canvas_2
for i5 in range(0, int(w/rx)):
    canvas_2.create_line(i5*rx, 0, i5*rx, h, fill="#323744", width="0.5")
for i3 in range(0,int(hx/ry)):
    canvas_2.create_line(0,i3*ry,w,i3*ry,fill="#323744",width="0.5")
# create grid in the canvas_3
for i4 in range(0,int(hx/ryv5)):
    canvas_3.create_line(0,i4*ryv5,w,i4*ryv5,fill="#323744",width="0.5")
for i6 in range(0, int(w/rx)):
    canvas_3.create_line(i6*rx, 0, i6*rx, h, fill="#323744", width="0.5")

canvas_1.create_line(0, h/2, w, h/2, fill="white", width="1")
canvas_1.create_oval(w/2-4, h/2-4, w/2+4, h/2+4, fill="red", tag="object")

canvas_2.create_line(0, hx/2 ,w, hx/2, fill="white", width="1")
canvas_3.create_line(0, hx/2, w, hx/2, fill="white", width="1")
canvas_1.create_line(w/2, h/2-10, w/2, h/2+10, fill="white", width="1")

for i2 in range(0,int(w/rx)):
    canvas_1.create_line(i2*rx, 0, i2*rx, 6, fill="silver")
    if (i2/5) == int(i2/5):
        canvas_1.create_line(i2*rx, 0, i2*rx, 13,fill="silver")

for i5 in range(0,int(h/ryg)):
    canvas_1.create_line(0, i5*ryg, 6, i5*ryg, fill="silver")
    if (i5/5) == int(i5/5):
        canvas_1.create_line(0, i5*ryg, 13, i5*ryg, fill="silver")

canvas_1.bind("<Motion>",setruler)
canvas_2.bind("<Motion>",setrulerx)
canvas_3.bind("<Motion>",setrulerv)


root.mainloop()

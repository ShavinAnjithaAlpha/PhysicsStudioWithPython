from tkinter import*
import math

root=Tk()
root.title("Waves")
root.config(bg="black")

start_stop=StringVar()
start_stop.set("start")

def draw_wave_graph(xf,a,A):
    canvas.delete("wave")
    i=0.1
    xr=15
    num_of_x = w/xr
    x=0
    if not(xf >= num_of_x):
        while x<=xf:
            x+=i
            y1=A*pow(math.sin(x+a),1)+A*pow(math.cos(x+a),3)
            y2=A*pow(math.sin(x+a-i),1)+A*pow(math.cos(x+a-i),3)
            canvas.create_line(x*xr,h/2-y1,(x-i)*xr,h/2-y2,fill="red",tag="wave")
    else:
        while x <= num_of_x:
            x+=i
            y1=A*pow(math.sin(x+a),1)+A*pow(math.cos(x+a),3)
            y2=A*pow(math.sin(x+a-i),1)+A*pow(math.cos(x+a-i),3)
            canvas.create_line(x*xr,h/2-y1,(x-i)*xr,h/2-y2,fill="red",tag="wave")
        

def start():
    start_stop.set("start")
    v=float(ent_v.get())
    f=float(ent_f.get())
    dt=0.1
    alpha=0
    amp=float(ent_a.get())
    k=2*math.pi*f*dt
    x=0
    while True:
        if start_stop.get()=="stop":
            break
        draw_wave_graph(x,alpha,amp)
        x+=v*dt
        alpha+=k
        canvas.update()
        canvas.after(100)


w=700
h=400
canvas=Canvas(root,width=w,height=h,bg="#262c3d")
canvas.grid(row=0,column=0,rowspan=5)

frame_1=LabelFrame(root,text="source",bg="#262c3d")
frame_1.grid(row=0,column=1)

Button(frame_1,text="start",bg="black",fg="white",relief=FLAT,width="10",\
                                command=start).grid(row=0,column=0,pady=2,columnspan=2)
Button(frame_1,text="stop",bg="black",fg="white",relief=FLAT,width="10",\
        command=lambda:start_stop.set("stop")).grid(row=1,column=0,columnspan=2)
Label(frame_1,text="wave speed",bg="#262c3d",fg="white").grid(row=2,column=0)
Label(frame_1,text="frequency",bg="#262c3d",fg="white").grid(row=3,column=0)
Label(frame_1,text="amplitude",bg="#262c3d",fg="white").grid(row=4,column=0)

ent_v=Entry(frame_1,relief=FLAT)
ent_v.grid(row=2,column=1)

ent_f=Entry(frame_1,relief=FLAT)
ent_f.grid(row=3,column=1)
ent_a=Entry(frame_1,relief=FLAT)
ent_a.grid(row=4,column=1)

#######################################
def draw_stand_wave_graph(A):
    canvas.delete("wave")
    i=0.2
    xr,xf=80,math.pi*2
    x=0
    while x<=xf:
        x+=i
        y1=A*pow(math.sin(x),1)
        y2=A*pow(math.sin(x-i),1)
        canvas.create_line(x*xr,h/2-y1,(x-i)*xr,h/2-y2,fill="red",tag="wave")
        


def start2():
    start_stop.set("start")
    f=float(ent_fs.get())
    dt=0.1
    amp=float(ent_as.get())
    ak=2*math.pi*f*dt
    A=amp
    t=0
    while True:
        if start_stop.get()=="stop":
            break
        draw_stand_wave_graph(A)
        A=amp*math.cos(t*f)
        t+=0.1
        canvas.update()
        canvas.after(100)
    

frame_2=LabelFrame(root,text="standing wave",bg="#262c3d")
frame_2.grid(row=1,column=1)

Button(frame_2,text="start",bg="black",fg="white",relief=FLAT,width="10",\
                                command=start2).grid(row=0,column=0,pady=2,columnspan=2)
Button(frame_2,text="stop",bg="black",fg="white",relief=FLAT,width="10",\
        command=lambda:start_stop.set("stop")).grid(row=1,column=0,columnspan=2)
Label(frame_2,text="frequency",bg="#262c3d",fg="white").grid(row=3,column=0)
Label(frame_2,text="amplitude",bg="#262c3d",fg="white").grid(row=4,column=0)


ent_fs=Entry(frame_2,relief=FLAT)
ent_fs.grid(row=3,column=1)
ent_as=Entry(frame_2,relief=FLAT)
ent_as.grid(row=4,column=1)

root.mainloop()

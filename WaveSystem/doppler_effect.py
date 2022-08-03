from tkinter import*
from PIL import ImageTk,Image

root=Tk()
root.title("Doppler Effect")
img=ImageTk.PhotoImage(Image.open("black_bg.jpg"))

root.config(bg="black")

start_stop=StringVar()
start_stop.set("start")

def get_new_plate(t):
    global plates,x_s
    plates.append((x_s,t,x_s))
def update_plate_position(t):
    global plates,x_s
    dt=0.1
    u=20
    new=[]
    for p in plates:
        x=p[0]+u*dt
        new.append((x,p[1],p[2]))
    plates=new

def draw_plates():
    canvas.delete("plates","source")
    global plates,x_s
    xo=200
    yo=h/2
    for p in plates:
        r=p[0]-p[2]
        canvas.create_line(xo+p[0],yo-50,xo+p[0],yo+50,fill="blue",tag="plates")
        canvas.create_oval(xo+p[2]-r,yo-r,xo+p[2]+r,yo+r,\
                                                               outline="red",tag="plates")
    canvas.create_oval((x_s+xo)-2,yo-2,(x_s+xo)+2,yo+2,fill="red",tag="source",outline="red")

def start():
    global plates,x_s
    plates=[]
    x_s,dt=0,0.1
    start_stop.set("start")
    v=float(ent_su.get())
    f=float(ent_f.get())
    T=1/f
    T_c=0
    t=0
    while True:
        if start_stop.get()=="stop":
            break
        if round((t)-(T*T_c),3)==0:
            get_new_plate(t)
            T_c+=1
        x_s+=v*dt
        update_plate_position(t)
        draw_plates()
        t+=dt
        ent_t.delete(0,END)
        ent_t.insert(0,round(t,3))
        canvas.update()
        canvas.after(100)
    
w=700
h=600
canvas=Canvas(root,width=w,height=h,bg="#262c3d")
canvas.grid(row=0,column=0)
xo=200
canvas.create_line(0,h/2,w,h/2,fill="brown",dash=(2,2))
canvas.create_line(xo,0,xo,h,fill="brown",dash=(2,2))

frame_1=LabelFrame(root,text="source",bg="#262c3d",fg="white")
frame_1.grid(row=0,column=1)
Button(frame_1,text="start",bg="green2",fg="white",relief=FLAT,width="10",\
                                command=start).grid(row=0,column=0,pady=2,columnspan=2)
Button(frame_1,text="stop",bg="green2",fg="white",relief=FLAT,width="10",\
        command=lambda:start_stop.set("stop")).grid(row=1,column=0,columnspan=2)
Label(frame_1,text="sou. speed",bg="#262c3d",fg="white").grid(row=2,column=0)
Label(frame_1,text="frequency",bg="#262c3d",fg="white").grid(row=3,column=0)

ent_su=Entry(frame_1,relief=FLAT)
ent_su.grid(row=2,column=1)

ent_f=Entry(frame_1,relief=FLAT)
ent_f.grid(row=3,column=1)
ent_t=Entry(frame_1,relief=FLAT,font=('verdana',11))
ent_t.grid(row=4,column=0,columnspan=2)

# Button(canvas,text="Hi", relief=FLAT, width="20", bg="#262c3d",activebackground="#262c3d",fg="white",borderwidth=0).place(x=50,y=50)




root.mainloop()

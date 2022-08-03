from tkinter import*
import math


root=Tk()
root.title("Simple Harmonic Oscilation")
root.config(bg="black")

w=900
h=200
h2=500
rx=10
rx2=20
dx1=-w/(rx*2)
k=2
k2=0.2
ry=5
ryv=1
t=float()
state_var=StringVar()
state_var.set("start")
canvas_1=Canvas(width=w,height=h,bg="#262c3d")
canvas_1.grid(row=0,rowspan=5,column=0,pady="4")

canvas_2=Canvas(width=w,height=h2,bg="#262c3d")
canvas_2.grid(row=6,column=0)

def setruler(event):
    canvas_1.delete("rulerline","rulertext")
    canvas_1.create_line(event.x,0,event.x,h/2,fill="red",width="0.5",tag="rulerline")
    rulertext=str((event.x+dx1*rx)/rx)
    canvas_1.create_text(event.x,20,text=rulertext,font=("verdana",8),fill="white",tag="rulertext")

def setvar():
    if state_var.get()=="start":
        state_var.set("stop")


def startanim():
    state_var.set("start")
    canvas_2.delete("graphx","graphv")
    org_v=float(entry1.get())
    x=0
    v=org_v
    org_yx=h2/2-x*ry
    org_yv=h2/2-v*ryv
    t=0
    org_x=t*rx2
    
    while 1:
        if  state_var.get()=="stop":
            break
        a=-k*x-k2*v+10*math.cos(20*t)
        v=v+a*0.01
        x=x+v*0.01
        t +=0.01
        cx=(-dx1+x)*rx
        if v==50:
            canvas_1.create_line(cx,h/2-5,cx,h/2+5,fill="red")
        canvas_1.delete("object")
        canvas_1.create_oval(cx-4,h/2-4,cx+4,h/2+4,fill="red",tag="object")
        canvas_2.create_line(org_x,org_yx,t*rx2,h2/2-x*ry,fill="blue",width="0.5",tag="graphx")
        canvas_2.create_line(org_x,org_yv,t*rx2,h2/2-v*ryv,fill="red",width="0.2",tag="graphv")
        org_yx=h2/2-x*ry
        org_x=t*rx2
        org_yv=h2/2-v*ryv
        
        canvas_1.update()
        canvas_1.after(10)

entry1=Entry(root,width="10",fg="black",relief=FLAT,font=('verdana',10))
entry1.grid(row=0,column=1)

Button(root,text="start",width="10",bg="green",fg="white",font=('verdana',10),relief=FLAT,command=startanim).grid(row=1,column=1)

Button(root,text="stop",width="10",bg="green",fg="white",font=('verdana',10),relief=FLAT,command=setvar).grid(row=2,column=1)


for i1 in range(0,int(w/rx)):
            canvas_1.create_line(i1*rx,0,i1*rx,h,fill="#323744",width="0.5")
canvas_1.create_line(0,h/2,w,h/2,fill="white",width="1")
canvas_1.create_oval(w/2-4,h/2-4,w/2+4,h/2+4,fill="red",tag="object")

canvas_2.create_line(0,h2/2,w,h2/2,fill="white",width="1")
canvas_1.create_line(w/2,h/2-10,w/2,h/2+10,fill="white",width="1")

for i2 in range(0,int(w/rx)):
    canvas_1.create_line(i2*rx,0,i2*rx,8,fill="white")
    if (i2/5)==int(i2/5):
        canvas_1.create_line(i2*rx,0,i2*rx,16,fill="white")

canvas_1.bind("<Motion>",setruler)








root.mainloop()

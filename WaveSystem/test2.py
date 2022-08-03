from tkinter import*
import math


root=Tk()
root.title("Simple Harmonic Oscilation in 2D")
root.config(bg="black")

w=600
h=500
hx=100
rx=10
ryg=10
dy2=h/(2*ryg)
rx2=10
dx1=-w/(rx*2)
ry=1
ryv=0.5
ryv5=10
t=float()
state_var=StringVar()
state_var.set("start")
canvas_1=Canvas(width=w,height=h,bg="#262c3d",relief=FLAT)
canvas_1.grid(row=0,rowspan=5,column=0,pady="4")

canvas_2=Canvas(width=w,height=hx,bg="#262c3d",relief=FLAT)
canvas_2.grid(row=6,column=0)
canvas_3=Canvas(width=w,height=hx,bg="#262c3d",relief=FLAT)
canvas_3.grid(row=7,column=0)

def setruler(event):
    canvas_1.delete("rulerline","rulertext")
    canvas_1.create_line(event.x,0,event.x,h/2,fill="red",width="0.5",tag="rulerline")
    rulertext=str((event.x+dx1*rx)/rx)
    canvas_1.create_text(event.x,20,text=rulertext,font=("verdana",8),fill="white",tag="rulertext")

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
    org_vx=float(entry1.get())
    org_vy=float(entry3.get())
    x=0
    y=0
    ox=0
    oy=0
    vx=org_vx
    vy=org_vy
    org_yx=hx/2-x*ry
    org_yv=hx/2-vx*ryv
    t=0
    k=float(entry2.get())
    org_x=t*rx2
    f=float(entry3.get())
    
    while 1:
        if  state_var.get()=="stop":
            break
        ax=-k*x+20*math.sin(1*t)
        ay=-k*y+20*math.sin(3*t)
        vx=vx+ax*0.01
        vy=vy+ay*0.01
        x=x+vx*0.01
        y=y+vy*0.01
        t +=0.01
        cx=(-dx1+x)*rx
        cy=(dy2-y)*ryg
        canvas_1.delete("object")
        canvas_2.delete("time")
        canvas_1.create_oval(cx-4,cy-4,cx+4,cy+4,fill="red",tag="object")
        canvas_1.create_line((-dx1+ox)*rx,(dy2-oy)*ryg,cx,cy,fill="red",tag="path")
        canvas_2.create_text(650,30,text=("t="+str(round(t,2))),font=('verdana',10),fill="white",tag="time")
        ox=x
        oy=y
        canvas_2.create_line(org_x,org_yx,t*rx2,hx/2-x*ry,fill="blue",width="0.5",tag="graphx")
        canvas_3.create_line(org_x,org_yv,t*rx2,hx/2-vx*ryv,fill="red",width="0.2",tag="graphv")
        org_yx=hx/2-x*ry
        org_x=t*rx2
        org_yv=hx/2-vx*ryv
        
        canvas_1.update()
        canvas_1.after(10)


Label(root,text="velocity-X",width="15",bg="gray",fg="white").grid(row=0,column=1)
Label(root,text="velocity-Y",width="15",bg="gray",fg="white").grid(row=1,column=1)
Label(root,text="k",width="15",bg="gray",fg="white").grid(row=2,column=1)
entry1=Entry(root,width="10",fg="black",relief=FLAT,font=('verdana',10))
entry1.grid(row=0,column=2)

entry2=Entry(root,width="10",fg="black",relief=FLAT,font=('verdana',10))
entry2.grid(row=2,column=2)

entry3=Entry(root,width="10",fg="black",relief=FLAT,font=('verdana',10))
entry3.grid(row=1,column=2)
entry3.insert(0,"30")



Button(root,text="start",width="20",bg="blue2",fg="white",font=('verdana',10),relief=FLAT,command=startanim).grid(row=3,column=1,columnspan=2)

Button(root,text="stop",width="20",bg="blue3",fg="white",font=('verdana',10),relief=FLAT,command=setvar).grid(row=4,column=1,columnspan=2)


for i1 in range(0,int(w/rx)):
            canvas_1.create_line(i1*rx,0,i1*rx,h,fill="#323744",width="0.5")

for i3 in range(0,int(hx/ry)):
            canvas_2.create_line(0,i3*ry,w,i3*ry,fill="#323744",width="0.5")
for i4 in range(0,int(hx/ryv5)):
            canvas_3.create_line(0,i4*ryv5,w,i4*ryv5,fill="#323744",width="0.5")
canvas_1.create_line(0,h/2,w,h/2,fill="white",width="1")
canvas_1.create_oval(w/2-4,h/2-4,w/2+4,h/2+4,fill="red",tag="object")

canvas_2.create_line(0,hx/2,w,hx/2,fill="white",width="1")
canvas_3.create_line(0,hx/2,w,hx/2,fill="white",width="1")
canvas_1.create_line(w/2,h/2-10,w/2,h/2+10,fill="white",width="1")

for i2 in range(0,int(w/rx)):
    canvas_1.create_line(i2*rx,0,i2*rx,8,fill="white")
    if (i2/5)==int(i2/5):
        canvas_1.create_line(i2*rx,0,i2*rx,16,fill="white")

canvas_1.bind("<Motion>",setruler)
canvas_2.bind("<Motion>",setrulerx)
canvas_3.bind("<Motion>",setrulerv)








root.mainloop()

from tkinter import*
import math


root=Tk()
root.title("Simple Harmonic Oscilation")
root.config(bg="black")

w=700
h=160
hx=250
rx=10
rx2=10
dx1=-w/(rx*2)
ry=5
ryv=1
ryv5=5
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
    org_v=float(entry1.get())
    x=0
    ox=0
    v=org_v
    org_yx=hx/2-x*ry
    org_yv=hx/2-v*ryv
    t=0
    k=float(entry2.get())
    org_x=t*rx2
    f=float(entry3.get())
    
    while 1:
        if  state_var.get()=="stop":
            break
        a=-k*x-f*v
        v=v+a*0.01
        x=x+v*0.01
        t +=0.01
        cx=(-dx1+x)*rx
        canvas_1.delete("object")
        canvas_2.delete("time")
        canvas_1.create_oval(cx-4,h/2-4,cx+4,h/2+4,fill="red",tag="object")
        canvas_1.create_line((-dx1+ox)*rx,h/2,cx,h/2,fill="red",tag="path")
        canvas_2.create_text(650,30,text=("t="+str(round(t,2))),font=('verdana',10),fill="white",tag="time")
        ox=x
        canvas_2.create_line(org_x,org_yx,t*rx2,hx/2-x*ry,fill="blue",width="0.5",tag="graphx")
        canvas_3.create_line(org_x,org_yv,t*rx2,hx/2-v*ryv,fill="red",width="0.2",tag="graphv")
        org_yx=hx/2-x*ry
        org_x=t*rx2
        org_yv=hx/2-v*ryv
        
        canvas_1.update()
        canvas_1.after(10)


Label(root,text="velocity",width="15",bg="gray",fg="white").grid(row=0,column=1)
Label(root,text="friction factor",width="15",bg="gray",fg="white").grid(row=1,column=1)
Label(root,text="k",width="15",bg="gray",fg="white").grid(row=2,column=1)
entry1=Entry(root,width="10",fg="black",relief=FLAT,font=('verdana',10))
entry1.grid(row=0,column=2)

entry2=Entry(root,width="10",fg="black",relief=FLAT,font=('verdana',10))
entry2.grid(row=2,column=2)

entry3=Entry(root,width="10",fg="black",relief=FLAT,font=('verdana',10))
entry3.grid(row=1,column=2)
entry3.insert(0,"0")



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

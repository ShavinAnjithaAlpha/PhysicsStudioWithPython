from tkinter import *
from tkinter import ttk
import math, sys

class wave_oscillation(Frame):
    def __init__(self):
        
        Frame.__init__(self)
        self.master.title("wave grpah")
        self.master.geometry("900x730")
        self.config(bg="#212422")
        self.grid(row=0, column=0)

        self.wGr = 600
        self.hGr = 20
        self.w = 300
        self.h = 720
        # start variable for start and the stop
        self.start = StringVar()
        self.start.set("start")
        # idenify motion object parameter
        self.td = 10 # width of the object
        self.l = 200
        self.t1 = 50
        self.xr = 10
        self.xy = [0, self.hGr/2]
        self.ampchecker = []
        self.mainamp = []
        ButtonBox
        self.ampandomega = []
        # create the canvas objects
        self.canvasPlot = Canvas(self, width=self.wGr, height=self.hGr, bg="black", bd=0, highlightthickness=0)
        self.canvasPlot.grid(row=0, column=0, pady=2)
        self.canvasPlot.create_line(0, self.hGr/2, self.wGr, self.hGr/2, fill="blue")
        # canvas for the amplitudes
        self.canvasAmp = Canvas(self, width=self.wGr, height=self.hGr, bg="#454a47", highlightthickness=0, bd=0)
        self.canvasAmp.grid(row=1, column=0)

        self.canvasImage = Canvas(self, width=self.w, height=self.h, bg="#212422", bd=0, highlightthickness=0)
        self.canvasImage.grid(row=0, column=1, rowspan=3, padx=5)
        # draw the based
        self.canvasImage.create_rectangle(self.t1, self.h-25, self.t1+self.l, self.h, fill="brown", outline="brown")
        self.canvasImage.create_line(0, self.h/2, self.w ,self.h/2, fill="blue", dash=(2,2))

        # parameter setting frame
        self.paraframe = LabelFrame(self, text="parameters", bg="#212422", fg="white")
        self.paraframe.grid(row=2, column=0, ipadx=20)
        # variable for the scale
        self.alpha = StringVar()
        self.beta = StringVar()
        self.gama = StringVar()
        self.osci = StringVar()
        self.initvelocity = StringVar()
        self.weight = StringVar()
        # label for alpha beta and gama parameter
        Label(self.paraframe, text="alpha factor ", font=('verdana', 9), width="15", bg="#212422", fg="white").grid(row=0,column=0)
        Label(self.paraframe, text="beta factor ", font=('verdana', 9), width="15", bg="#212422", fg="white").grid(row=1, column=0)
        Label(self.paraframe, text="gama factor ", font=('verdana', 9), width="15", bg="#212422", fg="white").grid(row=2, column=0)
        Label(self.paraframe, text="oscillation factor ", font=('verdana', 9), width="15", bg="#212422", fg="white").grid(row=3, column=0)
        Label(self.paraframe, text="init velocity ", font=('verdana', 9), width="15", bg="#212422", fg="white").grid(row=4, column=0)
        Label(self.paraframe, text="weight ", font=('verdana', 9), width="15", bg="#212422", fg="white").grid(row=5, column=0)
        # scale for get the value for the plpha beta and gama
        self.alphascale = Scale(self.paraframe, from_=0.0, to=200.0, orient=HORIZONTAL, length="330", variable=self.alpha, resolution=0.1, bd=0, highlightthickness=0, fg="white", width="15", bg="#212422", sliderrelief=FLAT)
        self.alphascale.grid(row=0, column=1, columnspan=2)

        self.betascale = Scale(self.paraframe, from_=0.0, to=10.0, orient=HORIZONTAL, length="330", variable=self.beta, resolution=0.05, bd=0, highlightthickness=0, fg="white", width="15", bg="#212422", sliderrelief=FLAT)
        self.betascale.grid(row=1, column=1, columnspan=2)

        self.gamascale = Scale(self.paraframe, from_=0.0, to=100.0, orient=HORIZONTAL, length="330", variable=self.gama, resolution=0.05, bd=0, highlightthickness=0, fg="white", width="15", bg="#212422", sliderrelief=FLAT)
        self.gamascale.grid(row=2, column=1, columnspan=2)

        self.osciscale = Scale(self.paraframe, from_=0.0, to=20.0, orient=HORIZONTAL, length="330", variable=self.osci, resolution=0.05, bd=0, highlightthickness=0, fg="white", width="15", bg="#212422", sliderrelief=FLAT)
        self.osciscale.grid(row=3, column=1, columnspan=2)

        self.velocityscale = Scale(self.paraframe, from_=0.0, to=200.0, orient=HORIZONTAL, length="350", variable=self.initvelocity, resolution=0.1, bd=0, highlightthickness=0, fg="white", width="15", bg="#212422", sliderrelief=FLAT)
        self.velocityscale.grid(row=4, column=1, columnspan=2)

        self.weightscale = Scale(self.paraframe, from_=0.0, to=100.0, orient=HORIZONTAL, length="350",
                                   variable=self.weight, resolution=0.1, bd=0, highlightthickness=0, fg="white", width="15", bg="#212422", sliderrelief=FLAT)
        self.weightscale.grid(row=5, column=1 , columnspan=2)

        # create start ,pause and stop button
        Button(self.paraframe, text="Start", bd=0, font=('verdana', 10), command=self.startMotion, width="10", bg="#12d95d", fg="white").grid(row=6, column=0, pady=5)
        Button(self.paraframe, text="Stop", bd=0, font=('verdana', 10), command=self.setvar, width="10", bg="#12d95d", fg="white").grid(row=6, column=1)

        # amplitude entry box
        Label(self.paraframe, text="amplitude", font=('verdana' ,10), bg="#212422", fg="white").grid(row=7, column=0)
        self.ampentry = Entry(self.paraframe, bd=0, font=('verdana', 10))
        self.ampentry.grid(row=7, column=1)
        Button(self.paraframe, text="Save amp. and omega", bd=0, font=('verdana', 10), bg="#12d95d", fg="white",command=self.save_ampomega).grid(row=7, column=2)
        Button(self.paraframe, text="Plotting", font=('verdana', 10),
               command=self.plotampversesomega, bd=0, bg="#12d95d", fg="white").grid(row=7, column=3)

    def rearrangedlist(self, l, x):
        
        a, b, c = l[0], l[1], l[2]
        return [b, c, x]

    def startMotion(self):
        
        # identify parameters
        self.v = float(self.initvelocity.get())
        self.x = 0
        self.t = 0
        dt = 0.01
        # start var set to start
        self.start.set("start")
        # identify parameter to dedicate the relative amplitude
        self.relativeamp = []
        # initialize the motion
        while self.start.get() == "start":
            alpha ,beta, gama = float(self.alpha.get()), float(self.beta.get()), float(self.gama.get())
            omega ,w= float(self.osci.get()), float(self.weight.get())
            f = gama*math.cos(omega*self.t) - beta*self.v - alpha*self.x -w
            self.v += f*dt
            self.x += self.v*dt
            if len(self.relativeamp) < 3:
                self.relativeamp.append(self.x)
            else:
                self.relativeamp = self.rearrangedlist(self.relativeamp, self.x)
            # check the relativeamp list have the relative amplitude
            if len(self.relativeamp) == 3:
                if (self.relativeamp[0] < self.relativeamp[1] > self.relativeamp[2]) or (self.relativeamp[0] > self.relativeamp[1] < self.relativeamp[2]):
                    self.ampentry.delete(0, END)
                    self.ampentry.insert(0, abs(round(self.relativeamp[1], 3)))
            # update the new image in the canvas
            self.createNewImage(self.x, self.t)
            # update the list and plot the grpah
            self.plot()
            if round(self.x,0)  == 0:
                self.saveampchecker(self.ampchecker)
                self.ampchecker = []
            self.ampchecker.append([self.t ,self.x])
            self.t += dt
            self.canvasImage.update()
            self.canvasPlot.update()
            self.canvasImage.after(10)
            self.canvasPlot.after(10)

    def createNewImage(self, x, t):
        
        self.canvasImage.delete("object", "elastic", "force")
        pos_object = self.h/2 - x*self.xr
        # draw the new motion object
        # draw the elastic
        self.canvasImage.create_line(self.w/2, pos_object+self.td/2, self.w/2, self.h-25, fill="#fcfe31", width="5", tag="elastic")
        self.canvasImage.create_rectangle(self.t1, pos_object-self.td/2, self.t1+self.l, pos_object+self.td/2, fill="#f57435", outline="orange", tag="object")
        # draw the oscillation force in canvas
        gama, omega = float(self.gama.get()), float(self.osci.get())
        value_of_F = gama*math.cos(omega* t)
        b_point = pos_object - self.td/2
        self.canvasImage.create_line(self.w/2, b_point, self.w/2, b_point-value_of_F*5, fill="#e51734", arrow="last", tag="force", width="1.5")

    def plot(self):
        
        self.canvasPlot.delete("plot_line")
        self.xy.append(self.t*100)
        self.xy.append(self.hGr/2-self.x*10)
        self.canvasPlot.create_line(self.xy, fill="red", tag="plot_line", smooth=True, width="1.2")

    def setvar(self):
        
        self.canvasAmp.delete("amp")
        self.start.set("stop")
        self.xy = [0, self.hGr/2]
        self.canvasAmp.create_line(self.mainamp, fill="red", dash=(2,2), smooth=True, tag="amp")
        self.mainamp = []

    def saveampchecker(self, amp):
        
        amplitude = []
        
        for i in range(1, len(amp)-1):
            if (amp[i][1] > amp[i-1][1] and amp[i][1] > amp[i+1][1]) or (amp[i][1] < amp[i-1][1] and amp[i][1] < amp[i+1][1]):
                amplitude.append(amp[i][0]*100)
                amplitude.append(self.hGr/2 - amp[i][1]*10)
                if amp[i][1] > 0:
                    self.mainamp.append(amp[i][0]*100)
                    self.mainamp.append(self.hGr / 2 - amp[i][1] * 10)
        if len(amplitude) >= 2:
            self.canvasAmp.create_oval(amplitude[0]-3, amplitude[1]-3, amplitude[0]+3, amplitude[1]+3, fill="green2", outline="green2", tag="amp")

    def save_ampomega(self):
        
        self.ampandomega.append([float(self.osci.get()), float(self.ampentry.get())])
    
    def plotampversesomega(self):
        
        self.plotwindow = Toplevel(self)
        self.plotcanvas = Canvas(self.plotwindow, width="600", height="600", bg="black")
        self.plotcanvas.grid(row=0, column=0)

        rx = 30
        ry = 60
        plotpoints = []
        for item in self.ampandomega:
            plotpoints.append(rx * item[0])
            plotpoints.append(ry * item[1])
        self.plotcanvas.create_line(plotpoints, smooth=True, fill="red", width="1.5")



def main():
    wave_oscillation().mainloop()

if __name__ == "__main__":
    main()
    sys.exit(0)
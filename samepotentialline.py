from tkinter import *
import math

class Potentiallines(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.master.title("Same Potentila fileld line creater")
        self.master.geometry("700x600")
        self.grid(row=0, column=0)

        # identify consts
        self.w = 600
        self.h = 600
        self.rx = 30
        self.ry = 30
        self.q1 = [0, 0]
        self.q2 = [0, 0]
        # create canvas
        self.canvas = Canvas(self, width=self.w, height=self.h, bg="#262c3d")
        self.canvas.grid(row=0, column=0)
        # create the grid system
        self.gridcreater()
        # show the two point charges in the canvas
        self.x1 ,self.y1 = -int(self.w/(self.rx*2)), -int(self.h/(self.ry*2))
        self.showcharges(self.q1)
        self.showcharges(self.q2)

        self.potentiallinecreater()


    def gridcreater(self):
        # create main x_axis and y_axis
        self.canvas.create_line(0, self.h/2, self.w, self.h/2, fill="white")
        self.canvas.create_line(0, self.w/2, self.h, self.w/2, fill="white")

        # create grid lines
        for i in range(0, int(self.w/self.rx)):
            self.canvas.create_line(i*self.rx, 0, i*self.rx, self.h, fill="#323744")
        for j in range(0, int(self.h/self.ry)):
            self.canvas.create_line(0, j*self.ry, self.w, j*self.ry, fill="#323744")

    def showcharges(self, Q):
        self.canvas.create_oval((-self.x1 + Q[0]) * self.rx - 2, self.h-(Q[1]-self.y1)*self.ry-2, \
                                (-self.x1 + Q[0]) * self.rx + 2, self.h - (Q[1] - self.y1) * self.ry + 2, fill="green2", outline="green2")
    def calculatePotential(self, r, theta):
        theta = math.radians(theta)
        point = [r*math.cos(theta), r*math.sin(theta)]
        try:
            # calculate potential V1 by q1
            v1 = 1/math.sqrt(pow(point[0]- self.q1[0], 2) + pow(point[1]- self.q1[1], 2))
            # calculate potential V2 by q2
            v2 = 1 / math.sqrt(pow(point[0] - self.q2[0], 2) + pow(point[1] - self.q2[1], 2))
            return [round(v1 + v2 , 2), point[0], point[1]]
        except:
            return False

    def appendpoint(self, x, y):
        point_x = (-self.x1 + x)*self.rx
        poin_y = self.h - self.ry*(y-self.y1)
        return [point_x, poin_y]

    def potentiallinecreater(self):
        pointU = []
        for r in range(1, 20):
            for theta in range(0, 36):
                if self.calculatePotential(r*1, theta*5):
                    pointU.append(self.calculatePotential(r*4, theta*5))
        # filter the same values of potentials
        samePotential = []
        for item in pointU:
            if not(item[0] in samePotential):
                samePotential.append(item[0])
        # draw the same potential lines
        for U in samePotential:
            new_point = []
            for item in pointU:
                if U == item[0]:
                    p = self.appendpoint(item[1], item[2])
                    new_point.append(p[0])
                    new_point.append(p[1])
            # draw the line by new_point list
            if len(new_point) >= 4:
                self.canvas.create_line(new_point, fill="red", smooth=True, dash=(2,2))
                self.canvas.update()
            new_point = []

def main():
    Potentiallines().mainloop()

if __name__ == '__main__':
    main()


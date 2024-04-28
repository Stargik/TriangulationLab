import tkinter as tk
import random
from Voronoi import Voronoi
import time

class MainWindow:
    RADIUS = 2
    LOCK_FLAG = False
    
    def __init__(self, master):

        self.vp = None
        self.delauneys = []
        self.lines = []
        self.points = []

        self.master = master
        self.master.title("Triangulation")
        self.rand_count = 5

        self.frmMain = tk.Frame(self.master, relief=tk.RAISED, borderwidth=1)
        self.frmMain.pack(fill=tk.BOTH, expand=1)

        self.w = tk.Canvas(self.frmMain, width=1000, height=700)
        self.w.config(background='white')
        self.w.bind('<Double-1>', self.onDoubleClick)
        self.w.pack()       

        self.frmButton = tk.Frame(self.master)
        self.frmButton.pack()
        
        self.btnDelauney = tk.Button(self.frmButton, text='Calculate Delauney', width=16, command=self.onClickDelauney)
        self.btnDelauney.pack(side=tk.LEFT)

        self.btnVoronoi = tk.Button(self.frmButton, text='Show Voronoi', width=16, command=self.onClickVoronoi)
        self.btnVoronoi.pack(side=tk.LEFT)

        self.btnVoronoi = tk.Button(self.frmButton, text='Hide Voronoi', width=16, command=self.onClickHideVoronoi)
        self.btnVoronoi.pack(side=tk.LEFT)

        self.btnClear = tk.Button(self.frmButton, text='Clear', width=16, command=self.onClickClear)
        self.btnClear.pack(side=tk.LEFT)

        self.btnDelauney = tk.Button(self.frmButton, text='Random points', width=16, command=self.onClickRandomPoints)
        self.btnDelauney.pack(side=tk.LEFT)

        self.randomField = tk.Entry(self.frmButton, width=6)
        self.randomField.insert(0, self.rand_count)
        self.randomField.pack(side=tk.LEFT)
        
    def onClickVoronoi(self):
        if self.vp:
            lines = self.vp.get_output()
            self.drawLinesOnCanvas(lines)

    def onClickHideVoronoi(self):
        for l in self.lines:
            self.w.delete(l)
        self.lines = []

    def onClickClear(self):
        self.LOCK_FLAG = False
        self.w.delete(tk.ALL)
        self.delauneys = []
        self.lines = []
        self.points = []
        self.vp = None

    def onDoubleClick(self, event):
        if not self.LOCK_FLAG:
            eps = random.random() / 10
            self.w.create_oval(event.x-self.RADIUS+eps, event.y-self.RADIUS+eps, event.x+self.RADIUS+eps, event.y+self.RADIUS+eps, fill="black")

    def onClickRandomPoints(self):
        if not self.LOCK_FLAG:
            self.w.delete(tk.ALL)
            pts = []
            self.rand_count = int(self.randomField.get())
            for i in range(0,self.rand_count):
                isAppend = False
                while not isAppend:
                    x = random.uniform(20,980)
                    y = random.uniform(20,680)
                    xy = (x, y)
                    if xy not in pts:
                        pts.append(xy)
                        isAppend = True
            for p in pts:
                self.w.create_oval(p[0]-self.RADIUS, p[1]-self.RADIUS, p[0]+self.RADIUS, p[1]+self.RADIUS, fill="black")
            
    def drawLinesOnCanvas(self, lines):
        for l in lines:
            self.lines.append(self.w.create_line(l[0], l[1], l[2], l[3], fill='blue'))

    def onClickDelauney(self):
        if not self.LOCK_FLAG:
            self.LOCK_FLAG = True
        
        pObj = self.w.find_all()
        self.points = []
        for p in pObj:
            coord = self.w.coords(p)
            self.points.append((coord[0]+self.RADIUS, coord[1]+self.RADIUS))

        start = time.time()
        self.vp = Voronoi(self.points)
        self.vp.process()
        end = time.time()
        print(f"Points count: {len(self.points)}; Execution time: {(end-start) * 10**3} ms (Voronoi)")

        self.delauneys = []
        start2 = time.time()
        for seg in self.vp.output:
            if seg.verts[1].p.x and seg.verts[1].p.y:
                self.delauneys.append(self.w.create_line(seg.verts[0].p.x, seg.verts[0].p.y, seg.verts[1].p.x, seg.verts[1].p.y, fill="red"))
        end2 = time.time()
        print(f"Points count: {len(self.points)}; Execution time: {(end2-start2) * 10**3} ms (Delauney)")

def main(): 
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()

if __name__ == '__main__':
    main()

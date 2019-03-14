from turtle import *
from tkinter.filedialog import askopenfile, asksaveasfile





class GraphImage(object):
    def __init__(self,dots=[],connects = []):
        self.dots = dots
        self.connects = connects

    def add_dot(self,dot):
        if self.nearest_dot(dot, min_distance=30) == None:
            self.dots.append(dot)

    def add_connect(self,connect):
        self.connects.append(connect)

    def nearest_dot(self,pos, min_distance=15):
        for i in range(len(self.dots)):
                dist = ((self.dots[i][0]-pos[0])**2+(self.dots[i][1]-pos[1])**2)**0.5
                if dist<=min_distance:
                    return i

    def get_dot(self,id):
        return self.dots[id]

    @staticmethod
    def from_graph(graph):
        pass
    @staticmethod
    def form_file(file):
        dots = [list(map(float,i.split(',')[:2]))for i in file.readline().split('|')]
        conects = [list(map(int,i.split(','))) for i in file.readline()[:-1].split('|')]
        return GraphImage(dots=dots,connects=conects)

    def save_to_file(self,file):
        to_save_dot = '|'.join([','.join(list(map(str,i))) for i in self.dots])
        to_save_con = '|'.join([','.join(list(map(str,i))) for i in self.connects])
        file.write(str(to_save_dot)+'\n'+str(to_save_con)+'\n')


class Drawer(object):
    def __init__(self,graph_im=GraphImage()):
        self.turtle = Turtle()
        self.graph_im = graph_im
        self.new_con = []
        self.mod = 'points'
        speed(0)
        onkey(self.change_mod,'m')
        onkey(self.clear,'c')
        onkey(self.open_file,'o')
        onkey(self.save_as_file,'s')
        onscreenclick(self.get_pos)
        listen()
    def draw(self):
        mainloop()
    def get_pos(self,x,y):
        if self.mod == 'points':
            self.graph_im.add_dot([x,y])
        else:
            i = self.graph_im.nearest_dot([x,y])
            if i !=None:
                self.new_con.append(i)
            if len(self.new_con)==2:
                self.graph_im.add_connect(self.new_con)
                self.new_con = []
        self.draw_graph()

    def clear(self):
        self.graph_im = GraphImage()
        self.mod = 'points'
        self.new_con = []
        resetscreen()
    def open_file(self,filename=None):
        if filename == None:
            file = askopenfile(mode = 'r',filetypes=[('Text Files', '*.txt')])
        else:
            file = open(filename,'r')

        if file:
            self.clear()
            self.graph_im = GraphImage.form_file(file)
            self.draw_graph()
    def save_as_file(self):
        file = asksaveasfile(mode = 'w',filetypes=[('Text Files', '*.txt')])
        if file:
            self.graph_im.save_to_file(file)
    def change_mod(self):
        if self.mod == 'points':
            self.mod = 'connects'
        else:
            self.mod = 'points'


    def draw_graph(self):
        for dot in self.graph_im.dots:
            self.put_dot(dot)
        for con in self.graph_im.connects:
            self.put_con(con) 

    def put_dot(self,pos):
        self.turtle.penup()
        self.turtle.setposition(*pos)
        self.turtle.dot(30)
        self.turtle.penup()
    def put_con(self,connect):
        dot1 = self.graph_im.get_dot(connect[0])
        dot2 = self.graph_im.get_dot(connect[1])
        self.turtle.penup()
        self.turtle.setposition(*dot1)
        self.turtle.pendown()
        self.turtle.setposition(*dot2)
        self.turtle.penup()


if __name__=='__main__':
    Drawer().draw()
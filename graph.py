from turtle import *
from tkinter.filedialog import askopenfile, asksaveasfile

__all__=['Drawer','Graph','Func_Result']

class Dot(object):
    def __init__(self,pos,color='black'):
        self.pos = pos
        self.color = color
    def __repr__(self):
        return ','.join(list(map(str,self.pos))) + ',' + self.color
class Connect(object):
    def __init__(self,dot1,dot2,color='black'):
        self.dot1=dot1
        self.dot2=dot2
        self.color=color
    def __repr__(self):
        return str(self.dot1)+','+str(self.dot2)+','+self.color

class GraphImage(object):
    def __init__(self,dots=[],connects = []):
        self.dots = dots
        self.connects = connects

    def add_dot(self,pos,d_color='black'):
        dot = Dot(pos,color=d_color)
        if self.nearest_dot(pos, min_distance=30) == None:
            self.dots.append(dot)

    def add_connect(self,connect):
        self.connects.append(connect)

    def nearest_dot(self,pos, min_distance=15):
        for i in range(len(self.dots)):           
            dist = ((self.dots[i].pos[0]-pos[0])**2+(self.dots[i].pos[1]-pos[1])**2)**0.5
            if dist<=min_distance:
                return i

    def get_dot(self,id):
        return self.dots[id]

    def get_graph(self):
        return Graph(dots=len(self.dots),connects=self.connects)

    def update_from_func_result(self,Func_Result):
        for i in Func_Result.colored_dots:
            self.dots[i[0]].color=i[1]
        for i in Func_Result.colored_connects:
            for j in range(len(self.connects)):
                if (i[0]==self.connects[j].dot1 and i[1]==self.connects[j].dot2) or (i[0]==self.connects[j].dot2 and i[1]==self.connects[j].dot1):
                    self.connects[j].color = i[2]


    @staticmethod
    def from_graph(graph):
        pass


    @staticmethod
    def form_file(file):
        dots = [i.split(',') for i in file.readline()[:-1].split('|')]
        a = []
        for i in dots:
            a.append(Dot(list(map(float,i[:2])),color=i[2]))
        dots = a

        conects = [i.split(',') for i in file.readline()[:-1].split('|')]
        a = []
        for i in conects:
            a.append(Connect(int(i[0]),int(i[1]),color=i[2]))
        conects = a
        return GraphImage(dots=dots,connects=conects)

    def save_to_file(self,file):
        to_save_dot = '|'.join([str(i) for i in self.dots])
        to_save_con = '|'.join([str(i) for i in self.connects])
        file.write(str(to_save_dot)+'\n'+str(to_save_con)+'\n')


class Graph(object):
    def __init__(self,dots=0,connects=[]):
        self.dots = dots
        self.connects = connects
        someshit = []
        for i in range(dots):
            someshit.append([i])
            for connect in self.connects:
                if connect.dot1==i:
                    someshit[i].append(connect.dot2)
                elif connect.dot2==i:
                    someshit[i].append(connect.dot1)
        self.grap_something = someshit

    def connected_component(self,dot):
        return self.grap_something[dot]
    def add_dot(self):
        self.dots+=1
    def add_connect(self,connect):
        self.connects.append(connect)

class Func_Result(object):
    def __init__(self,colored_dots=[],colored_connects=[]):
        self.colored_dots = colored_dots
        self.colored_connects = colored_connects


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
                self.graph_im.add_connect(Connect(self.new_con[0],self.new_con[1]))
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

    def execute(self,function):
        update = function(self.graph_im.get_graph())
        self.graph_im.update_from_func_result(update)
        self.draw_graph()

    def draw_graph(self):
        for con in self.graph_im.connects:
            self.put_con(con) 
        for dot in range(len(self.graph_im.dots)):
            self.put_dot(self.graph_im.dots[dot],dot)

    def put_dot(self,dot,id):
        self.turtle.penup()
        self.turtle.setposition(*dot.pos)
        self.turtle.dot(30,dot.color)
        self.turtle.color('magenta')
        self.turtle.write(str(id+1),font=("Arial", 72, "normal"))
        self.turtle.color('black')
        self.turtle.penup()
    def put_con(self,connect):
        dot1 = self.graph_im.get_dot(connect.dot1)
        dot2 = self.graph_im.get_dot(connect.dot2)
        self.turtle.color(connect.color)
        self.turtle.penup()
        self.turtle.setposition(*dot1.pos)
        self.turtle.pendown()
        self.turtle.setposition(*dot2.pos)
        self.turtle.penup()
        self.turtle.color('black')


if __name__=='__main__':
    Drawer().draw()
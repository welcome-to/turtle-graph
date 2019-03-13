from turtle import *
from tkinter.filedialog import askopenfile, asksaveasfile


__all__ = ['open_file']


def get_pos(*args):
    x,y = args[:2]
    if len(args)>2:
        color = args[2]
    else:
        color = 'black'

    global mod, list_of_pos,conects,first_point_id,second_point_id,T
    if mod == 0:
        T.penup()
        T.setposition(x,y)
        T.dot(30,color)
        T.penup()
        list_of_pos.append((x,y,color))
    else:
        if first_point_id == None:
            for i in range(len(list_of_pos)):
                dist = ((list_of_pos[i][0]-x)**2+(list_of_pos[i][1]-y)**2)**0.5
                if dist<15:
                    first_point_id = i
        else:
            for i in range(len(list_of_pos)):
                dist = ((list_of_pos[i][0]-x)**2+(list_of_pos[i][1]-y)**2)**0.5
                if dist<15:
                    second_point_id = i
            if second_point_id != None:
                T.penup()
                T.setposition(*list_of_pos[first_point_id][:2])
                T.pendown()
                T.setposition(*list_of_pos[second_point_id][:2])
                conects.append((first_point_id,second_point_id))
                first_point_id = None
                second_point_id = None
def open_file(filename=None):
    if filename==None:
        file = askopenfile(mode = 'r',filetypes=[('Text Files', '*.txt')])
    else:
        file = open(filename,'r')
        create_turtle()

    try:
        dots = file.readline()
        conects = file.readline()
        clear()
        draw_graf(dots,conects)
    except:
        pass
def save_as_file():
    file = asksaveasfile(mode = 'w',filetypes=[('Text Files', '*.txt')])
    global list_of_pos, conects
    try:
        to_save_dot = '|'.join([','.join(list(map(str,i))) for i in list_of_pos])
        to_save_con = '|'.join([','.join(list(map(str,i))) for i in conects])
        file.write(str(to_save_dot)+'\n'+str(to_save_con)+'\n')
    except:
        pass
def draw_graf(dots,conects):
    try:
        dots = dots[:-1]
        dots = [list(map(float,i.split(',')[:2]))+[i.split(',')[-1]] for i in dots.split('|')]
        for i in dots:
            get_pos(*i)
        change_mod()
        conects = [list(map(int,i.split(','))) for i in conects[:-1].split('|')]
        for i in conects:
            dot1 = dots[i[0]]
            dot2 = dots[i[1]]
            get_pos(*dot1)
            get_pos(*dot2)
    except:
        pass



def change_mod():
    global mod,first_point_id,second_point_id
    if mod == 0:
        mod = 1
    else:
        mod = 0
        second_point_id = None
        first_point_id = None
def clear():
    global mod,list_of_pos,first_point_id,second_point_ids
    mod = 0
    first_point_id = None
    second_point_id = None
    list_of_pos = []
    resetscreen()

def create_turtle():
    global list_of_pos, conects,mod,first_point_id,second_point_id,T
    T = Turtle()
    list_of_pos = []
    conects = []
    mod = 0
    first_point_id = None
    second_point_id = None
    onkey(change_mod,'m')
    onkey(clear,'c')
    onkey(open_file,'o')
    onkey(save_as_file,'s')
    onscreenclick(get_pos)
    listen()
    mainloop()

if __name__ == '__main__':
    create_turtle()
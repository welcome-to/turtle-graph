from graph import *


def func(Graph):
    print(Graph.connected_component(2))
    return Func_Result(colored_dots = [[0,'black']],colored_connects=[[0,1,'blue']])



im = Drawer()
im.open_file(filename='test_graph.txt')
im.execute(func)
im.draw()

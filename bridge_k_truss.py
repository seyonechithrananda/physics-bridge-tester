from anastruct import SystemElements
import anastruct
import math
import numpy as np
#height = 0.136
height = 0.102
element_type = 'truss'
length = 1
pop_len = 0.95
pop_width = 0.9/100
#pop_thick = 1.8/1000
pop_thick = 1.8/1000
pop_density = 880 #kg/m^3
pop_compressive_strength = 18100 #kPa
pop_tensile_strength = 70000 #kPa
class Bridge:
    def __init__(self, x, y, connections, loads, supports, density=880, unit = 'm', width=0.95/100, thick=1.8/1000, pop_compressive_strength = 18100, pop_tensile_strength = 70000):
        pop_cross_area = width * thick
        pop_mpl = pop_cross_area * density
        g = pop_mpl * 9.81 / 1000
        unit_conv = 1
        if (unit == 'cm'):
            unit_conv = (1/100)
        nodes = [[x[i]*unit_conv, y[i]*unit_conv] for i in range(len(x))]
        ss = SystemElements(EA = pop_cross_area*8600000)
        for node1, node2 in connections:
            ss.add_element([nodes[node1], nodes[node2]], element_type='truss', g=g)

        for node in supports:
            id = ss.find_node_id(nodes[node])
            ss.add_support_fixed(id)
        for node, load in loads:
            id = ss.find_node_id(nodes[node])
            ss.point_load(id, Fy=-9.81*load/1000)
        ss.solve()
        self.ss = ss
        self.nodes = nodes
        self.connections = connections
        self.loads = loads
        self.supports = supports
        self.pop_mpl = pop_mpl
        self.cross_area = pop_cross_area
        self.compress = pop_compressive_strength
        self.tensile = pop_tensile_strength
    def test(self, verbose=False):
        arr = self.ss.get_element_results()
        forces = [x['N'] for x in arr]
        if (verbose):
            print("Difference between maximum tens. pressure and tensile strength: {}".format(max(forces)/self.cross_area - self.tensile))
            print("Difference between maximum comp. pressure and compressive strength: {}".format(-1*min(forces)/self.cross_area - self.compress))
        return (max(forces)/self.cross_area < self.tensile and -1*min(forces)/self.cross_area < self.compress)
    def change_load(self, old_load_id, new_load):
        id = self.ss.find_node_id(self.nodes[old_load_id])
        self.ss.point_load(id, Fy=-9.81*new_load/1000)

        self.ss.solve()
    def mass(self):
        arr = self.ss.get_element_results()
        length_total = sum([x['length'] for x in arr])
        return length_total * pop_mpl * 1000
    def show(self):
        self.ss.show_structure()
    def stress_test(self, dw):
        for id, load in self.loads:
            self.change_load(id, 0)
        cur_load = 0
        while (self.test()):
            for id, load in self.loads:
                self.change_load(id, cur_load)
            cur_load += dw
        print("{} kg".format(cur_load))

def createPratt(length, height, n):
    dx = length/n
    x = [i*dx for i in range(n+1)] + [i*dx for i in range(1,n)]
    y = [0 for i in range(n+1)] + [height for i in range(1,n)]
    connections = []
    for i in range(1, n):
        connections.append([i, i+n])
    for i in range(0, math.ceil(n/2)):
        connections.append([i, i+n+1])
    for i in range(n, n-math.ceil(n/2), -1):
        connections.append([i, i+n-1])
    connections.extend([[i, i+1] for i in range(n)])
    connections.extend([[i, i+1] for i in range(n+1, 2*n-1)])
    loads = [(math.ceil((3/2)*n), 18.2)]
    supports = [(0), (n)]
    return Bridge(x, y, connections, loads, supports)
def createKTruss(length, height, n):
    dx = length/n
    x = [i*dx for i in range(n+1)] + [i*dx for i in range(1, n)] + [i*dx for i in range(1,n)]
    y = [0 for i in range(n+1)] + [height/2 for i in range(1,n)] + [height for i in range(1,n)]
    connections = []
    for i in range(1,n):
        connections.append([i, i+2*n-1])
    connections.append([0,2*n])
    connections.append([n, 3*n-2])
    connections.extend([[i, i+1] for i in range(n)])
    connections.extend([[i, i+1] for i in range(2*n, 3*n-2)])
    for i in range(n+1, n+math.ceil(n/2)):
        connections.append([i, i+n])
        connections.append([i, i-n+1])
    for i in range(n+math.floor(n/2)+1, 2*n):
        connections.append([i, i+n-2])
        connections.append([i, i-n-1])
    supports = [(0), (n)]
    #loads = [(math.floor((5/2)*n-1), 18.2)]
    loads = [(21,9)]
    print(loads)
    return Bridge(x, y, connections, loads, supports)

k = createKTruss(90.5, 10.2, 9)
k.show()
k.stress_test(0.01)

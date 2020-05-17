from anastruct import SystemElements
import anastruct
import numpy as np

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

pop_cross_area = pop_width * pop_thick
pop_mpl = pop_cross_area * pop_density
g = pop_mpl * 9.81 / 1000
unit_conv = 1

unit_conv = (1/100)

x= [0,10,20,30,40,50,60,70,80,90,10,20,30,40,50,60,70,80,90,0]
y= [0,0,0,0,0,0,0,0,0,0,10.2,10.2,10.2,10.2,10.2,10.2,10.2,10.2,10.2,10.2]
supports= [(0),(9)]

nodes = [[x[i]*unit_conv, y[i]*unit_conv] for i in range(len(x))]

ss = SystemElements(EA = pop_cross_area*8600000)

# bottom horizontal elements
ss.add_element([nodes[0], nodes[1]], element_type='truss', g=g)
ss.add_element([nodes[1], nodes[2]], element_type='truss', g=g)
ss.add_element([nodes[2], nodes[3]], element_type='truss', g=g)
ss.add_element([nodes[3], nodes[4]], element_type='truss', g=g)
ss.add_element([nodes[4], nodes[5]], element_type='truss', g=g)
ss.add_element([nodes[5], nodes[6]], element_type='truss', g=g)
ss.add_element([nodes[6], nodes[7]], element_type='truss', g=g)
ss.add_element([nodes[7], nodes[8]], element_type='truss', g=g)
ss.add_element([nodes[8], nodes[9]], element_type='truss', g=g)

#fixed end vertical elements
ss.add_element([nodes[0], nodes[19]], element_type='truss', g=g)
ss.add_element([nodes[9], nodes[18]], element_type='truss', g=g)

#top deck horiztonal elements
ss.add_element([nodes[19], nodes[10]], element_type='truss', g=g)
ss.add_element([nodes[10], nodes[11]], element_type='truss', g=g)
ss.add_element([nodes[11], nodes[12]], element_type='truss', g=g)
ss.add_element([nodes[12], nodes[13]], element_type='truss', g=g)
ss.add_element([nodes[13], nodes[14]], element_type='truss', g=g)
ss.add_element([nodes[14], nodes[15]], element_type='truss', g=g)
ss.add_element([nodes[15], nodes[16]], element_type='truss', g=g)
ss.add_element([nodes[16], nodes[17]], element_type='truss', g=g)
ss.add_element([nodes[17], nodes[18]], element_type='truss', g=g)

x_mid = [5,15,25,35,45,55,65,75,85,45]
y_mid = [10.2,10.2,10.2,10.2,10.2,10.2,10.2,10.2,10.2,0]

nodes_mid = [[x_mid[i]*unit_conv, y_mid[i]*unit_conv] for i in range(len(x_mid))]

#triangular beams for truss
ss.add_element([nodes[0],nodes_mid[0]], element_type='truss', g=g)
ss.add_element([nodes[1],nodes_mid[0]], element_type='truss', g=g)
ss.add_element([nodes[1],nodes_mid[1]], element_type='truss', g=g)
ss.add_element([nodes[2],nodes_mid[1]], element_type='truss', g=g)
ss.add_element([nodes[2],nodes_mid[2]], element_type='truss', g=g)
ss.add_element([nodes[3],nodes_mid[2]], element_type='truss', g=g)
ss.add_element([nodes[3],nodes_mid[3]], element_type='truss', g=g)
ss.add_element([nodes[4],nodes_mid[3]], element_type='truss', g=g)
ss.add_element([nodes[4],nodes_mid[4]], element_type='truss', g=g)
ss.add_element([nodes[5],nodes_mid[4]], element_type='truss', g=g)
ss.add_element([nodes[5],nodes_mid[5]], element_type='truss', g=g)
ss.add_element([nodes[6],nodes_mid[5]], element_type='truss', g=g)
ss.add_element([nodes[6],nodes_mid[6]], element_type='truss', g=g)
ss.add_element([nodes[7],nodes_mid[6]], element_type='truss', g=g)
ss.add_element([nodes[7],nodes_mid[7]], element_type='truss', g=g)
ss.add_element([nodes[8],nodes_mid[7]], element_type='truss', g=g)
ss.add_element([nodes[8],nodes_mid[8]], element_type='truss', g=g)
ss.add_element([nodes[9],nodes_mid[8]], element_type='truss', g=g)

#vertical beams at midpoints of triangles
ss.add_element([nodes_mid[9],nodes_mid[4]], element_type='truss', g=g)
ss.add_element([nodes[4],nodes[13]], element_type='truss', g=g)
ss.add_element([nodes[5],nodes[14]], element_type='truss', g=g)

for node in supports:
    id = ss.find_node_id(nodes[node])
    ss.add_support_fixed(id)

loads = [(4,9)]

for node, load in loads:
    id = ss.find_node_id(nodes_mid[node])
    ss.point_load(id, Fy=-9.81*load/1000)

ss.solve()

def test(verbose=False):
    arr = ss.get_element_results()
    forces = [x['N'] for x in arr]
    if (verbose):
        print("Difference between maximum tens. pressure and tensile strength: {}".format(max(forces)/pop_cross_area - pop_tensile_strength))
        print("Difference between maximum comp. pressure and compressive strength: {}".format(-1*min(forces)/pop_cross_area - pop_compressive_strength))
    return (max(forces)/pop_cross_area < pop_tensile_strength and -1*min(forces)/pop_cross_area < pop_compressive_strength)
def change_load(old_load_id, new_load):
    id = ss.find_node_id(nodes[old_load_id])
    ss.point_load(id, Fy=-9.81*new_load/1000)

    ss.solve()
def mass():
    arr = ss.get_element_results()
    length_total = sum([x['length'] for x in arr])
    return length_total * pop_mpl * 1000
def show():
    ss.show_structure()
def stress_test(dw):
    for id, load in loads:
        change_load(id, 0)
    cur_load = 0
    while (test()):
        for id, load in self.loads:
            change_load(id, cur_load)
        cur_load += dw
    print("{} kg".format(cur_load))
    print(cur_load)

ss.show_structure()

dw = 0.01

for id, load in loads:
    change_load(old_load_id=id, new_load=0)
cur_load = 0
while (test()):
    for id, load in loads:
        change_load(id, cur_load)
    cur_load += dw
print("{} kg".format(cur_load))
print(cur_load)

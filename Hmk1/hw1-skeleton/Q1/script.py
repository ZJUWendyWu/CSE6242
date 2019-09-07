import http.client
import json
import time
import timeit
import sys
import collections
from pygexf.gexf import *


#
# implement your data retrieval code here
#
#key = sys.argv[1]
key = 'e57cdfa95ea05beef7251eb962f62af3'
part_min = 1150
ordering = '-num_parts'
url = 'https://rebrickable.com/api/v3/lego/sets/?page_size=400&min_parts=' + str(1150) + '&ordering=-num_parts'
connection = http.client.HTTPConnection('rebrickable.com')
connection.request("GET", url,'',{"Accept": "application/json", "Authorization": "key "+key})
result = connection.getresponse()
set_data = result.read().decode()
connection.close()

# decode the data and build LEGO set list
count = set_data.split(",", 3)[0].split(':')[1].strip('"')
results = set_data.split(",", 3)[3]
results = results.split("{")
sets = []
for i in range(1,len(results)):
     set_num = results[i].split(",")[0].split(":")[1].strip("\"")
     set_name = results[i].split(",")[1].split(":")[1].strip("\"")
     if(len(set_num) > 0 and len(set_name) > 0):
        sets.append({"set_num": set_num, "set_name": set_name})

# retrieve parts for LEGO sets
for set in sets:
    parts = []
    part_url = 'https://rebrickable.com/api/v3/lego/sets/' + set.get('set_num') + '/parts/?page_size=1000'
    connection = http.client.HTTPConnection('rebrickable.com')
    connection.request("GET", part_url,'',{"Accept": "application/json", "Authorization": "key "+key})
    result = connection.getresponse()
    part_data = result.read().decode()
    connection.close()
    
    part_data = part_data.split(",",3)[3]
    index = 0
    while part_data.find('part_num') > -1:
        index = part_data.find('part_num')
        part_data = part_data[index :]
        part_num = part_data.split(',', 2)[0].split(':')[1].strip('\"')
        part_name = part_data.split(',', 2)[1].split(':')[1].strip('\"')

        index = part_data.find('rgb')
        part_data = part_data[index :]
        part_color = part_data.split(',', 1)[0].split(':')[1].strip('\"')

        index = part_data.find('quantity')
        part_data = part_data[index :]
        part_quantity = part_data.split(',', 1)[0].split(':')[1].strip('\"')
        parts.append({'part_id': part_num + '_' + part_color, 'part_num': part_num, 'part_name': part_name, 'part_color' : part_color, 'part_quantity': part_quantity})
    parts.sort(key=lambda k: (k.get('part_quantity', 0)), reverse=True)
    if len(parts) > 20:
        parts = parts[:20]
    set['parts'] = parts


#  Build graph
gexf = Gexf("Geyu Wu","Graph for LEGO")
graph=gexf.addGraph("undirected", "static", "A LEGO Graph")

#Define Node attributes
attr_type = graph.addNodeAttribute(title='Type', type='string')

edge_num = 0
for set in sets:
    if(~graph.nodeExists(set.get('set_num'))):
        node = graph.addNode(set.get('set_num'), set.get('set_name'))
        node.addAttribute(attr_type,"set")
        node.setColor('0', '0', '0')
    for part in set.get('parts'):
        if(~graph.nodeExists(part.get('part_id'))):
            node = graph.addNode(part.get('part_id'), part.get('part_name'))
            node.addAttribute(attr_type, "part")
            color = part.get('part_color')
            r = color[:2]
            g = color[2:4]
            b = color[4:6]
            node.setColor(r=r, g=g, b=b)  
            graph.addEdge(str(edge_num), set.get('set_num'), part.get('part_id'), weight=part.get('part_quantity'))
            edge_num += 1
output_file=open("bricks_graph.gexf","wb")
gexf.write(output_file)





# complete auto grader functions for Q1.1.b,d
def min_parts():
    """
    Returns an integer value
    """
    # you must replace this with your own value
    return min_parts

def lego_sets():
    """
    return a list of lego sets.
    this may be a list of any type of values
    but each value should represent one set

    e.g.,
    biggest_lego_sets = lego_sets()
    print(len(biggest_lego_sets))
    > 280
    e.g., len(my_sets)
    """
    # you must replace this line and return your own list
    return sets

def gexf_graph():
    """
    return the completed Gexf graph object
    """
    # you must replace these lines and supply your own graph
    gexf = Gexf("Geyu Wu","Graph for LEGO")
    graph=gexf.addGraph("undirected", "static", "A LEGO Graph")

    #Define Node attributes
    attr_type = graph.addNodeAttribute(title='Type', type='string')

    edge_num = 0
    for set in sets:
     if(~graph.nodeExists(set.get('set_num'))):
          node = graph.addNode(set.get('set_num'), set.get('set_name'))
          node.addAttribute(attr_type,"set")
          node.setColor('0', '0', '0')

     for part in set.get('parts'):
          if(~graph.nodeExists(part.get('part_id'))):
               node = graph.addNode(part.get('part_id'), part.get('part_name'))
               node.addAttribute(attr_type, "part")
               color = part.get('part_color')
               r = color[:2]
               g = color[2:4]
               b = color[4:6]
               node.setColor(r=r, g=g, b=b)  
               graph.addEdge(str(edge_num), set.get('set_num'), part.get('part_id'), weight=part.get('part_quantity'))
               edge_num += 1
    output_file=open("bricks_graph.gexf","wb")
    gexf.write(output_file)
    return gexf.graphs[0]

# complete auto-grader functions for Q1.2.d

def avg_node_degree():
    """
    hardcode and return the average node degree
    (run the function called “Average Degree”) within Gephi
    """
    # you must replace this value with the avg node degree
    return -1

def graph_diameter():
    """
    hardcode and return the diameter of the graph
    (run the function called “Network Diameter”) within Gephi
    """
    # you must replace this value with the graph diameter
    return -1

def avg_path_length():
    """
    hardcode and return the average path length
    (run the function called “Avg. Path Length”) within Gephi
    :return:
    """
    # you must replace this value with the avg path length
    return -1
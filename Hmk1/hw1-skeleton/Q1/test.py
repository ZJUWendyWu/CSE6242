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

import time
start = time.process_time()

#key = sys.argv[1]
key = 'e57cdfa95ea05beef7251eb962f62af3'
part_min = 1150
ordering = '-num_parts'
url = 'https://rebrickable.com/api/v3/lego/sets/?page_size=5&ordering=-num_parts'
connection = http.client.HTTPConnection('rebrickable.com')
connection.request("GET", url,'',{"Accept": "application/json", "Authorization": "key "+key})
result = connection.getresponse()
set_data = result.read().decode()
connection.close()

# decode the data and build LEGO set list
strings = set_data.split(",", 3)
results = set_data.split(",", 3)[3].split("{")
sets = []
for i in range(1,len(results)):
     set_num = results[i].split(",")[0].split(":")[1].strip("\"")
     set_name = results[i].split(",")[1].split(":")[1].strip("\"")
     if(len(set_num) > 0 and len(set_name) > 0):
        sets.append({"set_num": set_num, "set_name": set_name})

# retrieve parts for LEGO sets
for set in sets:
    print(sets.index(set))
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

gexf = Gexf("Geyu Wu","Graph for LEGO")
graph=gexf.addGraph("undirected", "static", "A LEGO Graph")

#Define Node attributes
attr_type = graph.addNodeAttribute(title='Type', type='string')

nodes = {node.id: node for node in graph.nodes}
print(len(nodes))
edge_num = 0
for set in sets:
     if(~graph.nodeExists(set.get('set_num'))):
          node = graph.addNode(set.get('set_num'), set.get('set_name'), r='0', g='0', b='0')
          node.addAttribute(attr_type,"set")

     for part in set.get('parts'):

        if(~graph.nodeExists(part.get('part_id'))):
            color = part.get('part_color')
            node = graph.addNode(part.get('part_id'), 
                                 part.get('part_name'),
                                 r = color[:2],
                                 g = color[2:4],
                                 b = color[4:6])
            node.addAttribute(attr_type, "part")
               
            graph.addEdge(str(edge_num), set.get('set_num'), part.get('part_id'), weight=part.get('part_quantity'))
            edge_num += 1

print(len(nodes))
output_file=open("helloworld.gexf","wb")
gexf.write(output_file)
print(gexf.graphs[0])

# # test GexfImport
# f = open("gexf.net.dynamics_openintervals.gexf")
# gexf_import = Gexf.importXML(f)
# f.close()
# f = open("gexf.net.dynamics_openintervals.gexf")
# gexf_import2 = Gexf.importXML(f)
# f.close()
# print "test gexf comparision "+str(gexf_import==gexf_import2)



# graph=gexf_import.graphs[0]
# # display nodes list 
# for node_id,node in graph.nodes.iteritems() : 
#     print node.label
#     pprint.pprint(node.getAttributes(),indent=1,width=1)

# # display edges list 
# for edgeid,edge in graph.edges.iteritems() : 
#     print str(graph.nodes[edge.source])+" -> "+str(graph.nodes[edge.target])
#     pprint.pprint(edge.getAttributes(),indent=1,width=1)


# o = open("gexf.net.dynamics_openintervals_copied.gexf", "w")

# gexf_import.write(o)


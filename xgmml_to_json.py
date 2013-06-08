### http://cytoscape.github.io/cytoscape.js/#notation/elements-json
### https://github.com/bendtherules/GSOC_13/blob/master/nnf_and_sif_to_json_py/result.json
from bs4 import BeautifulSoup
import json
from collections import OrderedDict



def get_position(xline):
    position = xline.find_all("graphics")
    x = position[0].get("x")
    y = position[0].get("y") 
    return x,y


class NodeLine(object):
    _slots_ = ("id","name","x","y","group")

    def __init__(self, xline):
        self.group = "nodes"
        self.cid = xline.get("id")
        self.name = xline.get("label")
        self.x, self.y = get_position(xline)


class EdgeLine(object):
    _slots_ = ("name","target","source","x","y","group")

    def __init__(self, xline):
        self.group = "edge"
        self.name = xline.get("label")
        self.source = xline.get("source")
        self.target = xline.get("target")
        self.x, self.y = get_position(xline)



class Element(object):

    def __init__(self,filename):
        self.filename = filename
        self.nformat = 'nodes: [ \n'
        self.eformat = '\n ],\n edges: [\n'

        fh = open(filename)
        xgmml = fh.read()
        soup = BeautifulSoup(xgmml)

        for nline in soup.find_all("node"):
            node = NodeLine(nline)
            ## need to use double brackets with bracket
            njson = "{{ data: {{id: '{0}', name: '{1}'}}, position: {{x: {2}, y:{3}}}}},\n".format(node.cid, node.name, node.x, node.y)
            self.nformat = self.nformat + njson


        for eline in soup.find_all("edge"):
            edge = EdgeLine(eline)
            ejson = "{{ data: {{id: '{0}', source: '{1}', target: '{2}'}}}},\n".format(edge.name,edge.source,edge.target)
            self.eformat = self.eformat + ejson

def main(xgmml_file):
    cyto = Element(xgmml_file)
    jsonformat = cyto.nformat[:-2] + cyto.eformat[:-2] + "\n ] \n },\n"
    print jsonformat

main("fe_minus_subset_stric_arrow.xgmml")

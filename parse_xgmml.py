from bs4 import BeautifulSoup


def getheader(xgmml,outfile):
    """copies the the header from the imput file, thus copies everything up
    till the term node """
    for line in xgmml.split("\n"):
        if "node" in line: break
        outfile.write(line + "\n")

def writetofile(des,outfile,arrow):
    """write to outfile goes through each line of section and adds tabs. Before
    tabing was off when attpt to just write back to file. Also adds arrow info
    in edge"""
    for line in str(des).split("\n"):
        line = str(line)
        if "node" not in line and "edge" not in line:
            ## tabing was okay for headers and ends
            if arrow and "<graphics" in line:
                # if graphics and a edge line add arrow info
                line = line.split("></")[0]
                line = line.split("<graphics")[0]
                line = "\t" + line  +  arrow +  "/>"
            else:
                ## just fix tabbing
                line = line.split("></")[0]
                line = "\t" + line + "/>"

        outfile.write("\t" + line + "\n")

def match_nodes(soup, my_subset, outfile):
    """creates a list of nodes from the xgmml file. for each node in file if
    the node is also in mysubset then its added to a the new xgmml file  """
    arrow = False
    ## only need arrow info when an edge
    for nodes in soup.find_all("node"):
        gene = nodes.get("label")
        if gene in my_subset:
            writetofile(nodes,outfile,arrow)

def match_edge(soup, my_subset, outfile,corr_dic):
    """creates a list of all the edges in xgmml file. For each edge if both
    genes are present in my subset list then it adds it to the new xgmml file"""
    seen = []
    for edges in soup.find_all("edge"):
        connected_genes = edges.get("label")
        gene1,gene2 = connected_genes.split(" (pd) ")
        if gene1 in my_subset and gene2 in my_subset:
            arrow = getarrow(gene1,gene2,corr_dic)
            writetofile(edges,outfile,arrow)
    
def getarrow(gene1, gene2,corr_dic):
    """returns cytoscape code for adding an arrow to the image"""
    try:
        key = "{0}_{1}".format(gene1,gene2)
        corr = corr_dic[key]
    except KeyError:
        key = "{0}_{1}".format(gene2,gene1)
        corr = corr_dic[key]
    if abs(corr) >= 0.7:
        if corr < 0:
            arrow = "<graphics fill=\"#771100\" width=\"2\" cy:sourceArrow=\"0\" cy:targetArrow=\"15\""
            ## T bone arrow/ inhibt arrow and red
        else:
            arrow = "<graphics fill=\"#99CC00\" width=\"2\" cy:sourceArrow=\"0\" cy:targetArrow=\"6\""
            ### arrow marking up regulated and green
    else:
        arrow = "<graphics fill=\"#999999\" width=\"2\" cy:sourceArrow=\"0\" cy:targetArrow=\"0\""
        ## no arrow if correlation greater than .7 and grey

    return arrow

def parse_corr(corr_fh):
    """parse corr file to create dic TODO to have this outputed as std format"""
    corr_dic = {}
    for line in open(corr_fh):
        gene1,gene2,corr = line.split("\t")
        key = "{0}_{1}".format(gene1,gene2)
        #print float(corr)
        corr_dic[key] = float(corr)
    return corr_dic

def main(xgmml_file, my_subset, outfh, corr_fh):
    fh = open(xgmml_file)
    corr_dic = parse_corr(corr_fh)
    xgmml = fh.read()
    soup = BeautifulSoup(xgmml)
    outfile = open(outfh, "wb")
    header = getheader(xgmml,outfile)
    match_nodes(soup,my_subset,outfile)
    match_edge(soup,my_subset,outfile,corr_dic)
    outfile.write("</graph>\n")
    outfile.close()






main("Sheet1.xgmml", new_network_list, "fe_minus_subset_stric_arrow.xgmml","fe_cyto_corr.tsv")


import pandas as pd
import json
import pickle
import zipfile
import networkx as nx
from time import time
import numpy as np

def createJSON(data):

    jsonData = {"Name" : "flare", "children" : []}

    check = set([])

    for index, row in data.iterrows():
        people = row.People if pd.notna(row.People) else "Empty"
        try:
            size = row.publications if pd.notna(row.publications) else len(row.People.split(',')) * 10
        except AttributeError:
            size = row.publications if pd.notna(row.publications) else 2
        if row.modules not in check and pd.notna(row.modules):
            jsonData["children"].append({"name":row.modules, "children": []})
            check.add(row.modules)

        for mod in jsonData["children"]:
            for discipline in row.discipline.split(','):
                for subdiv in row.subdivision.split(','):
                    if discipline not in check and mod["name"] == row.modules and pd.notna(discipline):
                        mod["children"].append({"name":discipline, "children": []})
                        check.add(discipline)
                    elif not pd.notna(discipline) and mod["name"] == row.modules:
                        try:
                            mod["children"].append({"name":subdiv, "children":[], "size":size, "people":[people.split(',')]})

                        except AttributeError:
                            mod["children"].append({"name":subdiv, "children":[], "size":row.publications, "people":[people]})
                    elif discipline == "Undefined" and mod["name"] == row.modules:
                        mod["children"].append({"name":subdiv, "children":[], "size":size, "people":[people]})        

                    for disc in mod["children"]:
                        if subdiv not in check and disc["name"] == discipline and pd.notna(subdiv):
                            try:
                                disc["children"].append({"name":subdiv, "children":[], "size":size, "people":[people.split(',')]})
                            except AttributeError:
                                disc["children"].append({"name":subdiv, "children":[], "size":size, "people":[people]})

    for listItems in jsonData["children"]:
        for module in listItems["children"]:
            try:
                try:
                    for person in module["people"][0].split(","):
                        module["children"].append({"name": person, "size":20})
                except AttributeError:
                    module["children"].append({"name": module["people"][0][0], "size":20})
            except KeyError:
                for subdomain in module["children"]:
                    try:
                        try:
                            for person in subdomain["people"][0]:
                                subdomain["children"].append({"name": person, "size":20})
                        except AttributeError:
                            subdomain["children"].append({"name": subdomain["people"][0], "size":20})
                    except KeyError:
                        pass
                    
    return jsonData


def convert(input):
    if isinstance(input, dict):
        return {convert(key): convert(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [convert(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input


class adjacencyData:
    def __init__(self, G):
        self.var = G.nodes
        self.thresholdIndex = []
        for node in G.nodes:
            try:
                temp = {node : G.nodes[node]["sensitivity"]}
                self.thresholdIndex.append(temp)
            except KeyError:
                pass
        self.adjacencyMatrix = nx.to_numpy_matrix(G)
        self.graphData = G
        
    def plotGraph(self):
        elarge = [(u, v) for (u, v, d) in self.graphData.edges(data=True) if d['weight'] > 0.5]
        esmall = [(u, v) for (u, v, d) in self.graphData.edges(data=True) if d['weight'] <= 0.5]

        pos = nx.spring_layout(self.graphData)  # positions for all nodes
        nx.draw_networkx_nodes(self.graphData, pos, node_size=100)
        nx.draw_networkx_edges(self.graphData, pos, edgelist=elarge, width=2)
        nx.draw_networkx_edges(self.graphData, pos, edgelist=esmall, width=1, alpha=0.5, edge_color='b')
        nx.draw_networkx_labels(self.graphData, pos, font_size=10, font_family='sans-serif')

        plt.axis('off')
        plt.show()

def get_G(data):
    print("&&&&&&&&&&&&&&&&&&&&WHOLEOEOEO&&&&&&&&&&&&&&&&&")
    for ding in data["edges"]["_data"].keys():
        print(ding)
        print(data["edges"]["_data"][ding].keys())
    G = nx.DiGraph()
    data = convert(data)
    G.add_nodes_from([(data["nodes"]["_data"][node]["id"], {"sensitivity": data["nodes"]["_data"][node]["sensitivity"]}) for node in data["nodes"]["_data"]])
    edges = [(int(data["edges"]["_data"][node]["from"]), int(data["edges"]["_data"][node]["to"]), {"weight":data["edges"]["_data"][node]["con_strength"]}) if data["edges"]["_data"][node]["con_strength"] != "None" else (int(data["edges"]["_data"][node]["from"]), int(data["edges"]["_data"][node]["to"]), {"weight":1}) for node in data["edges"]["_data"]]
    G.add_edges_from(edges)
    adjaData = adjacencyData(G)

    return adjaData


def pkl_exp(data, filepath):
    filenames = [filepath + "weightParameters.txt", filepath + "thresholdParameters.txt"]
    G = nx.DiGraph()
    data = convert(data)
    print(data["edges"][data["edges"].keys()[0]].keys())
    legendNodes = [node for node in data["nodes"].keys() if int(node) > 999]
    for node in legendNodes: del data["nodes"][node]
    G.add_nodes_from([(data["nodes"][node]["id"], {"threshold": data["nodes"][node]["sensitivity_id"]}) for node in data["nodes"]])
    edges = [(int(data["edges"][node]["from"]), int(data["edges"][node]["to"]), {"weight":data["edges"][node]["con_strength"]}) if data["edges"][node]["con_strength"] != "None" else (int(data["edges"][node]["from"]), int(data["edges"][node]["to"]), {"weight":1}) for node in data["edges"]]
    G.add_edges_from(edges)
    graphData = adjacencyData(G)
    
    nx.write_gpickle(graphData.graphData, filepath + 'depression_network.pkl')

    weightStr = ""
    file = open(filepath + "weightParameters.txt", "w")
    weightStr += "\t".join([data["nodes"][str(d)]["label"] for d in graphData.var]) + "\n"
    for row in graphData.adjacencyMatrix.tolist():
        weightStr += "\t".join(['{:.1f}'.format(x) for x in row])+"\n"
    file.write(weightStr)
    file.close()

    threshStr = ""
    file = open(filepath + "thresholdParameters.txt", "w")
    threshStr += "var,threshold\n"
    for k in graphData.thresholdIndex:
        threshStr += str(k.keys()[0]) + ", " + str(k[k.keys()[0]]) + "\n"
    file.write(threshStr)
    file.close()
    return filenames, "text"
        
def json_exp(data, filepath):
    with open(filepath + 'depression_network.json', 'wb') as fp:
        json.dump(data, fp)
    return "depression_network.json", "text/json"
        
# def xlsx_exp(data):
#     sheets = ["edges", "nodes"]
#     writer = pd.ExcelWriter('app/static/data/depression_network.xlsx')

#     for sheet in sheets:
#         reformat = {}
#         for entry in data[sheet]:
#             for key in data[sheet][entry]:
#                 reformat.setdefault(key, []).append(data[sheet][entry][key])
#         pd.DataFrame.from_dict(reformat).to_excel(writer,sheet)
#     writer.save()
#     return "depression_network.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    

def csv_exp(data, filepath):
    sheets = ["edges", "nodes"]
    filenames = []
    for sheet in sheets:
        filename = filepath + 'depression_network_' + sheet + '.csv'
        reformat = {}
        for entry in data[sheet]:
            if sheet == "nodes" and int(entry) > 999:
                continue
            else:
                for key in data[sheet][entry]:
                    reformat.setdefault(key, []).append(data[sheet][entry][key])
        pd.DataFrame.from_dict(reformat).to_csv(filename, sep=',')
        filenames.append(filename)
    return filenames, "text/csv"

        
def export_network_data(data, filepath):
    if data["format"] == "pkl":
        filenames, contentType = pkl_exp(data, filepath)
    elif data["format"] == "json":
        filenames, contentType = json_exp(data, filepath)
    elif data["format"] == "csv":
        filenames, contentType = csv_exp(data, filepath)
    elif data["format"] == "xlsx":
        filenames, contentType = xlsx_exp(data, filepath)
    return filenames, contentType


def give_arrows(value):
    if value < 3:
        return { "to": { "enabled": True, "type": 'bar' }}
    elif value > 3:
        return "to"
    elif value == 3:
        return { "to": { "enabled": True, "type": 'circle' }}


def give_strength(value):
    if value == 1 or value == 5:
        return 3
    elif value == 2 or value == 4:
        return 2
    elif value == 3:
        return 0.5

def give_dashes():
    randy = np.random.uniform(0,1)
    print(randy)
    if randy < 0.5:
        return [5,5]
    else:
        return False
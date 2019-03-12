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
            if row.discipline not in check and mod["name"] == row.modules and pd.notna(row.discipline):
                mod["children"].append({"name":row.discipline, "children": []})
                check.add(row.discipline)
            elif not pd.notna(row.discipline) and mod["name"] == row.modules:
                try:
                    mod["children"].append({"name":row.subdivision, "children":[], "size":size, "people":[people.split(',')]})

                except AttributeError:
                    mod["children"].append({"name":row.subdivision, "children":[], "size":row.publications, "people":[people]})
            elif row.discipline == "Undefined" and mod["name"] == row.modules:
                mod["children"].append({"name":row.subdivision, "children":[], "size":size, "people":[people]})        
            
            for disc in mod["children"]:
                if row.subdivision not in check and disc["name"] == row.discipline and pd.notna(row.subdivision):
                    try:
                        disc["children"].append({"name":row.subdivision, "children":[], "size":size, "people":[people.split(',')]})
                    except AttributeError:
                        disc["children"].append({"name":row.subdivision, "children":[], "size":size, "people":[people]})


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
                temp = {node : G.nodes[node]["threshold"]}
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
    G = nx.DiGraph()
    data = convert(data)
    G.add_nodes_from([(data["nodes"]["_data"][node]["id"], {"threshold": data["nodes"]["_data"][node]["threshold"]}) for node in data["nodes"]["_data"]])
    edges = [(int(data["edges"]["_data"][node]["from"]), int(data["edges"]["_data"][node]["to"]), {"weight":data["edges"]["_data"][node]["value"]}) if data["edges"]["_data"][node]["value"] != "None" else (int(data["edges"]["_data"][node]["from"]), int(data["edges"]["_data"][node]["to"]), {"weight":1}) for node in data["edges"]["_data"]]
    G.add_edges_from(edges)
    adjaData = adjacencyData(G)

    return adjaData


def pkl_exp(data):
    filenames = ["app/static/data/weightParameters.txt", "app/static/data/thresholdParameters.txt"]
    G = nx.DiGraph()
    data = convert(data)
    G.add_nodes_from([(data["nodes"][node]["id"], {"threshold": data["nodes"][node]["threshold"]}) for node in data["nodes"]])
    edges = [(int(data["edges"][node]["from"]), int(data["edges"][node]["to"]), {"weight":data["edges"][node]["relation_weight"]}) if data["edges"][node]["relation_weight"] != "None" else (int(data["edges"][node]["from"]), int(data["edges"][node]["to"]), {"weight":1}) for node in data["edges"]]
    G.add_edges_from(edges)
    graphData = adjacencyData(G)
    
    nx.write_gpickle(graphData.graphData, 'app/static/data/depression_network.pkl')

    weightStr = ""
    file = open("app/static/data/weightParameters.txt", "w")
    weightStr += "\t".join([data["nodes"][str(d)]["label"] for d in graphData.var]) + "\n"
    for row in graphData.adjacencyMatrix.tolist():
        weightStr += "\t".join(['{:.1f}'.format(x) for x in row])+"\n"
    file.write(weightStr)
    file.close()

    threshStr = ""
    file = open("app/static/data/thresholdParameters.txt", "w")
    threshStr += "var,threshold\n"
    for k in graphData.thresholdIndex:
        threshStr += str(k.keys()[0]) + ", " + str(k[k.keys()[0]]) + "\n"
    file.write(threshStr)
    file.close()
    return filenames, "text"
        
def json_exp(data):
    with open('app/static/data/depression_network.json', 'wb') as fp:
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
    

def csv_exp(data):
    sheets = ["edges", "nodes"]
    filenames = []
    for sheet in sheets:
        filename = 'app/static/data/depression_network_' + sheet + '.csv'
        reformat = {}
        for entry in data[sheet]:
            for key in data[sheet][entry]:
                reformat.setdefault(key, []).append(data[sheet][entry][key])
        pd.DataFrame.from_dict(reformat).to_csv(filename, sep=',')
        filenames.append(filename)
    return filenames, "text/csv"

        
def export_network_data(data):
    if data["format"] == "pkl":
        filenames, contentType = pkl_exp(data)
    elif data["format"] == "json":
        filenames, contentType = json_exp(data)
    elif data["format"] == "csv":
        filenames, contentType = csv_exp(data)
    elif data["format"] == "xlsx":
        filenames, contentType = xlsx_exp(data)
    return filenames, contentType


def simulation_1(W, b, I, c, select = np.ones(14, np.bool)):
    I = int(I)
    c = float(c)
    b_ = b.copy()
    b_[~select] = 100

    X = np.zeros((I, b.shape[0]), np.bool)
    P = np.zeros((I, b.shape[0]), np.float32)
    D = np.zeros((I), np.uint8)

    for i in range(1, I):
        A = np.sum(c * W * X[i-1], axis=1)
        P[i] = 1 / (1 + np.exp(b_ - A))
        X[i] = P[i] > np.random.uniform(0, 1, b.shape)
        D[i] = np.sum(X[i])
    return X, P, D


def simulation_2(W, b, I, c, select = np.ones(14, np.bool)):
    I = int(I)
    c = float(c)
    I2 = I//2

    b_ = b.copy()
    b_[~select] = 100

    X = np.zeros((I, b.shape[0]), np.bool)
    P = np.zeros((I, b.shape[0]), np.float32)
    D = np.zeros((I), np.uint8)
    S = np.concatenate((np.linspace(-10, 5, I2), np.linspace(5, -10, I2)))

    for i in range(1, I):
        A = np.sum(c * W * X[i-1] + S[i], axis=1)
        P[i] = 1 / (1 + np.exp(b_ - A))
        X[i] = P[i] > np.random.uniform(0, 1, b.shape)
        D[i] = np.sum(X[i])
    return S[:I2].tolist(), [X[:I2].tolist(), P[:I2].tolist(), D[:I2].tolist()], [X[I2:][::-1].tolist(), P[I2:][::-1].tolist(), D[I2:][::-1].tolist()]

def sim_div(message):
    parameters = json.loads(message)
    gData = get_G(parameters["data"])
    W = np.asarray(gData.adjacencyMatrix)
    b = np.abs(np.asarray([k[k.keys()[0]] for k in gData.thresholdIndex]))
    simulation, I, c = parameters['simulation'], int(parameters['I']), float(parameters['c'])

    t0 = time()
    if simulation == 1:
        if 'select' in parameters:
            select = np.array(parameters['select'], np.bool)
            X, P, D = simulation_1(W, b, I, c, select)
        else:
            X, P, D = simulation_1(W, b, I, c)
        data = json.dumps({"simulation": 1, "X": X.tolist(), "P": P.tolist(), "D": D.tolist()})
        return data

    if simulation == 2:
        if 'select' in parameters:
            select = np.array(parameters['select'], np.bool)
            S, (UP_X, UP_P, UP_D), (DOWN_X, DOWN_P, DOWN_D) = simulation_2(W, b, I, c, select)
        else:
            S, (UP_X, UP_P, UP_D), (DOWN_X, DOWN_P, DOWN_D) = simulation_2(W, b, I, c)

        data = json.dumps({
            "simulation": 2,
            "S": S,
            "UP": {"X": UP_X, "P": UP_P, "D": UP_D},
            "DOWN": {"X": DOWN_X, "P": DOWN_P, "D": DOWN_D}})
        return data

def give_arrows(value):
    if value < 0:
        return { "to": { "enabled": True, "type": 'bar' }}
    elif value > 0:
        return "to"
    elif value == 0:
        return { "to": { "enabled": True, "type": 'circle' }}


def give_dashes():
    randy = np.random.uniform(0,1)
    print(randy)
    if randy < 0.5:
        return [5,5]
    else:
        return False
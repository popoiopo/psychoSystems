import json
import os
from flask import Flask, render_template, jsonify, request, url_for
import pandas as pd
import numpy as np
from time import time
import os

# __file__ refers to the file settings.py 
APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
APP_STATIC = os.path.join(APP_ROOT, 'static')

# Load Weight & Threshold Files
W_PATH = APP_STATIC + '/website/data/EmpiricalWeightParameters.txt'
b_PATH = APP_STATIC + '/website/data/EmpiricalThresholdParameters.txt'
W = np.asarray(pd.read_csv(W_PATH, delimiter='\t', encoding='utf-8'))
b = np.abs(np.asarray(pd.read_csv(b_PATH, delimiter=',', encoding='utf-8').set_index("var"))).ravel()

print("******************DEBUGGING!!!**********************")
print(W)
print(b)

app = Flask(__name__)

def simulation_1(I, c, select = np.ones(14, np.bool)):
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


def simulation_2(I, c, select = np.ones(14, np.bool)):
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
    simulation, I, c = parameters['simulation'], int(parameters['I']), float(parameters['c'])

    t0 = time()
    if simulation == 1:
        if 'select' in parameters:
            select = np.array(parameters['select'], np.bool)
            X, P, D = simulation_1(I, c, select)
        else:
            X, P, D = simulation_1(I, c)
        data = json.dumps({"simulation": 1, "X": X.tolist(), "P": P.tolist(), "D": D.tolist()})
        return data

    if simulation == 2:
        if 'select' in parameters:
            select = np.array(parameters['select'], np.bool)
            S, (UP_X, UP_P, UP_D), (DOWN_X, DOWN_P, DOWN_D) = simulation_2(I, c, select)
        else:
            S, (UP_X, UP_P, UP_D), (DOWN_X, DOWN_P, DOWN_D) = simulation_2(I, c)

        data = json.dumps({
            "simulation": 2,
            "S": S,
            "UP": {"X": UP_X, "P": UP_P, "D": UP_D},
            "DOWN": {"X": DOWN_X, "P": DOWN_P, "D": DOWN_D}})
        return data


@app.route('/_add_numbers')
def add_numbers():
    a = request.args.get('a', "", type=str)
    data = sim_div(a)
    return jsonify(data)

@app.route("/fut_exp")
def fut_exp():
    return render_template("fut_exp.html")

@app.route("/sim1")
def sim1():
    return render_template("sim1.html")

if __name__ == "__main__":
    app.run(port=8000, debug=True)
    



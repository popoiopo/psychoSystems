# app/home/views.py

from flask import abort, render_template, request, jsonify, send_from_directory, make_response, send_file, Response
from ..models import Expert, Factor, Operator, Node, Edge, Temp_imp, Spat_aspect, Temp_aspect, pageTexts, Sensitivity, Con_strength
from flask_login import current_user, login_required
from helpers import createJSON, export_network_data, convert, give_arrows, give_dashes, give_strength
from requests_toolbelt import MultipartEncoder
from forms import NodeForm
from . import home
from .. import db
from ..models import Node, Edge
from sqlalchemy import text

import pandas as pd
import numpy as np
import pickle
from random import randint, choice
import json
import zipfile
import os
import io
import re
import pathlib


@home.route('/')
def homepage():
    """
    Render the homepage template on the / route
    """

    pagesClassIDs = {
        "index": {
            "bannertitle": [],
            "subtitle": [],
            "firstText": [],
            "secondText": []
        }
    }
    for key in pagesClassIDs["index"].keys():
        pagesClassIDs["index"][key].append(
            str(
                pageTexts.query.filter_by(pageID=key,
                                          htmlName="index").first()))

    experts = Expert.query.all()
    data = {
        "modules": [],
        "discipline": [],
        "subdivision": [],
        "publications": [],
        "People": []
    }
    for expert in experts:
        if not expert.is_admin and str(expert.accepted) == "Yes":
            data["modules"].append(str(expert.affiliation))
            data["discipline"].append(str(expert.discipline))
            data["subdivision"].append(str(expert.specialization))
            data["publications"].append(0)
            if str(expert.core_exp) == "Yes":
                data["People"].append(
                    str(expert.title) + " " + str(expert.first_name) + " " +
                    str(expert.last_name) + "(T)")
            else:
                data["People"].append(
                    str(expert.title) + " " + str(expert.first_name) + " " +
                    str(expert.last_name) + "(N)")

    crdata = pd.DataFrame(data).groupby(
        ['modules', 'discipline', 'subdivision'], as_index=False).agg({
            'publications':
            'sum',
            'People':
            lambda x: ','.join(x)
        })
    circleData = createJSON(crdata)

    return render_template(
        'home/index.html',
        pageDicts=pagesClassIDs,
        bannertitle="Introduction to Research",
        subtitle="Interactive Causal Mapping",
        title="Home",
        circleData=circleData)


@home.route('/fase1')
@login_required
def fase1():
    """
    Render the fase1 template on the /fase1 route
    """

    pagesClassIDs = {
        "fase1": {
            "bannertitle": [],
            "subtitle": [],
            "firstText": [],
            "secondText": []
        }
    }
    for key in pagesClassIDs["fase1"].keys():
        pagesClassIDs["fase1"][key].append(
            str(
                pageTexts.query.filter_by(pageID=key,
                                          htmlName="fase1").first()))

    spat_aspects = Spat_aspect.query.all()
    spat_aspectsList = [
        spat_aspect.__dict__["name"] for spat_aspect in spat_aspects
    ]

    temp_aspects = Temp_aspect.query.all()
    temp_aspectsList = [
        temp_aspect.__dict__["name"] for temp_aspect in temp_aspects
    ]

    nodes = Node.query.all()
    nodesList = [node.__dict__ for node in nodes]
    for nd in nodesList:
        del nd['_sa_instance_state']

    factorDict = {}
    for node in nodesList:
        spat_asp = int(node["spat_aspect_id"]) - 1
        temp_asp = int(node["temp_aspect_id"]) - 1
        factorDict.setdefault(spat_aspectsList[spat_asp], {})
        factorDict[spat_aspectsList[spat_asp]].setdefault(
            temp_aspectsList[temp_asp], [])
        factorDict[spat_aspectsList[spat_asp]][
            temp_aspectsList[temp_asp]].append(node["factor"])

    print(nodesList)
    print(factorDict)

    return render_template(
        'home/fase1.html',
        factorDict=factorDict,
        nodes=nodesList,
        spat_aspects=spat_aspectsList,
        temp_aspects=temp_aspectsList,
        pageDicts=pagesClassIDs,
        title="fase1")


@home.route('/fase2')
@login_required
def fase2():
    """
    Render the fase2 template on the /fase2 route
    """
    pagesClassIDs = {
        "fase2": {
            "bannertitle": [],
            "subtitle": [],
            "firstText": [],
            "secondText": []
        }
    }
    for key in pagesClassIDs["fase2"].keys():
        pagesClassIDs["fase2"][key].append(
            str(
                pageTexts.query.filter_by(pageID=key,
                                          htmlName="fase2").first()))

    nodes = Node.query.all()
    nodesList2 = {node.__dict__["id"] : node.__dict__ for node in nodes}
    nodesList = [node.__dict__ for node in nodes]
    for nd in nodesList:
        del nd['_sa_instance_state']


    edges = Edge.query.all()
    edgesList = [edge.__dict__ for edge in edges]
    for ed in edgesList:
        del ed['_sa_instance_state']

    sankeyData = {}
    sankeyData["links"] = [{"source":nodesList2[edge["factor_A"]]["factor"], "target":nodesList2[edge["factor_B"]]["factor"], "value":edge["con_strength_id"]*10,"optimal":"yes"} for edge in edgesList]

    nodeSet = set()
    for link in sankeyData["links"]:
        nodeSet.add(link["source"])
        nodeSet.add(link["target"])
    sankeyData["nodes"] = [{"name":node} for node in nodeSet]

    con_strengths = Con_strength.query.all()
    temp_aspects = Temp_aspect.query.all()
    spat_aspects = Spat_aspect.query.all()

    print(temp_aspects)

    dropDowns = {
        "temp_aspects": [str(x) for x in temp_aspects],
        "spat_aspects": [str(x) for x in spat_aspects],
        "con_strengths": [str(x) for x in con_strengths]
    }

    return render_template(
        'home/fase2.html',
        pageDicts=pagesClassIDs,
        dropDowns=dropDowns,
        nodes=nodesList,
        edges=edgesList,
        sankeyData=sankeyData,
        title="fase2")


@home.route('/fase3')
def fase3():
    """
    Render the fase3 template on the / route
    """

    pagesClassIDs = {
        "fase3": {
            "bannertitle": [],
            "subtitle": [],
            "firstText": [],
            "secondText": [],
            "thirdText": []
        }
    }
    for key in pagesClassIDs["fase3"].keys():
        pagesClassIDs["fase3"][key].append(
            str(
                pageTexts.query.filter_by(pageID=key,
                                          htmlName="fase3").first()))

    shapes = [
        "triangle", "square", "diamond", "triangle", "square", "diamond",
        "triangle", "square", "diamond"
    ]
    colors = [
        '#d53e4f', '#f46d43', '#fdae61', '#fee08b', '#e6f598', '#abdda4',
        '#66c2a5', '#3288bd', '#ffffbf'
    ]

    nodes = Node.query.all()
    edges = Edge.query.all()
    temp_imps = Temp_imp.query.all()
    spat_aspects = Spat_aspect.query.all()
    temp_aspects = Temp_aspect.query.all()
    sensitivities = Sensitivity.query.all()
    con_strengths = Con_strength.query.all()
    operators = Operator.query.all()
    experts = Expert.query.all()

    acceptedList = [
        expert.id for expert in experts if str(expert.accepted) == "Yes"
    ]
    dist_ops = Operator.query.distinct(Operator.name)
    op_dict = {str(x): shapes[i] for i, x in enumerate(dist_ops)}
    cl_dict = {str(x): colors[i] for i, x in enumerate(dist_ops)}

    dropDowns = {
        "type": op_dict.keys(),
        "temp_imps": [str(x) for x in temp_imps],
        "spat_aspects": [str(x) for x in spat_aspects],
        "temp_aspects": [str(x) for x in temp_aspects],
        "sensitivity_id": [str(x) for x in sensitivities],
        "con_strengths": [str(x) for x in con_strengths],
        "operators": [str(x) for x in operators]
    }

    randicon = ["onset", "maintenance", "relapse"]
    # randicon = ["stock", "cloud", "unknown", "onset", "maintenance", "relapse"]
    # randicon = ["variable", "stock", "cloud", "unknown"]

    data = {"nodes": [], "edges": []}
    data["nodes"] = [{
        "id": int(node.id),
        "sensitivity_id": int(node.sensitivity_id),
        "spat_aspect_id": str(node.spat_aspect_id),
        "temp_aspect_id": str(node.temp_aspect_id),
        "temp_imp_id": str(node.temp_imp_id),
        "notes": str(node.notes),
        "notes_factor": str(node.notes_factor),
        "created_date": str(node.created_date),
        "font": {
            "multi": 'html',
            "size": 20,
            "color": 'black',
            "bold": True
        },
        "label": '<b>'+str(node.factor).replace("_", "</b>\n<b>")+'</b>',
        "group": str(node.temp_aspect_id),
        "x": None,
        "y": None,
        "value": int(node.sensitivity_id),
        "sup_lit": None,
        "fixed": False,
        "physics": True,
        "level": node.temp_aspect_id
    } for node in nodes]


    data["edges"] = []
    for edge in edges:
        fromIndex = next((index for (index, d) in enumerate(data["nodes"]) if d["id"] == edge.factor_A), None)
        toIndex = next((index for (index, d) in enumerate(data["nodes"]) if d["id"] == edge.factor_A), None)

        if data["nodes"][fromIndex]["temp_aspect_id"] != data["nodes"][
                toIndex]["temp_aspect_id"]:
            smoothType = "continous"
        else:
            smoothType = "curvedCW"

        data["edges"].append({
            "arrows": give_arrows(edge.con_strength_id),
            "dashes": bool(1),
            "from": str(edge.factor_A),
            "to": str(edge.factor_B),
            "id": int(edge.id),
            "created_date": str(edge.created_date),
            "value": give_strength(edge.con_strength_id),
            "temp_imp_id": str(edge.temp_imp_id),
            "temp_aspect_id": str(edge.temp_aspect_id),
            "con_strength":int(edge.con_strength_id),
            "operator_id": str(edge.operator_id),
            "notes_relation": str(edge.notes_relation),
            "sup_lit": str(edge.sup_lit),
            "smooth": {
                "type": smoothType,
                "forceDirection": 'vertical',
                "roundness": 0.4
            }
        })

    for index, group in enumerate(dropDowns["temp_aspects"]):
        data["nodes"].append({"id": 1000 + index, 
                              "x": -1000, 
                              "y": index * 100, 
                              "font":{"multi": 'html',
                                      "size": 24,
                                      "color": 'black',
                                      "bold": True}, 
                              "notes":"This is just a Legend Node",
                              "notes_factor":"LegendNode999",
                              "sup_lit":None,
                              "created_date":None,
                              "label": group, 
                              "group": str(index+1), 
                              "sensitivity": None,
                              "temp_aspect_id": None,
                              "temp_imp_id": None,
                              "value": 7, 
                              "fixed": True, 
                              "level": str(index+1),
                              "physics":False})

    return render_template(
        'home/fase3.html',
        pageDicts=pagesClassIDs,
        dropDowns=dropDowns,
        causalData=data,
        op_dict=op_dict,
        cl_dict=cl_dict,
        title="fase3")


@home.route('/_add_numbers')
def add_numbers():
    a = request.args.get('a', "", type=str)
    data = sim_div(a)
    print(data)
    return jsonify(data)


@home.route('/admin/dashboard')
@login_required
def admin_dashboard():
    # prevent non-admins from accessing the page
    if not current_user.is_admin:
        abort(403)

    return render_template(
        'home/admin_dashboard.html',
        bannertitle="Welcome Admin",
        subtitle="A place to display your admin powers",
        title="AdminDashboard")


@home.route('/admin/presentation')
@login_required
def admin_presentation():
    # prevent non-admins from accessing the page
    if not current_user.is_admin:
        abort(403)

    shapes = [
        "triangle", "square", "diamond", "triangle", "square", "diamond",
        "triangle", "square", "diamond"
    ]
    colors = [
        '#d53e4f', '#f46d43', '#fdae61', '#fee08b', '#e6f598', '#abdda4',
        '#66c2a5', '#3288bd', '#ffffbf'
    ]

    nodes = Node.query.all()
    edges = Edge.query.all()
    temp_imps = Temp_imp.query.all()
    temp_aspects = Temp_aspect.query.all()
    operators = Operator.query.all()
    experts = Expert.query.all()

    acceptedList = [
        expert.id for expert in experts if str(expert.accepted) == "Yes"
    ]
    dist_ops = Operator.query.distinct(Operator.name)
    op_dict = {str(x): shapes[i] for i, x in enumerate(dist_ops)}
    cl_dict = {str(x): colors[i] for i, x in enumerate(dist_ops)}

    data = {"nodes": [], "edges": []}
    data["nodes"] = [{
        "id": int(node.id),
        "sensitivity": int(node.sensitivity_id),
        "temp_aspect_id": str(node.temp_aspect_id),
        "temp_imp_id": str(node.temp_imp_id),
        "notes": str(node.notes),
        "notes_factor": str(node.notes_factor),
        "created_date": str(node.created_date),
        "font": {
            "multi": 'html',
            "size": 20,
            "color": 'white',
            "bold": True
        },
        "label": '<b>' + str(node.factor) + '</b>',
        "x": None,
        "y": None,
        "value": np.random.uniform(8, 20),
        "sup_lit": None
    } for node in nodes]
    data["edges"] = [{
        "arrows": "to",
        "from": str(edge.factor_A),
        "to": str(edge.factor_B),
        "id": int(edge.id),
        "created_date": str(edge.created_date),
        "value": np.random.uniform(0, 4),
        "temp_imp_id": str(edge.temp_imp_id),
        "temp_aspect_id": str(edge.temp_aspect_id),
        "operator_id": str(edge.operator_id),
        "notes_relation": str(edge.notes_relation),
        "sup_lit": str(edge.sup_lit)
    } for edge in edges]

    circdat = {
        "modules": [],
        "discipline": [],
        "subdivision": [],
        "publications": [],
        "People": []
    }
    for expert in experts:
        if not expert.is_admin and str(expert.accepted) == "Yes":
            circdat["modules"].append(str(expert.affiliation))
            circdat["discipline"].append(str(expert.discipline))
            circdat["subdivision"].append(str(expert.specialization))
            circdat["publications"].append(0)
            if expert.core_exp == "Yes":
                circdat["People"].append(
                    str(expert.title) + " " + str(expert.first_name) + " " +
                    str(expert.last_name) + "(T)")
            else:
                circdat["People"].append(
                    str(expert.title) + " " + str(expert.first_name) + " " +
                    str(expert.last_name) + "(N)")

    crdata = pd.DataFrame(circdat).groupby(
        ['modules', 'discipline', 'subdivision'], as_index=False).agg({
            'publications':
            'sum',
            'People':
            lambda x: ','.join(x)
        })
    circleData = createJSON(crdata)

    return render_template(
        'home/presentation.html',
        circleData=circleData,
        temp_imps1=enumerate(temp_imps),
        temp_aspects1=enumerate(temp_aspects),
        temp_imps=enumerate(temp_imps),
        temp_aspects=enumerate(temp_aspects),
        operators=enumerate(operators),
        causalData=data,
        op_dict=op_dict,
        cl_dict=cl_dict,
        title="Presentation")


@home.route('/submitcausalmap', methods=['GET', 'POST'])
def submitcausalmap():
    data = request.json
    errors = ""
    post = ""

    # print("******************* DB EXECUTE ***************")
    # result = db.engine.execute(text("SELECT * FROM nodes WHERE factor LIKE '%Ne%'"))
    # nodes = [factor for factor in result]
    # print(nodes)
    # print("---------------------------")

    for i, node in enumerate(data["nodes"]):
        try:
            nodePost = Node(
                factor=node["label"].replace("<b>", "").replace("</b>", ""),
                expert_id=current_user.get_id(),
                sensitivity_id=node["sensitivity_id"],
                spat_aspect_id=node["spat_aspect_id"],
                temp_aspect_id=node["temp_aspect_id"],
                temp_imp_id=node["temp_imp_id"],
                notes=node["notes"],
                notes_factor=node["notes_factor"])
            db.session.add(nodePost)
            db.session.commit()
            post = "It worked!"
        except Exception as e:
            errors += " (" + str(i) + " " + str(e) + ")"
            post = "Something went wrong with adding nodes: "
    for i, edge in enumerate(data["edges"]):
        try:
            edgePost = Edge(
                expert_id=current_user.get_id(),
                factor_A=edge["from"],
                factor_B=edge["to"],
                con_strength_id=edge["con_strength"],
                operator_id=edge["operator_id"],
                temp_aspect_id=edge["temp_aspect_id"],
                notes_relation=edge["notes_relation"],
                sup_lit=edge["sup_lit"])
            db.session.add(edgePost)
            db.session.commit()
            post = "It worked!"
        except Exception as e:
            errors += " (" + str(i) + " " + str(e) + ")"
            post = "Something went wrong with adding edges: "

    if errors == "":
        return jsonify(post)
    else:
        return jsonify(post + errors)


@home.route('/submitNewNodes', methods=['GET', 'POST'])
def submitNewNodes():
    data = request.json
    errors = ""
    post = ""
    for i, key in enumerate(data):
        try:
            nodePost = Node(
                factor=key,
                expert_id=current_user.get_id(),
                spat_aspect_id=data[key]["spat_aspect"],
                temp_aspect_id=data[key]["temp_aspect"])
            db.session.add(nodePost)
            db.session.commit()
            post = "It worked!"
        except Exception as e:
            errors += " (" + str(i) + " " + str(e) + ")"
            post = "Something went wrong with adding nodes: "

    if errors == "":
        return jsonify(post)
    else:
        return jsonify(post + errors)

@home.route('/submitNewEdges', methods=['GET', 'POST'])
def submitNewEdges():
    data = request.json
    errors = ""
    post = ""
    print("&&&&&&&&&&&&&&&&& DEBUGGING ^^^^^^^^^^^^^^^")
    print(data)
    for i, edge in enumerate(data):
        try:
            edgePost = Edge(
                factor_A=edge["source"],
                factor_B=edge["target"],
                con_strength_id=edge["value"],
                temp_aspect_id=edge["temp_aspect"],
                expert_id=current_user.get_id())
            db.session.add(edgePost)
            db.session.commit()
            post = "It worked!"
        except Exception as e:
            errors += " (" + str(i) + " " + str(e) + ")"
            post = "Something went wrong with adding nodes: "

    if errors == "":
        return jsonify(post)
    else:
        return jsonify(post + errors)



@home.route('/export_data', methods=['GET', 'POST'])
def export_data():
    filepath = os.path.dirname(os.path.realpath(__file__))[:-4] + "static/data/"
    print(filepath)
    data = request.json["data"]
    if not data:
        return "No file"
    data = convert(data)
    filename, contentType = export_network_data(data, filepath)
    if data["format"] == "csv":
        m = MultipartEncoder(
            fields={
                'field1': (filename[0], open(filename[0], 'rb'), 'text/csv'),
                'field2': (filename[1], open(filename[1], 'rb'), 'text/csv')
            })
        return Response(m.to_string(), mimetype=m.content_type)
    if data["format"] == "pkl":
        m = MultipartEncoder(
            fields={
                'field1': (filename[0], open(filename[0], 'rb'), 'text'),
                'field2': (filename[1], open(filename[1], 'rb'), 'text')
            })
        return Response(m.to_string(), mimetype=m.content_type)
    return send_file(
        filepath + filename,
        mimetype=contentType,
        attachment_filename=filename,
        as_attachment=True)
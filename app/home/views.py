# app/home/views.py

from flask import abort, render_template, request, jsonify, send_from_directory, make_response, send_file, Response
from ..models import Expert, Factor, Operator, Node, Edge, Temp_imp, Temp_aspect
from flask_login import current_user, login_required
from helpers import createJSON, export_network_data, convert, simulation_1, simulation_2, sim_div, give_arrows, give_dashes
from requests_toolbelt import MultipartEncoder
from forms import NodeForm
from . import home

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

    shapes = ["triangle", "square", "diamond","triangle", "square", "diamond", "triangle", "square", "diamond"]
    colors = ['#d53e4f','#f46d43','#fdae61','#fee08b','#e6f598','#abdda4','#66c2a5','#3288bd','#ffffbf']
    string = "digraph {&#13;&#10;&Tab; node [width=.25,height=.375,fontsize=15]&#13;&#10;&Tab; node [shape=filled color=steelblue]&#13;&#10;&Tab; edge [length=100, fontcolor=black]&#13;&#10;&NewLine;"

    nodes = Node.query.all()
    edges = Edge.query.all()
    temp_imps = Temp_imp.query.all()
    temp_aspects = Temp_aspect.query.all()
    operators = Operator.query.all()
    experts = Expert.query.all()

    acceptedList = [expert.id for expert in experts if str(expert.accepted) == "Yes"]
    dist_ops = Operator.query.distinct(Operator.name)
    op_dict = {str(x) : shapes[i] for i, x in enumerate(dist_ops)}
    cl_dict = {str(x) : colors[i] for i, x in enumerate(dist_ops)}

    randicon = ["onset", "maintenance", "relapse"]
    # randicon = ["stock", "cloud", "unknown", "onset", "maintenance", "relapse"]
    randicon = ["variable", "stock", "cloud", "unknown"]

    data = { "nodes":[], "edges":[]}
    data["nodes"] = [{
        "id": int(node.id),
        "threshold": int(node.threshold),
        "temp_aspect_id": str(node.temp_aspect_id),
        "temp_imp_id": str(node.temp_imp_id),
        "notes": str(node.notes),
        "notes_factor": str(node.notes_factor),
        "created_date": str(node.created_date),
        "font": { "multi": 'html', "size": 20, "color":'black', "bold":True}, 
        "label": '<b>'+str(node.factor)+'</b>',
        "group": choice(randicon),
        "x": None,
        "y": None,
        "value": np.random.uniform(8,20),
        "sup_lit": None
    } for node in nodes]
    data["edges"] = [{
        "label":
        int(edge.value),
        "arrows":
        give_arrows(edge.value),
        "dashes":
        bool(1),
        "from":
        str(edge.factor_A),
        "to":
        str(edge.factor_B),
        "id":
        int(edge.id),
        "created_date":
        str(edge.created_date),
        "value": int(edge.value),
        "temp_imp_id":
        str(edge.temp_imp_id),
        "temp_aspect_id":
        str(edge.temp_aspect_id),
        "operator_id":
        str(edge.operator_id),
        "notes_relation":
        str(edge.notes_relation),
        "sup_lit":
        str(edge.sup_lit)
    } for edge in edges]

    return render_template('home/index.html', bannertitle="Depression Research", subtitle="Interactive Causal Mapping", temp_imps1=enumerate(temp_imps), temp_aspects1=enumerate(temp_aspects), temp_imps=enumerate(temp_imps), temp_aspects=enumerate(temp_aspects), operators=enumerate(operators), causalData=data, op_dict=op_dict, cl_dict=cl_dict, title="Testing")


@home.route('/testing')
def testing():
    """
    Render the testing template on the / route
    """

    shapes = ["triangle", "square", "diamond","triangle", "square", "diamond", "triangle", "square", "diamond"]
    colors = ['#d53e4f','#f46d43','#fdae61','#fee08b','#e6f598','#abdda4','#66c2a5','#3288bd','#ffffbf']
    string = "digraph {&#13;&#10;&Tab; node [width=.25,height=.375,fontsize=15]&#13;&#10;&Tab; node [shape=filled color=steelblue]&#13;&#10;&Tab; edge [length=100, fontcolor=black]&#13;&#10;&NewLine;"
    
    nodes = Node.query.all()
    edges = Edge.query.all()
    temp_imps = Temp_imp.query.all()
    temp_aspects = Temp_aspect.query.all()
    operators = Operator.query.all()
    experts = Expert.query.all()

    acceptedList = [expert.id for expert in experts if str(expert.accepted) == "Yes"]
    dist_ops = Operator.query.distinct(Operator.name)
    op_dict = {str(x) : shapes[i] for i, x in enumerate(dist_ops)}
    cl_dict = {str(x) : colors[i] for i, x in enumerate(dist_ops)}
    
    randicon = ["onset", "maintenance", "relapse"]
    # randicon = ["stock", "cloud", "unknown", "onset", "maintenance", "relapse"]
    # randicon = ["variable", "stock", "cloud", "unknown"]

    data = { "nodes":[], "edges":[]}
    data["nodes"] = [{
        "id": int(node.id),
        "threshold": int(node.threshold),
        "temp_aspect_id": str(node.temp_aspect_id),
        "temp_imp_id": str(node.temp_imp_id),
        "notes": str(node.notes),
        "notes_factor": str(node.notes_factor),
        "created_date": str(node.created_date),
        "font": { "multi": 'html', "size": 20, "color":'black', "bold":True}, 
        "label": '<b>'+str(node.factor)+'</b>',
        "group": choice(randicon),
        "x": None,
        "y": None,
        "value": np.random.uniform(8,20),
        "sup_lit": None
    } for node in nodes]
    data["edges"] = [{
        "label":
        int(edge.value),
        "arrows":
        give_arrows(edge.value),
        "dashes":
        bool(1),
        "from":
        str(edge.factor_A),
        "to":
        str(edge.factor_B),
        "id":
        int(edge.id),
        "created_date":
        str(edge.created_date),
        "value": int(edge.value),
        "temp_imp_id":
        str(edge.temp_imp_id),
        "temp_aspect_id":
        str(edge.temp_aspect_id),
        "operator_id":
        str(edge.operator_id),
        "notes_relation":
        str(edge.notes_relation),
        "sup_lit":
        str(edge.sup_lit)
    } for edge in edges]
    # form = NodeForm()
    # if form.validate_on_submit():
    #     factor = Factor(expert_id=current_user.get_id(),
    #                     factor=form.factor.data,
    #                     temp_imp_id=form.temp_imp_id.data.id,
    #                     temp_aspect_id=form.temp_aspect_id.data.id,
    #                     notes_factor=form.notes_factor.data,
    #                     notes=form.notes.data.id,
    #                     sup_lit=form.sup_lit.data
    #                     )
    #     print(factor)

    return render_template('home/testing.html', bannertitle="Depression Research", subtitle="Interactive Causal Mapping", temp_imps1=enumerate(temp_imps), temp_aspects1=enumerate(temp_aspects), temp_imps=enumerate(temp_imps), temp_aspects=enumerate(temp_aspects), operators=enumerate(operators), causalData=data, op_dict=op_dict, cl_dict=cl_dict, title="Testing")


@home.route('/_add_numbers')
def add_numbers():
    a = request.args.get('a', "", type=str)
    data = sim_div(a)
    return jsonify(data)


@home.route('/dashboard')
@login_required
def dashboard():
    """
    Render the dashboard template on the /dashboard route
    """

    experts = Expert.query.all()
    data = {"modules":[], "discipline":[], "subdivision":[], "publications":[], "People":[]}
    for expert in experts:
        if not expert.is_admin and str(expert.accepted) == "Yes":
            data["modules"].append(str(expert.affiliation))
            data["discipline"].append(str(expert.discipline))
            data["subdivision"].append(str(expert.specialization))
            data["publications"].append(0)
            if str(expert.core_exp) == "Yes":
                data["People"].append(str(expert.title) + " " + str(expert.first_name) + " " + str(expert.last_name) + "(T)")
            else:
                data["People"].append(str(expert.title) + " " + str(expert.first_name) + " " + str(expert.last_name) + "(N)")

    crdata = pd.DataFrame(data).groupby(['modules', 'discipline', 'subdivision'], as_index=False).agg({'publications':'sum', 'People':lambda x: ','.join(x)})
    circleData = createJSON(crdata)

    return render_template('home/dashboard.html', bannertitle="Stock- and- Flow Diagram", subtitle="Where automized system dynamics models will run", circleData=circleData, title="Dashboard")


@home.route('/admin/dashboard')
@login_required
def admin_dashboard():
    # prevent non-admins from accessing the page
    if not current_user.is_admin:
        abort(403)

    return render_template('home/admin_dashboard.html', bannertitle="Welcome Admin", subtitle="A place to display your admin powers", title="AdminDashboard")


@home.route('/admin/presentation')
@login_required
def admin_presentation():
    # prevent non-admins from accessing the page
    if not current_user.is_admin:
        abort(403)

    shapes = ["triangle", "square", "diamond","triangle", "square", "diamond", "triangle", "square", "diamond"]
    colors = ['#d53e4f','#f46d43','#fdae61','#fee08b','#e6f598','#abdda4','#66c2a5','#3288bd','#ffffbf']
    string = "digraph {&#13;&#10;&Tab; node [width=.25,height=.375,fontsize=15]&#13;&#10;&Tab; node [shape=filled color=steelblue]&#13;&#10;&Tab; edge [length=100, fontcolor=black]&#13;&#10;&NewLine;"
    
    nodes = Node.query.all()
    edges = Edge.query.all()
    temp_imps = Temp_imp.query.all()
    temp_aspects = Temp_aspect.query.all()
    operators = Operator.query.all()
    experts = Expert.query.all()

    acceptedList = [expert.id for expert in experts if str(expert.accepted) == "Yes"]
    dist_ops = Operator.query.distinct(Operator.name)
    op_dict = {str(x) : shapes[i] for i, x in enumerate(dist_ops)}
    cl_dict = {str(x) : colors[i] for i, x in enumerate(dist_ops)}
    
    data = { "nodes":[], "edges":[]}
    data["nodes"] = [{
        "id": int(node.id),
        "threshold": int(node.threshold),
        "temp_aspect_id": str(node.temp_aspect_id),
        "temp_imp_id": str(node.temp_imp_id),
        "notes": str(node.notes),
        "notes_factor": str(node.notes_factor),
        "created_date": str(node.created_date),
        "font": { "multi": 'html', "size": 20, "color":'white', "bold":True}, 
        "label": '<b>'+str(node.factor)+'</b>',
        "x": None,
        "y": None,
        "value": np.random.uniform(8,20),
        "sup_lit": None
    } for node in nodes]
    data["edges"] = [{
        "arrows":
        "to",
        "from":
        str(edge.factor_A),
        "to":
        str(edge.factor_B),
        "id":
        int(edge.id),
        "created_date":
        str(edge.created_date),
        "value": np.random.uniform(0,4),
        "temp_imp_id":
        str(edge.temp_imp_id),
        "temp_aspect_id":
        str(edge.temp_aspect_id),
        "operator_id":
        str(edge.operator_id),
        "notes_relation":
        str(edge.notes_relation),
        "sup_lit":
        str(edge.sup_lit)
    } for edge in edges]

    circdat = {"modules":[], "discipline":[], "subdivision":[], "publications":[], "People":[]}
    for expert in experts:
        if not expert.is_admin and str(expert.accepted) == "Yes":
            circdat["modules"].append(str(expert.affiliation))
            circdat["discipline"].append(str(expert.discipline))
            circdat["subdivision"].append(str(expert.specialization))
            circdat["publications"].append(0)
            if expert.core_exp == "Yes":
                circdat["People"].append(str(expert.title) + " " + str(expert.first_name) + " " + str(expert.last_name) + "(T)")
            else:
                circdat["People"].append(str(expert.title) + " " + str(expert.first_name) + " " + str(expert.last_name) + "(N)")

    crdata = pd.DataFrame(circdat).groupby(['modules', 'discipline', 'subdivision'], as_index=False).agg({'publications':'sum', 'People':lambda x: ','.join(x)})
    circleData = createJSON(crdata)

    return render_template('home/presentation.html', circleData=circleData, temp_imps1=enumerate(temp_imps), temp_aspects1=enumerate(temp_aspects), temp_imps=enumerate(temp_imps), temp_aspects=enumerate(temp_aspects), operators=enumerate(operators), causalData=data, op_dict=op_dict, cl_dict=cl_dict, title="Presentation")


@home.route('/submitcausalmap', methods=['GET','POST'])
def submitcausalmap():
    post = request.args.get('post', 0)
    print("****************************** DEBUGGING *************************")
    print(type(post))
    data = json_loads_byteified(post)
    print(data.keys())
    print("****************************** DEBUGGING *************************")
    # print(data["nodes"]["_data"])
    # print("****************************** DEBUGGING *************************")
    # print(data["edges"]["_data"])
    print("HIYAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    return jsonify(post)


@home.route('/export_data', methods = ['GET', 'POST'])
def export_data():
    data = request.json["data"]
    if not data:
        return "No file"
    data = convert(data)
    filename, contentType = export_network_data(data)
    if data["format"] == "csv":
        m = MultipartEncoder(fields={
           'field1': (filename[0], open(filename[0], 'rb'), 'text/csv'),
           'field2': (filename[1], open(filename[1], 'rb'), 'text/csv')}
        )
        return Response(m.to_string(), mimetype=m.content_type)
    if data["format"] == "pkl":
        m = MultipartEncoder(fields={
           'field1': (filename[0], open(filename[0], 'rb'), 'text'),
           'field2': (filename[1], open(filename[1], 'rb'), 'text')}
        )
        return Response(m.to_string(), mimetype=m.content_type)
    return send_file("static/data/" + filename, mimetype=contentType, attachment_filename=filename, as_attachment=True)

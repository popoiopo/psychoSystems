var nodes = null;
var edges = null;
var network = null;
var seed = 2;

// create an array with nodes
nodes = new vis.DataSet();
nodes.add(data["nodes"])

// create an array with edges
edges = new vis.DataSet();
edges.add(data["edges"]);

// create a network
var data = {
    nodes: nodes,
    edges: edges
};

function setDefaultLocale() {
  var defaultLocal = navigator.language;
  var select = document.getElementById('locale');
  select.selectedIndex = 0; // set fallback value
  for (var i = 0, j = select.options.length; i < j; ++i) {
    if (select.options[i].getAttribute('value') === defaultLocal) {
      select.selectedIndex = i;
      break;
    }
  }
}

function destroy() {
  if (network !== null) {
    network.destroy();
    network = null;
  }
}

function draw() {
  destroy();

  // create a network
  var container = document.getElementById('mynetwork');
  var options = {
    nodes: {
      shape: 'dot',
      scaling: {
        min: 10,
        max: 30
      },
      font: {
        size: 12,
        face: 'Tahoma'
      }
    },
    edges: {
      color:{inherit:true},
      width: 0.15,
<<<<<<< HEAD
      // smooth: {
      //   // type: 'continuous'
      //   type: 'curvedCW',
      //   forceDirection: 'vertical',
      //   roundness: 0.4
      // }
=======
      smooth: {
        type: 'continuous'
      }
>>>>>>> fd305919d27b64cdef0b41cb2aac0075e2ff6b3f
    },
    interaction: {
      hideEdgesOnDrag: true,
      tooltipDelay: 200
    },
<<<<<<< HEAD
    physics:false,
    // {
    //   barnesHut:{gravitationalConstant:-10000},
    //   stabilization: {iterations:2500}
    // },
    layout: {
      hierarchical: {
      direction: "UD"
    }}, // just to make sure the layout is the same when the locale is changed
=======
    physics:{
      barnesHut:{gravitationalConstant:-10000},
      stabilization: {iterations:2500}
    },
    layout: {randomSeed:seed}, // just to make sure the layout is the same when the locale is changed
>>>>>>> fd305919d27b64cdef0b41cb2aac0075e2ff6b3f
    locale: document.getElementById('locale').value,
    manipulation: {
      addNode: function (data, callback) {
        // filling in the popup DOM elements
        document.getElementById('node-operation').innerHTML = "Add Node";
        editNode(data, clearNodePopUp, callback);
      },
      editNode: function (data, callback) {
        // filling in the popup DOM elements
        document.getElementById('node-operation').innerHTML = "Edit Node";
        editNode(data, cancelNodeEdit, callback);
      },
      deleteNode: function(data, callback) {
        for (var i = data.nodes.length - 1; i >= 0; i--) {
            for (var i = newData.nodes.length - 1; i >= 0; i--) {
                if (newData.nodes[i].id == data.nodes[i]) {
                    newData.nodes.splice(i, 1);
                }
            }
        }
        callback(data);
        return true
      },
      addEdge: function (addData, callback) {
        if (addData.from == addData.to) {
          var r = confirm("Do you want to connect the node to itself?");
          if (r != true) {
            callback(null);
            return;
          }
        }
        
        document.getElementById('edge-operation').innerHTML = "Add Edge: " + data["nodes"]["_data"][addData.from]["label"] + " &rarr; " + data["nodes"]["_data"][addData.to]["label"];
        editEdgeWithoutDrag(addData, callback);
      },
      editEdge: {
        editWithoutDrag: function(editData, callback) {
          document.getElementById('edge-operation').innerHTML = "Edit Edge: " + data["nodes"]["_data"][editData.from]["label"] + " &rarr; " + data["nodes"]["_data"][editData.to]["label"];
          editEdgeWithoutDrag(editData,callback);
        }
      },
      deleteEdge: function(data, callback) {
        for (var i = data.edges.length - 1; i >= 0; i--) {
            for (var i = newData.edges.length - 1; i >= 0; i--) {
                if (newData.edges[i].id == data.edges[i]) {
                    newData.edges.splice(i, 1);
                }
            }
        }
        callback(data);
        return true
      }
    }
  };
  network = new vis.Network(container, data, options);
}

function checkForm(temp, infType) {
    keys = Object.keys(temp);
    console.log(temp);
    check = dropDowns
<<<<<<< HEAD
    noCheck = ["id", "to", "from", "created_date", "level", "arrows", "x", "y", "notes_factor", "sup_lit", "notes", "group"]
=======
    noCheck = ["id", "to", "from", "created_date", "arrows", "x", "y", "notes_factor", "sup_lit", "notes", "group"]
>>>>>>> fd305919d27b64cdef0b41cb2aac0075e2ff6b3f
    pass = true
    for (var i = keys.length - 1; i >= 0; i--) {
        if (!noCheck.includes(keys[i])) {
            if (temp[keys[i]] == "undefined" || temp[keys[i]] =="") {
                document.getElementById(infType + "-" + keys[i]).style.backgroundColor = "#FF0000"
                pass = false;
            }
            else { document.getElementById(infType + '-' + keys[i]).style.backgroundColor = "#f9f9f9" }
            if (Object.keys(check).includes(keys[i])){
                if (temp[keys[i]] == "") {
                    document.getElementById(infType + "-" + keys[i]).style.backgroundColor = "#FF0000"
                    pass = false;
                }
            }
        }
    }
    return pass
}

function editNode(data, cancelAction, callback) {
  document.getElementById('node-label').value = data.label;
  document.getElementById('node-notes').value = data.notes;
  document.getElementById('node-sensitivity_id').value = data.sensitivity_id;
  document.getElementById('node-sup_lit').value = data.sup_lit;
  document.getElementById('node-temp_imp_id').value = data.temp_imp_id;
  document.getElementById('node-notes_factor').value = data.notes_factor;
  document.getElementById('node-temp_aspect_id').value = data.temp_aspect_id;
  document.getElementById('node-spat_aspect_id').value = data.spat_aspect_id;

  document.getElementById('node-saveButton').onclick = saveNodeData.bind(this, data, callback);
  document.getElementById('node-cancelButton').onclick = cancelAction.bind(this, callback);
  document.getElementById('node-popUp').style.display = 'block';
}

// Callback passed as parameter is ignored
function clearNodePopUp() {
  document.getElementById('node-saveButton').onclick = null;
  document.getElementById('node-cancelButton').onclick = null;
  document.getElementById('node-popUp').style.display = 'none';
}

function cancelNodeEdit(callback) {
  clearNodePopUp();
  callback(null);
}

function saveNodeData(data, callback) {
  data.label = document.getElementById('node-label').value;

  var nodeID = data.label + String(Math.random());

  data.label = document.getElementById('node-label').value;
  data.id = nodeID
  data.group = parseInt(document.getElementById('node-temp_imp_id').value)-1;
  data.notes = document.getElementById('node-notes').value;
  data.sensitivity_id = document.getElementById('node-sensitivity_id').value;
  data.sup_lit = document.getElementById('node-sup_lit').value;
  data.temp_imp_id = document.getElementById('node-temp_imp_id').value;
  data.notes_factor = document.getElementById('node-notes_factor').value;
  data.temp_aspect_id = document.getElementById('node-temp_aspect_id').value;
<<<<<<< HEAD
  data.level = document.getElementById('node-temp_aspect_id').value;
=======
>>>>>>> fd305919d27b64cdef0b41cb2aac0075e2ff6b3f
  data.spat_aspect_id = document.getElementById('node-spat_aspect_id').value;
  data.created_date = new Date().toLocaleString("en-GB", {timeZone: "Europe/Amsterdam",
                                    timeZoneName: "short"})

  if (!checkForm(data, "node")) { return }

  newData.nodes.push(data);

  clearNodePopUp();
  callback(data);
}

function editEdgeWithoutDrag(data, callback) {
  // filling in the popup DOM elements
  for (var i = 0; i < newData.edges.length; i++) {
      if (newData.edges[i].id == data.id) {
          document.getElementById('edge-label').value = newData.edges[i].label;
          document.getElementById('edge-operator_id').value = newData.edges[i].type;
          document.getElementById('edge-con_strength').value = newData.edges[i].con_strength;
          document.getElementById('edge-temp_imp_id').value = newData.edges[i].temp_imp;
          document.getElementById('edge-temp_aspect_id').value = newData.edges[i].temp_aspect;
          document.getElementById('edge-notes_relation').value = newData.edges[i].notes;
          document.getElementById('edge-sup_lit').value = newData.edges[i].sup_lit;
      }
  }  

  document.getElementById('edge-saveButton').onclick = saveEdgeData.bind(this, data, callback, data.id);
  document.getElementById('edge-cancelButton').onclick = cancelEdgeEdit.bind(this,callback);
  document.getElementById('edge-popUp').style.display = 'block';
}

function clearEdgePopUp() {
  document.getElementById('edge-saveButton').onclick = null;
  document.getElementById('edge-cancelButton').onclick = null;
  document.getElementById('edge-popUp').style.display = 'none';
}

function cancelEdgeEdit(callback) {
  clearEdgePopUp();
  callback(null);
}

function saveEdgeData(data, callback, edit, type) {
  
  if (type != "opNode") {
    if (typeof data.to === 'object')
      data.to = data.to.id
    if (typeof data.from === 'object')
      data.from = data.from.id

    // data.label = document.getElementById('edge-label').value;
    // if (edit) { data.id = edit }
    // else {
    //   var edgeID = data.label + String(Math.random());
    //   data.id = edgeID
    // }
    data.created_date = new Date().toLocaleString("en-GB", {timeZone: "Europe/Amsterdam",
                                    timeZoneName: "short"})
    data.operator_id = document.getElementById('edge-operator_id').value;
    data.con_strength = document.getElementById('edge-con_strength').value;
    data.temp_imp_id = document.getElementById('edge-temp_imp_id').value;
    data.temp_aspect_id = document.getElementById('edge-temp_aspect_id').value;
    data.notes_relation = document.getElementById('edge-notes_relation').value;
    data.sup_lit = document.getElementById('edge-sup_lit').value;
    data.arrows = "to"

    if (!checkForm(data, "edge")) { return };

    if (Object.keys(op_dict).includes(data.type) && data.type != "No operator needed") {
      newNode = data.to;
      nodeID = data.from.slice(0,3) + "_" + data.to.slice(0, 3) + "_" + String(Math.random());
      nodeData = {
        "id": nodeID, 
        "label":data.from.slice(0,3) + "_" + data.to.slice(0, 3) + "_" + data.type.toUpperCase(), 
        "shape":op_dict[data.type], 
        "color":cl_dict[data.type]}
      network.body.data.nodes.update(nodeData)
      newData.nodes.push(nodeData);

      data.to = nodeID
      data.id = data.label + String(Math.random());
      data.arrows = "to"
      network.body.data.edges.add(data);
      newData.edges.push(data);

      data.from = nodeID;
      data.to = newNode;
      data.label = undefined;
      data.id = data.label + String(Math.random());
      network.body.data.edges.add(data);
      newData.edges.push(data);

      clearEdgePopUp();
      callback(data);
    }
    else {
      newData.edges.push(data);
      clearEdgePopUp();
      callback(data);
    }
  }
  else {
    newData.edges.push(data);
    clearEdgePopUp();
    callback(data);
  }
}

function init() {
  setDefaultLocale();
  draw();
}

function saveData() {
  console.log(newData);
  var posting = JSON.stringify(newData);
  $.ajax({
    url: '/submitcausalmap',
    contentType: "application/json; charset=utf-8",
    data: posting,
    type: 'POST',
    success: function(response ,jqxhr, settings) {
      console.log(response, jqxhr, settings);
    },
    error: function(error, jqxhr, settings) {
      console.log(error);
      console.log(jqxhr);
      console.log(settings);
      alert("Something has gone wrong with submitting your data to the database. Please contact the server administrator.")
    }
  });
}

function downloadFile(filename, text) {
  var element = document.createElement('a');
  element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
  element.setAttribute('download', filename);
  element.style.display = 'none';

  document.body.appendChild(element);
  element.click();
  document.body.removeChild(element);
}

function parseFiles(response) {
  var lines = response.split('\n');
  header = lines[0];
  a = lines.slice(1);
  index = a.findIndex(x => x == header);
  b = lines.splice(0,4);
  c = lines.splice(index-4);
  var newtext_A = lines.join('\n');

  d = c.splice(5);
  d.splice(-3);
  var newtext_B = d.join('\n');

  return [newtext_A, newtext_B]
}

function export_data() {
  format = document.getElementById('export').value;
  exp_data = { "data": {"format" : format, "nodes" : data.nodes._data, "edges" : data.edges._data} };
  posting = JSON.stringify(exp_data);
  $.ajax({
    url: '/export_data',
    contentType: "application/json; charset=utf-8",
    data: posting,
    type: 'POST',
    success: function(response ,jqxhr, settings) {
      if (format == "csv") { 
        var newtext = parseFiles(response);

        var promise1 = new Promise(function(resolve, reject) {
            resolve( downloadFile("depression_network_nodes."+format, newtext[0]) );
        });

        promise1.then(function(value) {
          setTimeout(function() {
            downloadFile("depression_network_edges."+format, newtext[1])
          }, 1000);
        });
      }
      if (format == "pkl") { 
        var newtext = parseFiles(response);

                var promise1 = new Promise(function(resolve, reject) {
            resolve( downloadFile("depression_network_weights.txt", newtext[1]) );
        });

        promise1.then(function(value) {
          setTimeout(function() {
            downloadFile("depression_network_thresholds.txt", newtext[0]); 
          }, 1000);
        });
      }
      else if (format == "json") { downloadFile("depression_network_data."+format, JSON.stringify(response)); }
    },
    error: function(error, jqxhr, settings) {
      alert("Something has gone wrong with the export. Please contact the server administrator.")
    }
  });
}

document.getElementById('import').onclick = function() {
  var nodesFileData = document.getElementById('selectFiles1').files;
  var edgesFileData = document.getElementById('selectFiles2').files;

  if (nodesFileData.length <= 0 || edgesFileData.length <= 0) {
    alert("Files cannot be read properly.")
    return false;
  }

  const readNodeData = (inputFile) => {
    const NodeReader = new FileReader();

    return new Promise((resolve, reject) => {
      NodeReader.onerror = () => {
        NodeReader.abort();
        reject(new DOMException("Problem parsing input file."));
      };

      NodeReader.onload = () => {

        const readEdgeData = (inputFile) => {
          const EdgeReader = new FileReader();

          return new Promise((resolve, reject) => {
            EdgeReader.onerror = () => {
              EdgeReader.abort();
              reject(new DOMException("Problem parsing input file."));
            };

            EdgeReader.onload = () => {
              nodeData = [];
              edgeData = [];
              dataNodes = $.csv.toArrays(NodeReader.result);
              for (var i = 1; i < dataNodes.length-1; i++) {
                nodeTemp = {}
                for (var j = 1; j < dataNodes[i].length; j++) {
                  if (dataNodes[0][j] == "id") {
                    nodeTemp[dataNodes[0][j]] = dataNodes[i][j]
                  }
                  else {
                    if (dataNodes[i][j] == "") {
                      nodeTemp[dataNodes[0][j]] = null;
                    }
                    else {
                      nodeTemp[dataNodes[0][j]] = dataNodes[i][j]
                    }
                  }
                }
                nodeData.push(nodeTemp)
              }

              dataEdges = $.csv.toArrays(EdgeReader.result);
              for (var i = 1; i < dataEdges.length-1; i++) {
                edgeTemp = {}
                for (var j = 1; j < dataEdges[i].length; j++) {
                  if (dataEdges[0][j] == "id") {
                    edgeTemp[dataEdges[0][j]] = dataEdges[i][j]
                  }
                  else {
                    if (dataEdges[i][j] == "") {
                      edgeTemp[dataEdges[0][j]] = null;
                    }
                    else {
                      edgeTemp[dataEdges[0][j]] = dataEdges[i][j]
                    }
                  }
                }
                edgeData.push(edgeTemp)
              }

              nodes.clear();
              edges.clear();
              nodes.add(nodeData);
              edges.add(edgeData);

              resolve(draw());
            };
            EdgeReader.readAsText(inputFile);
          });
        };
        resolve(readEdgeData(edgesFileData.item(0)));
      };
      NodeReader.readAsText(inputFile);
    });
  };
  readNodeData(nodesFileData.item(0));
};


document.getElementById('importJSON').onclick = function() {
  var jsonFileData = document.getElementById('selectFilesJSON').files;

  if (jsonFileData.length <= 0) {
    alert("Files cannot be read properly.")
    return false;
  }

  const readjsonData = (inputFile) => {
    const jsonReader = new FileReader();

    return new Promise((resolve, reject) => {
      jsonReader.onerror = () => {
        jsonReader.abort();
        reject(new DOMException("Problem parsing input file."));
      };

      jsonReader.onload = () => {
          jsonData = JSON.parse(jsonReader.result)
          nodeData = []
          edgeData = []

          Object.keys(jsonData["edges"]).forEach(function(key) {
              edgeData.push(jsonData["edges"][key]);
          });

          Object.keys(jsonData["nodes"]).forEach(function(key) {
              nodeData.push(jsonData["nodes"][key]);
          });

          nodes.clear();
          edges.clear();
          nodes.add(nodeData);
          edges.add(edgeData);

          resolve(draw());
      };
      jsonReader.readAsText(inputFile);
    });
  }
  readjsonData(jsonFileData.item(0));
};

function openNav() {
  document.getElementById("mySidebar").style.width = "450px";
  document.getElementById("main").style.marginLeft = "450px";
}

function closeNav() {
  document.getElementById("mySidebar").style.width = "0";
  document.getElementById("main").style.marginLeft= "0";
}

init();
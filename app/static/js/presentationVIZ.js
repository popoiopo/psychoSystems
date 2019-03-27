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

var options = {
  nodes: {
    shape:"box",
    color:'#7d0499',
    scaling:{
      label: {
        min:8,
        max:20
      }
    }
  }
};

var container = document.getElementById('mynetwork');

network = new vis.Network(container, data, options);

var link, node, circle_mask, circle, label;
var selected = new Array(Object.values(data["nodes"]["_data"]).length)
selected.fill(1);
var width = 720;
var height = 400;
var global_nodeList = [];
var global_1or2 = 1;
var start = 0;
var dataSimAll;

drawSlider("div#slider1_HN", "div#slider2_HN", "_HN", 2);
drawSlider("div#slider1_sim3", "div#slider2_sim3", "_sim3", 2);

function request(sim){
    if (sim) { global_1or2 = sim }
    json = '{"simulation": ' + global_1or2 + ', "I":' + d3.select("p#value2_sim3").text() + ', "c": ' + d3.select("p#value1_sim3").text() + ', "select": ' + "[" + selected.toString() + "]" + ', "data":' + JSON.stringify(data) + '}';
    if (start == 0) { json = '{"simulation": 1, "I":1500, "c": 2, "select": ' + "[" + selected.toString() + "]" + ', "data":' + JSON.stringify(data) + '}' }
    $.getJSON($SCRIPT_ROOT + '/_add_numbers', {
        a: json
      }, function(dataSim) {
        dataSim = JSON.parse(dataSim);
        dataSimAll = dataSim;
        if (start == 0) { drawLineGraph(dataSim["D"], "#heavy_networkSVG", "#heavy_network"); start = 1;}
        if (circle !== null) { dataSimPoint = Math.floor(slider.value * d3.select("p#value2_sim3").text());
                           update(dataSimPoint, dataSim); }
        sim1_2(dataSim);
      });
}

function update(i, dataSim) {
    if (dataSim.simulation == 1){
        X = dataSim.X[i];
        P = dataSim.P[i];
    }
    else {
        X = dataSim.UP.X[Math.floor(i/2)];
        P = dataSim.UP.P[Math.floor(i/2)];
    }

    circle
        .attr("fill-opacity", function(d) { return P[d.index]; })
        .attr("stroke-opacity", function(d) { return X[d.index] ? 1 : 0; });

    label.attr("opacity", function(d) { return X[d.index] ? 1 : 0.7; } );
}

function select(index) {
    selected[index] = selected[index] ? 0 : 1;
    circle_mask.style("stroke", function(d) { return (selected[d.index]) ? 'grey' : 'red'; });
    circle.style("stroke", function(d) { return (selected[d.index]) ? 'black' : 'red'; });
    request();
}

var slider = document.getElementById("myRange");
slider.oninput = function() {
    if (circle !== null && dataSimAll !== null) {
        update(Math.floor(this.value * d3.select("p#value2_sim3").text()), dataSimAll);
        updateLine(this.value, dataSimAll);
    }
};

request();

var svg = d3.select("#graph_network")
    .append("svg")
      .attr("id", "#graph_networkSVG")
      .attr("preserveAspectRatio", "xMinYMin meet")
      .attr("viewBox", "0 0 " + width + " " + height)
      .classed("svg-content", true);

var color = d3.scaleOrdinal(d3.schemeCategory20);

var simulation = d3.forceSimulation()
    .force("link", d3.forceLink().id(function(d) { return d.id; }).distance(function(d) {
        return Math.max(10, 50 / (d.weight));
    }))
    .force('collision', d3.forceCollide().radius(function(d) { return 25;}))
    .force("center", d3.forceCenter(width / 2, height / 2));


function graphData(allData) {
    nodeData = []
    console.log(allData);
    for (var key in data["nodes"]["_data"]) {
        // skip loop if the property is from prototype
        if (!data["nodes"]["_data"].hasOwnProperty(key)) continue;

        var obj = data["nodes"]["_data"];

        temp = {"threshold" : 1,
            "activationValues" : 0, 
            "stateValues": 0,
            "id" : key,
            "index" : parseInt(key), 
            "name" : obj[key].label}
        nodeData.push(temp)
    }

    edgeData = []
    for (var key in data["edges"]["_data"]) {
        // skip loop if the property is from prototype
        if (!data["edges"]["_data"].hasOwnProperty(key)) continue;

        var obj = data["edges"]["_data"];

        if (obj[key].value == "None") { var weightValue = 1; }
        else { var weightValue = obj[key].value; }

        temp = {
            "weight" : weightValue,
            "source" : obj[key].from, 
            "target": obj[key].to}
        edgeData.push(temp)
    }
    
    return {"directed": false,
            "multigraph": false,
            "graph": {},
            "nodes": nodeData,
            "links": edgeData}
}

graph = graphData(data);

link = svg.append("g")
    .attr("class", "links")
    .selectAll("line")
    .data(graph.links)
    .enter().append("line")
    .attr("stroke-width", function(d) {
        if (d.weight > 0) { return d.weight * d.weight; }
        else { return 0; }
     });

node = svg.append("g")
    .attr("class", "nodes")
    .selectAll("g")
    .data(graph.nodes)
    .enter().append("g");

circle_mask = node.append("circle")
    .attr("r", 10)
    .style("fill", 'white');

circle = node.append("circle")
    .attr("r", 10)
    .style("fill", function(d) { return color(d.id); })
    .style("stroke", "black")
    .on("click", function(d) { return select(d.index); })
    .call(d3.drag()
        .on("start", dragstarted)
        .on("drag", dragged)
        .on("end", dragended));

circle.append("title").text(function(d) { return d.name; });

label = node.append("text")
    .attr("font-size", '20px')
    .text(function(d) { return d.id; });

simulation
    .nodes(graph.nodes)
    .on("tick", ticked);

simulation.force("link")
    .links(graph.links);

function ticked() {
    link
        .attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });
    node
        .attr("cx", function(d) { return d.x; })
        .attr("cy", function(d) { return d.y; });
    circle_mask
        .attr("cx", function(d) { return d.x; })
        .attr("cy", function(d) { return d.y; });
    circle
        .attr("cx", function(d) { return d.x; })
        .attr("cy", function(d) { return d.y; });
    label
        .attr("x", function(d) { return d.x + 15; })
        .attr("y", function(d) { return d.y + 5; });
}

function dragstarted(d) {
    if (!d3.event.active) simulation.alphaTarget(0.3).restart();
    d.fx = d.x;
    d.fy = d.y;
}

function dragged(d) {
    d.fx = d3.event.x;
    d.fy = d3.event.y;
}

function dragended(d) {
    if (!d3.event.active) simulation.alphaTarget(0);
    d.fx = null;
    d.fy = null;
}

function sim1(dataSim) {
    global_1or2 = 1;
    changeGraph("#graph_nw_linesSVG", "#graph_nw_lines", "_sim3", dataSim);
}

function sim2(dataSim) {
    global_1or2 = 2;
    changeGraph2("#graph_nw_linesSVG", "#graph_nw_lines", "_sim3", dataSim);
}

function sim1_2(dataSim) {if (global_1or2 == 1) { sim1(dataSim); } else { sim2(dataSim); }}

function updateLine(dataSimPoint, dataSim) {
    d3.select("#dataSimPoint").remove();
    // dimensions
    var height = 400;
    if (dataSim.simulation == 1) {
        var width = 695;
    }
    else {
        var width = 595;
    }

    var margin = {
      top: 40,
      bottom:75,
      left: 10,
      right: 150,
    };
    usage = width;

    lineSVG = d3.select("#graph_nw_linesSVG")
        .append("line")
            .attr("id", "dataSimPoint")
            .attr("x1", 48 + (dataSimPoint * width))
            .attr("y1", margin.top + 9)
            .attr("x2", 48 + (dataSimPoint * width))
            .attr("y2", 410 - margin.bottom)
            .attr("stroke-width", 2)
            .attr("stroke", "black");
}
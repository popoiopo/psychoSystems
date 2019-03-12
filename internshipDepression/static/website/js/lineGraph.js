function drawLineGraph(array_data, divRem, div, parasData, special="", figtitle="Symptoms activated during simulation", ytitle="# of active symptoms", xtitle="Number of iterations") {
  d3.select(divRem).remove();

  // dimensions
  var width = 750;
  var height = 400;

  var margin = {
      top: 40,
      bottom:75,
      left: 10,
      right: 50,
  };

  function zeroFill( number, width )
  {
    width -= number.toString().length;
    if ( width > 0 )
    {
      return new Array( width + (/\./.test( number ) ? 2 : 1) ).join( '0' ) + number;
    }
    return number + ""; // always return a string
  }

  // create an svg to draw in
  var svg = d3.select(div)
      .append("svg")
      .attr("id", divRem.slice(1))
      .attr("preserveAspectRatio", "xMinYMin meet")
      .attr("viewBox", "0 0 " + width + " " + height)
      .classed("svg-content", true)
      .append('g')
      .attr('transform', 'translate(' + margin.top + ',' + margin.left + ')');

  width = width - margin.left - margin.right;
  height = height - margin.top - margin.bottom;

  var parseTime = d3.timeParse("%Y"),
      bisectDate = d3.bisector(function(d) { return d.year; }).left;

  var x = d3.scaleTime().range([0, width]);
  var y = d3.scaleLinear().range([height, 0]);

  var line = d3.line()
      .x(function(d) { return x(d.year); })
      .y(function(d) { return y(d.value); });

  var g = svg.append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  svg.append("text").attr("x", margin.left)
                    .attr("y", margin.top/2)
                    .html(figtitle)
                    .attr("font-family", "Times New Roman")
                    .attr("font-size", "20px")
                    .attr("font-weight", "bold")
                    .attr("fill", "#6F257F");

  svg.append("text").attr("x", width)
                    .attr("y", height + margin.top + 35)
                    .html(xtitle)
                    .attr("font-family", "Times New Roman")
                    .attr("font-size", "15px")
                    .attr("font-weight", "bold")
                    .attr("fill", "#6F257F")
                    .attr("text-anchor", "end");

  // gridlines in y axis function
  function make_y_gridlines() {
      return d3.axisLeft(y);
  }

  var data = [];
  var N = array_data.length;
  xdata = Array.apply(null, {length: N}).map(Number.call, Number);
  xdata.forEach(function(d) {
    data.push({"year":parseTime(d), "value":array_data[d]});
  });

  x.domain(d3.extent(data, function(d) { return d.year; }));
  y.domain(d3.extent(data, function(d) { return d.value; }));

  // add the Y gridlines
  g.append("g")
      .attr("class", "grid")
      .call(make_y_gridlines()
          .tickSize(-width)
          .tickFormat("")
              .ticks(6)
      );

    g.append("g")
        .attr("class", "axis axis--y")
        .call(d3.axisLeft(y)
              .ticks(6)
             )
      .append("text")
        .attr("class", "axis-title")
        .attr("transform", "rotate(-90)")
        .attr("y", 6)
        .attr("dy", ".71em")
        .style("text-anchor", "end")
        .attr("fill", "#5D6971")
        .text(ytitle);

    g.append("path")
        .datum(data)
        .attr("class", "line")
        .attr("d", line);

    var dataText = [];

    if (special == "specific") {
      g.append("text")
        .attr("id", "specificText")
        .attr("class", "onhover_set")
        .attr("y", height + 10)
        .attr("x", margin.left)
        .attr("dy", ".71em")
        .style("text-anchor", "begin")
        .attr("fill", "#8b8d8f");
    }

    var focus = g.append("g")
        .attr("class", "focus")
        .style("display", "none");

    focus.append("line")
        .attr("class", "x-hover-line hover-line")
        .attr("y1", 0)
        .attr("y2", height);

    focus.append("circle")
        .attr("r", 15);

    focus.append("text")
        .attr("x", -10)
        .attr("y", 4)
        .attr("dy", ".15em")
        .style("fill", "#8b8d8f")
        .attr("font-family", "Times New Roman")
        .attr("font-size", "18px")
        .attr("font-weight", "bold");

    svg.append("rect")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
        .attr("class", "overlay")
        .attr("width", width)
        .attr("height", height)
        .on("mouseover", function() { focus.style("display", null); })
        .on("mouseout", function() { focus.style("display", "none"); })
        .on("mousemove", mousemove);

    function mousemove() {
      var x0 = x.invert(d3.mouse(this)[0]),
          i = bisectDate(data, x0, 1),
          d0 = data[i - 1],
          d1 = data[i],
          d = x0 - d0.year > d1.year - x0 ? d1 : d0;
      focus.attr("transform", "translate(" + x(d.year) + "," + y(d.value) + ")");
      focus.select("circle").attr("r", function(k) { if (Number.isInteger(d.value )) { return 15; } else { return 25; }});
      focus.select("text")
        .text(function() { if (Number.isInteger(d.value )) { return zeroFill(d.value, 2); } else { return zeroFill(d.value.toFixed(3), 2); }})
        .attr("x", function() { if (Number.isInteger(d.value )) { return  -10; } else { return -22; }});
      focus.select(".x-hover-line").attr("y2", height - y(d.value));
      focus.select(".y-hover-line").attr("x2", width + width);
      if (special == "specific") { g.select("#specificText").text(function() { return "Removed nodes [" + parasData[i] + "]"})};
    }
}


function drawSlider(div1, div2, extension, defaultVal=1.1) {
  var data1 = [0.5, 1, 1.5, 2, 2.5, 3];
  var data2 = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000];
  var width = 400;
  var height = 100;

  var slider1 = d3.sliderHorizontal()
    .min(d3.min(data1))
    .max(d3.max(data1))
    .width(width * (3/4))
    .tickFormat(d3.format('.2'))
    .ticks(5)
    .default(defaultVal)
    .on('onchange', val => {
      d3.select("p#value1" + extension).text(Math.round(val * 100) / 100);
    });

  var g = d3.select(div1).append("svg")
    .attr("preserveAspectRatio", "xMinYMin meet")
    .attr("viewBox", "0 0 400 100")
    .classed("svg-content", true)
    .append("g")
    .attr("transform", "translate(30,30)");

  var text = g.append("text")
    .attr("x", 0)
    .attr("y", 60)
    .attr("dy", ".15em")
    .style("fill", "#8b8d8f")
    .attr("font-family", "Times New Roman")
    .attr("font-size", "18px")
    .attr("font-weight", "bold")
    .text("C-Value");

  g.call(slider1);

  d3.select("p#value1" + extension).text(d3.format('.2')(slider1.value()));

  var slider2 = d3.sliderHorizontal()
    .min(d3.min(data2))
    .max(d3.max(data2))
    .width(width * (3/4))
    .tickFormat(d3.format('.2'))
    .ticks(5)
    .default(1500)
    .on('onchange', val => {
      d3.select("p#value2" + extension).text(2 * Math.round(val / 2));
    });

  var g = d3.select(div2).append("svg")
    .attr("preserveAspectRatio", "xMinYMin meet")
    .attr("viewBox", "0 0 " + width + " " + height)
    .classed("svg-content", true)
    .append("g")
    .attr("transform", "translate(30,30)");

  var text = g.append("text")
    .attr("x", 0)
    .attr("y", 60)
    .attr("dy", ".15em")
    .style("fill", "#8b8d8f")
    .attr("font-family", "Times New Roman")
    .attr("font-size", "18px")
    .attr("font-weight", "bold")
    .text("Number of Iterations");

  g.call(slider2);

  d3.select("p#value2" + extension).text(2 * Math.round(slider2.value() / 2));
}


function changeGraph(div1, div2, extension, data) {
  string = '{"simulation":1, "I":' + d3.select("p#value2" + extension).text() + ', "c":' + d3.select("p#value1" + extension).text() + '}';
  if (data) { drawLineGraph(data.D, div1, div2); } else {
    $.getJSON($SCRIPT_ROOT + '/_add_numbers', {
        a: string
      }, function(data) {
        data = JSON.parse(data);
        drawLineGraph(data["D"], div1, div2);
      });
  }
}


function adjacency() {
    var promiseWrapper = (d) => new Promise(resolve => d3.csv(d, (p) => resolve(p)));

    Promise.all([promiseWrapper("static/website/data/nodeList.csv"),promiseWrapper("static/website/data/edgeList.csv")]).then(resolve => {
        createAdjacencyMatrix(resolve[0],resolve[1]);
     });

    function createAdjacencyMatrix(nodes,edges){

      var width = 600;
      var height = 600;

      var edgeHash = {};
      edges.forEach(edge =>{
        var id = edge.source + "-" + edge.target;
        edgeHash[id] = edge;
      });

      var matrix = [];
      nodes.forEach((source, a) => {
        nodes.forEach((target, b) => {
          var grid = {id: source.id + "-" + target.id, x: b, y: a, weight: 0};
          if(edgeHash[grid.id]){
            grid.weight = edgeHash[grid.id].weight;
          }
        matrix.push(grid);
        });
      });

    var svg = d3.select("div#adjacencyDIV")
        .append("svg")
        .attr("id", "adjacency")
        .attr("preserveAspectRatio", "xMinYMin meet")
        .attr("viewBox", "0 0 " + width + " " + height)
        .classed("svg-content", true);

    var div = d3.select("body").append("div")
        .attr("class", "tooltip")
        .style("opacity", 0);

    svg.attr("align","center").append("g")
      .attr("transform","translate(50,50)")
      .attr("id","adjacencyG")
      .selectAll("rect")
      .data(matrix)
      .enter()
      .append("rect")
      .attr("class","grid")
      .attr("width",35)
      .attr("height",35)
      .attr("x", d=> d.x*35)
      .attr("y", d=> d.y*35)
      .style("fill", d => (d.weight < 0) ? 'red' : 'green')
      .style("fill-opacity", d=> Math.abs(d.weight) * .2);

    svg.append("g")
      .attr("transform","translate(50,45)")
      .selectAll("text")
      .data(nodes)
      .enter()
      .append("text")
      .attr("x", (d,i) => i * 35 + 17.5)
      .text(d => d.id)
      .style("text-anchor","middle")
      .style("font-size","10px");

    svg.append("g").attr("transform","translate(45,50)")
      .selectAll("text")
      .data(nodes)
      .enter()
      .append("text")
      .attr("y",(d,i) => i * 35 + 17.5)
      .text(d => d.id)
      .style("text-anchor","end")
      .style("font-size","10px");

    d3.selectAll("rect.grid").on("mouseover", function(d){
        div.transition()
         .duration(200)
         .style("opacity", .9);
       div.html(d.id + "<br/>" + d.weight)
         .style("left", (d3.event.pageX) + "px")
         .style("top", (d3.event.pageY - 28) + "px");
       gridOver(d);
       })
      .on("mouseout", function(d) {
        div.transition()
           .duration(500)
           .style("opacity", 0);
        gridOut(d);
      });

    function gridOver(d) {
      d3.select("svg#adjacency").selectAll("rect").style("stroke-width", function(p) { return p.x == d.x || p.y == d.y ? "3px" : "1px"; });
    }
    function gridOut(d) {
      d3.select("svg#adjacency").selectAll("rect").style("stroke-width", function(p) { return "1px"; });
    }
  }
}


function drawLineGraph2(array_data, divRem, div, title, yaxis,
  figtitle="Symptoms activated during simulation", ytitle="# of active symptoms", xtitle="Level of stress") {
  d3.select(divRem).remove();

  data_graph = []

  for (var i = 0; i < array_data["S"].length; i++) {
    data_graph.push({"S" : array_data["S"][i], "D" : array_data["DOWN"]["D"][i], "U" : array_data["UP"]["D"][i]});
  }

  // dimensions
  var width = 750;
  var height = 400;

  var margin = {
      top: 40,
      bottom:75,
      left: 10,
      right: 150,
  };

  function zeroFill( number, width )
  {
    width -= number.toString().length;
    if ( width > 0 )
    {
      return new Array( width + (/\./.test( number ) ? 2 : 1) ).join( '0' ) + number;
    }
    return number + ""; // always return a string
  }

  // create an svg to draw in
  var svg = d3.select(div)
      .append("svg")
      .attr("id", divRem.slice(1))
      .attr("preserveAspectRatio", "xMinYMin meet")
      .attr("viewBox", "0 0 " + width + " " + height)
      .classed("svg-content", true)
      .append('g')
      .attr('transform', 'translate(' + margin.top + ',' + margin.left + ')');

  width = width - margin.left - margin.right;
  height = height - margin.top - margin.bottom;

  var x = d3.scaleLinear().range([0, width]),
      y = d3.scaleLinear().range([height, 0]),
      bisectS = d3.bisector(function(d) { return d.S; }).left;

  var line1 = d3.line()
      .x(function(d) { return x(d["S"]); })
      .y(function(d) { return y(d["D"]); })
      .curve(d3.curveMonotoneX);

  var line2 = d3.line()
      .x(function(d) { return x(d["S"]); })
      .y(function(d) { return y(d["U"]); })
      .curve(d3.curveMonotoneX);

  var g = svg.append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  svg.append("text").attr("x", margin.left)
                    .attr("y", margin.top/2)
                    .html(figtitle)
                    .attr("font-family", "Times New Roman")
                    .attr("font-size", "20px")
                    .attr("font-weight", "bold")
                    .attr("fill", "#6F257F");

  svg.append("text").attr("x", width)
                    .attr("y", height + margin.top + 35)
                    .html(xtitle)
                    .attr("font-family", "Times New Roman")
                    .attr("font-size", "15px")
                    .attr("font-weight", "bold")
                    .attr("fill", "#6F257F")
                    .attr("text-anchor", "end");

  // gridlines in y axis function
  function make_y_gridlines() {
      return d3.axisLeft(y);
  }

  x.domain([-10,5]);
  y.domain([0,14]);

  // add the Y gridlines
  g.append("g")
      .attr("class", "grid")
      .call(make_y_gridlines()
          .tickSize(-width)
          .tickFormat("")
              .ticks(6)
      );

    g.append("g")
        .attr("class", "axis axis--y")
        .call(d3.axisLeft(y)
              .ticks(6)
             )
      .append("text")
        .attr("class", "axis-title")
        .attr("transform", "rotate(-90)")
        .attr("y", 6)
        .attr("dy", ".71em")
        .style("text-anchor", "end")
        .attr("fill", "#5D6971")
        .text(ytitle);

    g.append("g")
        .attr("class", "axis axis--x")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x)
              .ticks(15)
             );

    g.append("path")
        .datum(data_graph)
        .attr("class", "line")
        .attr("d", line1)
        .style("stroke", "#900C3E")
        .style("stroke-width", "2px")
        .style("opacity", "0.4");

    g.append("path")
        .datum(data_graph)
        .attr("class", "line")
        .attr("d", line2)
        .style("stroke", "#FFC300")
        .style("stroke-width", "2px")
        .style("opacity", "0.4");

    g.selectAll(".dot1")
        .data(data_graph)
      .enter().append("circle") // Uses the enter().append() method
        .attr("class", "dot1") // Assign a class for styling
        .attr("cx", function(d, i) { return x(d.S) })
        .attr("cy", function(d) { return y(d.D) })
        .attr("r", 3)
        .attr("fill", "#571845")
        .style("opacity", "1");

    g.selectAll(".dot2")
        .data(data_graph)
      .enter().append("circle") // Uses the enter().append() method
        .attr("class", "dot2") // Assign a class for styling
        .attr("cx", function(d, i) { return x(d.S) })
        .attr("cy", function(d) { return y(d.U) })
        .attr("r", 3)
        .attr("fill", "#FF5733")
        .style("opacity", "1");

    svg.append('rect')
        .attr("x", width + 20)
        .attr("y", 50)
        .attr("width", 10)
        .attr("height", 10)
        .style("fill", "#FF5733");

    svg.append('text')
        .attr("x", width + 38)
        .attr("y", 59)
    .html("Low &rarr; High")
        .attr("class", "textselected")
        .style("text-anchor", "start")
        .attr("font-family", "Times New Roman")
        .attr("font-size", "12px")
        .attr("font-weight", "bold");

    svg.append('rect')
        .attr("x", width + 20)
        .attr("y", 70)
        .attr("width", 10)
        .attr("height", 10)
        .style("fill", "#571845");

    svg.append('text')
        .attr("x", width + 38)
        .attr("y", 79)
    .html("High &rarr; Low")
        .attr("class", "textselected")
        .style("text-anchor", "start")
        .attr("font-family", "Times New Roman")
        .attr("font-size", "12px")
        .attr("font-weight", "bold");

    var focus = g.append("g")
        .attr("class", "focus")
        .style("display", "none");

    focus.append("line")
        .attr("class", "x-hover-line hover-line")
        .attr("y1", 0)
        .attr("y2", height);

    focus.append("circle")
        .attr("id", "down")
        .attr("r", 15);

    focus.append("circle")
        .attr("id", "up")
        .attr("r", 15);

    focus.append("text")
        .attr("id", "downtext")
        .attr("x", -10)
        .attr("y", 4)
        .attr("dy", ".15em")
        .style("fill", "#8b8d8f")
        .attr("font-family", "Times New Roman")
        .attr("font-size", "18px")
        .attr("font-weight", "bold");

    focus.append("text")
        .attr("id", "uptext")
        .attr("x", -10)
        .attr("y", 4)
        .attr("dy", ".15em")
        .style("fill", "#8b8d8f")
        .attr("font-family", "Times New Roman")
        .attr("font-size", "18px")
        .attr("font-weight", "bold");

    svg.append("rect")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
        .attr("class", "overlay")
        .attr("width", width)
        .attr("height", height)
        .on("mouseover", function() { focus.style("display", null); })
        .on("mouseout", function() { focus.style("display", "none"); })
        .on("mousemove", mousemove);

    function mousemove() {
      var x0 = x.invert(d3.mouse(this)[0]),
          i = bisectS(data_graph, x0, 1),
          d0 = data_graph[i - 1],
          d1 = data_graph[i],
          d = x0 - d0.S > d1.S - x0 ? d1 : d0;
      focus.select("#down").attr("transform", "translate(" + x(d.S) + "," + y(d.D) + ")");
      focus.select("#up").attr("transform", "translate(" + x(d.S) + "," + y(d.U) + ")");
      focus.select("#downtext")
        .attr("transform", "translate(" + x(d.S) + "," + y(d.D) + ")")
        .text(function() { return zeroFill(d.D, 2); });
      focus.select("#uptext")
        .attr("transform", "translate(" + x(d.S) + "," + y(d.U) + ")")
        .text(function() { return zeroFill(d.U, 2); });
      focus.select(".x-hover-line")
        .attr("transform", "translate(" + x(d.S) + "," + y(d.U) + ")")
        .attr("y2", y(d.D) - y(d.U));
      focus.select(".y-hover-line")
        .attr("transform", "translate(" + x(d.S) + "," + y(d.U) + ")")
        .attr("x2", width + width);
    }
}


function changeGraph2(div1,div2,extension,data) {
  string2 = '{"simulation":2, "I":' + d3.select("p#value2" + extension).text() + ', "c":' + d3.select("p#value1" + extension).text() + '}';
  if (data) { drawLineGraph2(data, div1, div2); } else {
    $.getJSON($SCRIPT_ROOT + '/_add_numbers', {
        a: string2
      }, function(data) {
        data = JSON.parse(data);
        drawLineGraph2(data, div1, div2);
      });
  }
}


function initFunctions(array_data) {
  if (array_data.simulation == 1) {
    drawLineGraph(array_data.D, "#graphSVG1", "div#lineGraph");
    drawSlider("div#slider1", "div#slider2", "");
  }
  else if (array_data.simulation == 2) {
    drawLineGraph2(array_data, "#graphSVG2", "#lineGraph_sim2");
    drawSlider("div#slider1_sim2", "div#slider2_sim2", "_sim2");
  }
}

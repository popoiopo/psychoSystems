function gridData() {
    temp_y_vars = Object.assign([], x_y_vars["y_vars"].slice().reverse())
	// iterate for rows	
	for (var row = 0; row < numRows; row++) {
		data.push( new Array() );
		
		// iterate for cells/columns inside rows
		for (var column = 0; column < numCols; column++) {
            if (Object.keys(factorDict).includes(temp_y_vars[row]) &&
                Object.keys(factorDict[temp_y_vars[row]]).includes(x_y_vars["x_vars"][column])) {

    			data[row].push({
    				x: xpos + margin.left,
    				y: ypos +  margin.top,
    				width: cell_width,
    				height: cell_height,
                    click: click,
                    xvars: x_y_vars["x_vars"][column],
                    yvars: temp_y_vars[row],
                    factors: factorDict[temp_y_vars[row]][x_y_vars["x_vars"][column]]
    			})
            } else {
                data[row].push({
                    x: xpos + margin.left,
                    y: ypos +  margin.top,
                    width: cell_width,
                    height: cell_height,
                    click: click,
                    xvars: x_y_vars["x_vars"][column],
                    yvars: temp_y_vars[row],
                    factors: []
                })
            }

			// increment the x position. I.e. move it over by 50 (width variable)
			xpos += cell_width;
		}
		// reset the x position after a row is complete
		xpos = 1;
		// increment the y position for the next row. Move it down 50 (height variable)
		ypos += cell_height;	
	}
	return data;
}

var x_y_vars = {"x_vars" : temp_aspects, 
            "y_vars" : spat_aspects};
var cur_var = {"x_vars" : temp_aspects[0], "y_vars" : spat_aspects[0]};
var cur_filter = "x_vars";
// gridData[gridData.length - 1][gridData[gridData.length - 1].length - 1].y + height

var margin = {
        top:70,
        right: 120,
        bottom: 30,
        left: 90
    },
    grid_width = 630 - margin.left - margin.right,
    grid_height = 410 - margin.top - margin.bottom,
    cell_width = grid_width / x_y_vars["x_vars"].length,
    cell_height = grid_height / x_y_vars["y_vars"].length,
    data = new Array(),
    xpos = 1,
    ypos = 1,
    numRows = x_y_vars["y_vars"].length,
    numCols = x_y_vars["x_vars"].length,
    axisMargin = 5,
    click = 0,
    maxFactor = 40,
    gridcellWidth = grid_width / maxFactor,
    prev_target = "Miliseconds_Biology",
    prev_rc = "Miliseconds",
    target,
    cur_rc;
    
// Define 'div' for tooltips
var div = d4.select("body")
	.append("div")  // declare the tooltip div 
	.attr("class", "tooltip")              // apply the 'tooltip' class
  .style("opacity", 0);                  // set the opacity to nil
  
// Define 'div' for tooltips
var hoverdiv = d4.select("body")
	.append("div")  // declare the tooltip div 
	.attr("class", "hovertip")              // apply the 'tooltip' class
	.style("opacity", 0);                  // set the opacity to nil

var gridData = gridData();	
// I like to log the data to the console for quick debugging
console.log(gridData);

var grid = d4.select("#grid")
  .append("div")
    .classed("svg-container", true) //container class to make it responsive
  .append("svg")
    //   //responsive SVG needs these 2 attributes and no width and height attr
    // .attr("preserveAspectRatio", "xMinYMin meet")
    // .attr("viewBox","0 0 " + grid_width + " " + grid_height)
    // //class to make it responsive
    // .classed("svg-content-responsive", true); 
        .attr("width", grid_width + margin.left + margin.right)
        .attr("height", grid_height + margin.top + margin.bottom);
    
var xScale = d4.scalePoint()
    .rangeRound([0, grid_width - cell_width])
    .domain(x_y_vars["x_vars"]);

var yScale = d4.scalePoint()
    .rangeRound([grid_height - cell_height, 0])
    .domain(x_y_vars["y_vars"]);

var xAxis = d4.axisBottom(xScale),
    yAxis = d4.axisLeft(yScale);

grid.append("g")
    .attr("class", "x axis ")
    .attr('id', "axis--x")
    .style("line", "red")
    .attr("transform", "translate(" + (margin.left + (cell_width/2)) + "," + (grid_height + margin.top + axisMargin) + ")")
    .call(xAxis);

grid.append("g")
    .attr("class", "y axis ")
    .attr('id', "axis--y")
    .attr("transform", "translate(" + (margin.left - axisMargin) + "," + (margin.top + (cell_height/2)) + ")")
    .call(yAxis);
	
var row = grid.selectAll(".row")
	.data(gridData)
	.enter().append("g")
    .attr("class", "row");

// LEGEND AND COLOR SCALE
    
var color = d4.scaleSequential(d4.interpolateHsl("white", "#1f3891"))
  .domain([0, maxFactor]);
  
var linearScale = d4.scaleLinear()
	.domain([0, maxFactor])
	.range([0, grid_width]);

var sequentialScale = d4.scaleSequential()
	.domain([maxFactor, 0]);

function dots(d) {
	sequentialScale
		.interpolator(function(t) { return d4.interpolateHsl("#1f3891", "white")(t)});

	d4.select(this)
		.selectAll('rect')
		.data(d4.range(0, maxFactor))
		.enter()
        .append('rect')
        .attr("transform", "translate(" + margin.left + "," + (margin.top - 30) + ")")
		.attr('x', function(d) {
			return linearScale(d);
		})
		.attr('width', gridcellWidth)
    .attr('height', 20)
    .attr('opacity', 0.85)
		.style('fill', function(d) {
			return sequentialScale(d);
        });

    d4.select(this)
        .append("g")
        .attr("class", "axis")
        .attr("transform", "translate(" + margin.left + "," + (margin.top - 30) + ")")
        .call(d4.axisTop(linearScale));

    // text label for the x axis
    d4.select(this).append("text")  
    .attr("class", "axisText")           
    .attr("transform",
            "translate(" + margin.left + "," + (margin.top - 55) + ")")
    .style("text-anchor", "left")
    .text("Amount of factors within Spatio Temporal gridcell")
    .style("stroke", "#c4c4c4")
    .style("font-size", "14px")
    .style("stroke-opacity", 0.75);
}

grid
	.selectAll('g.interpolator')
	.data(['interpolateViridis'])
	.enter()
	.append('g')
	.classed('interpolator', true)
	.each(dots);
  
// CREATING GRID

var column = row.selectAll(".square")
	.data(function(d) { return d; })
	.enter().append("rect")
	.attr("class",function(d) {return "square " + d.xvars + " " + d.yvars})
	.attr("x", function(d) { return d.x; })
    .attr("y", function(d) { return d.y; })
    .attr("id", function(d) { return d.xvars + "_" + d.yvars})
	.attr("width", function(d) { return d.width; })
	.attr("height", function(d) { return d.height; })
	.style("fill", "#fff")
  .style("stroke", "#c4c4c4")
  .style("opacity", 0.85)
  .on('mouseover', function(d) { 
    d4.select(this).style("stroke", "#636262").style("stroke-width", 2);
    hoverdiv.transition()
            .duration(500)	
            .style("display", "")
            .style("opacity", 0);
    hoverdiv.transition()
        .duration(200)	
        .style("opacity", .85);	
    hoverdiv	.html(
      '<div id="hoverbox">' +
          '<p id="hoverP" style="color:white; margin-bottom:15px;">' + d.xvars + ' - ' + d.yvars + '</p>' + 
      '</div>'
      )	 
      .style("left", (d4.event.pageX) + "px")			 
      .style("top", (d4.event.pageY - 28) + "px");
  })
  .on('mouseout', function() { d4.select(this).style("stroke", "#c4c4c4").style("stroke-width", 1);
  hoverdiv.transition()
    .duration(500)	
    .style("display", "")
    .style("opacity", 0);
  })
	.on('click', function(d) {
        cur_var["x_vars"] = d.xvars;
        cur_var["y_vars"] = d.yvars;

        if (cur_filter == "x_vars") {var variable = "y_vars"; cur_rc = d.yvars;}
        else {var variable = "x_vars"; cur_rc = d.xvars;};

        updateTable();  

        hoverdiv
            .style("display", "")
            .style("opacity", 0);

        div.transition()
            .duration(500)	
            .style("display", "")
            .style("opacity", 0);
        div.transition()
            .duration(200)	
            .style("opacity", .85)
            .on("end", () => d4.select("#hoverInput").node().focus());	

        target = d.xvars + "_" + d.yvars

        div.html(
            '<div id="box" onclick="checking()"><center>' +
                '<span class="fa-stack fa-lg closingTip" onclick="closeTTip(\'.tooltip\')">'+
                    '<i class="fa fa-times-circle fa-stack-2x fa-inverse"></i>'+
                '</span>' +
                '<p style="color: white; font-weight: bold; margin:5px;">' + d.xvars + ' - ' + d.yvars + '</p>' + 
                '<input id="hoverInput" style="margin-bottom:70px" type="text" name="factorName" id="factorInput" placeholder="Enter Factor-name"/>' +
            '</center></div>'
            )	 
            .style("left", function() { return (d4.event.pageX) + "px"; })
            .style("top", (d4.event.pageY - 28) + "px");

        $("#hoverInput").keyup(function(event) {
          if (event.keyCode === 13) {
              setData_color(target, event.target.value)
          }
        });

        d4.selectAll("." + prev_rc).attr("rx", 0).attr("ry", 0);
        d4.selectAll("." + cur_rc).attr("rx", 10).attr("ry", 10);
        prev_rc = cur_rc;
        d4.select("#tableFactor").html(" (" + cur_var[variable] + ")")
    });

function checking() {
    console.log("doet wel iets");
}

function closeTTip(tool) {
    console.log(tool);
    console.log("HAllooo?!?");
    var ttip = d4.select(tool)
        .transition()
        .duration(500)
        .style("display", "none");
}

function setData_color(d, newFactor) {
    if (newFactor == "") {return};

    var ttip = d4.select(".tooltip").style("display", "none");      
    var xyVars = d.split("_")

    var xIndex = x_y_vars["x_vars"].indexOf(xyVars[0]);
    var yIndex = x_y_vars["y_vars"].slice().reverse().indexOf(xyVars[1]);
    
    gridData[yIndex][xIndex].factors.push(newFactor);
    d4.select("#"+d).style("fill",function(e) { if (gridData[yIndex][xIndex].factors.length == 0) { return "white" } else { return color(gridData[yIndex][xIndex].factors.length) }});        

    newData[newFactor] = {}
    newData[newFactor]["temp_aspect"] = x_y_vars["x_vars"].indexOf(xyVars[0]);
    newData[newFactor]["spat_aspect"] = x_y_vars["y_vars"].slice().reverse().indexOf(xyVars[1]);

    console.log(newData);
    updateTable();
}
gridData.forEach(function(d, i) {
    d.forEach(function(cell, k) {
        d4.select("#" + cell.xvars + "_" + cell.yvars).style("fill",function(e) { if (gridData[i][k].factors.length == 0) { return "white" } else { return color(gridData[i][k].factors.length) }});
    });
});

function saveData() {
  console.log(newData);
  var posting = JSON.stringify(newData);
  $.ajax({
    url: '/submitNewNodes',
    contentType: "application/json; charset=utf-8",
    data: posting,
    type: 'POST',
    success: function(response ,jqxhr, settings) {
      console.log(response);
      console.log(jqxhr);
      console.log(settings);
    },
    error: function(error, jqxhr, settings) {
      console.log(error);
      console.log(jqxhr);
      console.log(settings);
      alert("Something has gone wrong with submitting your data to the database. Please contact the server administrator.")
    }
  });
}
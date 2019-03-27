window.onload = function() {

  var svg = d4.select("#circlePacking"),
      diameter = +svg.attr("width");


  if (placings == "presentation") {var margin = 70;} else {var margin = 20;}

  function getTransX(placings) {
    if (placings == "presentation") {var backgroundColoring = "#002A38"; var transx = diameter / 2;} 
    else {var backgroundColoring = "#FAFAFA"; var transx = window.innerWidth/2;}
    return backgroundColoring, transx
  }
  
  var backgroundColoring, transx = getTransX(placings);

  var g = svg.append("g").attr("transform", "translate(" + transx  + "," + diameter / 2 + ")");

  window.onresize = function() { backgroundColoring, transx = getTransX(placings); 
                                 g.attr("transform", "translate(" + transx + "," + diameter / 2 + ")"); };

  var color = d4.scaleLinear()
      .domain([-1, 6])
      .range(["hsl(152,80%,80%)", "hsl(228,30%,40%)"])
      .interpolate(d4.interpolateHcl);

  // Define our scales
  var colorScale = d4.scaleOrdinal(d4.schemeCategory10);

  var pack = d4.pack()
      .size([diameter - margin, diameter - margin])
      .padding(2);

  var div = d4.select("body").append("div")
      .attr("class", "circletip")
      .style("opacity", 0);

  root = d4.hierarchy(root)
      .sum(function(d) { return d.size; })
      .sort(function(a, b) { return b.value - a.value; });

  var focus = root,
      nodes = pack(root).descendants(),
      view;

  function hashCode(str) { // java String#hashCode
    var hash = 0;
    for (var i = 0; i < str.length; i++) {
       hash = str.charCodeAt(i) + ((hash << 5) - hash);
    }
    return hash;
  } 

  function intToRGB(i){
      var c = (i & 0x00FFFFFF)
          .toString(16)
          .toUpperCase();

      return "00000".substring(0, 6 - c.length) + c;
  }

  var circle = g.selectAll("circle")
    .data(nodes)
    .enter().append("circle")
      .attr("class", function(d) { return d.parent ? d.children ? "node" : "node node--leaf" : "node node--root"; })
      .style("fill", function(d) {
        var rightColor;
        if (!d.children) {
          if (d.data.name.substr(d.data.name.length - 3) == "(P)") {
            rightColor = "#ffcc00";
          }
          else if (d.data.name.substr(d.data.name.length - 3) == "(T)") {
            rightColor = "#08db2b";
          }
          else if (d.data.name.substr(d.data.name.length - 3) == "(N)") {
            rightColor = "#" + intToRGB(hashCode(d.data.name));
          }
          else if (d.data.name.substr(d.data.name.length - 3) == "(X)") {
            rightColor = "red";
          }
        }
        return d.children ? color(d.depth) : rightColor;
      })
      .style("opacity", function(d) {
        return d.children ? "1" : ".6";
      })
      .on("click", function(d) { if (focus !== d) zoom(d), d4.event.stopPropagation(); })
      .on("mouseover", function(d) { 
        if (placings != "presentation") {
          var color = colorScale(d.data.name);
          var htmlData = getHTML(d);
          div.transition()
            .duration(200)
            .style("opacity", .9);
          div.html(htmlData)
            .style("left", (d4.event.pageX) + "px")
            .style("top", (d4.event.pageY - 28) + "px");
        }
      })
     .on("mouseout", function(d) {
        if (placings != "presentation") {
           div.transition()
             .duration(500)
             .style("opacity", 0);
        }
       });

  var text = g.selectAll("text")
    .data(nodes)
    .enter().append("text")
      .attr("class", "label")
      .style("fill-opacity", function(d) { return d.parent === root ? 1 : 0; })
      .style("display", function(d) { return d.parent === root ? "inline" : "none"; })
      .style("fill", function(d) { if (placings != "presentation") { return "black"; } else { return "white";}})
      .style("font-size", function(d) { if (placings == "presentation"){return "15px"}})
      .text(function(d) {
        if (!d.children) {
          if (d.data.name.substr(d.data.name.length - 3).includes(["(P)", "(T)", "(N)", "(X)"])) {
            return d.data.name.substr(0, d.data.name.length - 3);
          }
          else {return d.data.name;}
        }
        else {return d.data.name;}
      });

  var node = g.selectAll("circle,text");

  svg
      .style("background", backgroundColoring)
      .on("click", function() { zoom(root); });

  zoomTo([root.x, root.y, root.r * 2 + margin]);

  function getHTML(d) {
    var pName;
    peopleNames = "<p style='color:white;'><small><span style='font-weight:bold; margin-bottom:10px; display:block;'>" + d.data.name + "</span>"
    for (var i = 0; i < d.data.children.length; i++) {
      if (!d.data.children[i].children) {
          if (d.data.children[i].name.substr(d.data.children[i].name.length - 3) == "(P)") {
            peopleNames += d.data.children[i].name.substr(0, d.data.children[i].name.length - 3) + "<span style='color: transparent;  text-shadow: 0 0 0 rgb(255, 204, 0); ';> &plusmn;</span><br/>";
          }
          else if (d.data.children[i].name.substr(d.data.children[i].name.length - 3) == "(T)") {
            peopleNames += d.data.children[i].name.substr(0, d.data.children[i].name.length - 3) + "<span style='color: transparent;  text-shadow: 0 0 0 rgb(8, 219, 43); color=#08db2b'> &#10004;</span><br/>";
          }
          else if (d.data.children[i].name.substr(d.data.children[i].name.length - 3) == "(N)") {
            peopleNames += d.data.children[i].name.substr(0, d.data.children[i].name.length - 3) + "<span style='color: transparent;  text-shadow: 0 0 0 rgb(194, 4, 219); color=#c204db'> &#9899;</span><br/>";
          }
          else if (d.data.children[i].name.substr(d.data.children[i].name.length - 3) == "(X)") {
            peopleNames += d.data.children[i].name.substr(0, d.data.children[i].name.length - 3) + "<span style='color: transparent;  text-shadow: 0 0 0 rgb(255, 0, 0); color=red'> &times;</span><br/>";
          }
          else {peopleNames += d.data.children[i].name + "<br/>";}
        }
        else {peopleNames += d.data.children[i].name + "<br/>";}
    }
    peopleNames += "</p></small>";
    return peopleNames;
  }

  function zoom(d) {
    var focus0 = focus; focus = d;

    var transition = d4.transition()
        .duration(d4.event.altKey ? 7500 : 750)
        .tween("zoom", function(d) {
          var i = d4.interpolateZoom(view, [focus.x, focus.y, focus.r * 2 + margin]);
          return function(t) { zoomTo(i(t)); };
        });

    transition.selectAll("text")
      .filter(function(d) { return d.parent === focus || this.style.display === "inline"; })
        .style("fill-opacity", function(d) { return d.parent === focus ? 1 : 0; })
        .on("start", function(d) { if (d.parent === focus) this.style.display = "inline"; })
        .on("end", function(d) { if (d.parent !== focus) this.style.display = "none"; });
  }

  function zoomTo(v) {
    var k = diameter / v[2]; view = v;
    node.attr("transform", function(d) { return "translate(" + (d.x - v[0]) * k + "," + (d.y - v[1]) * k + ")"; });
    circle.attr("r", function(d) { return d.r * k; });
  }
}
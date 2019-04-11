var margin = { top: 100, right: 120, bottom: 130, left: 120 };
var width = 500;
var height = 800;

const nodePadding = 40;

const circularLinkGap = 2;

var sankey = d4.sankey()
    .nodeWidth(10)
    .nodePadding(nodePadding)
    .nodePaddingRatio(0.5)
    .scale(0.5)
    .size([width, height])
    .nodeId(function (d) {
    return d.name;
    })
    .nodeAlign(d4.sankeyJustify)
    .iterations(32);

function drawSankey() {
    d4.select(".sankeyChart").remove();

    var data = dataSankey;

    var svg = d4.select("#chart").append("svg")
        .attr("class", "sankeyChart")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom);

    var g = svg.append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")")

    var linkG = g.append("g")
        .attr("class", "links")
        .attr("fill", "none")
        .attr("stroke-opacity", 0.2)
        .selectAll("path");

    var nodeG = g.append("g")
        .attr("class", "nodes")
        .attr("font-family", "sans-serif")
        .attr("font-size", 10)
        .selectAll("g");

    //run the Sankey + circular over the data
    let sankeyData = sankey(data);
    let sankeyNodes = sankeyData.nodes;
    let sankeyLinks = sankeyData.links;

    let depthExtent = d4.extent(sankeyNodes, function (d) { return d.depth; });

    var nodeColour = d4.scaleSequential(d4.interpolateCool)
    .domain([0,width]);


    //Adjust link Y coordinates based on target/source Y positions

    var node = nodeG.data(sankeyNodes)
        .enter()
        .append("g");

    node.append("rect")
        .attr("x", function (d) { return d.x0; })
        .attr("y", function (d) { return d.y0; })
        .attr("height", function (d) { return d.y1 - d.y0; })
        .attr("width", function (d) { return d.x1 - d.x0; })
        .style("fill", function (d) { return nodeColour(d.x0); })
        .style("opacity", 0.5)
        .on("mouseover", function (d) {

        let thisName = d.name;

        node.selectAll("rect")
            .style("opacity", function (d) {
            return highlightNodes(d, thisName)
            })

        d4.selectAll(".sankey-link")
            .style("opacity", function (l) {
            return l.source.name == thisName || l.target.name == thisName ? 1 : 0.3;
            })

        node.selectAll("text")
            .style("opacity", function (d) {
            return highlightNodes(d, thisName)
            })
        })
        .on("mouseout", function (d) {
        d4.selectAll("rect").style("opacity", 0.5);
        d4.selectAll(".sankey-link").style("opacity", 0.7);
        d4.selectAll("text").style("opacity", 1);
        })

    node.append("text")
        .attr("x", function (d) { return (d.x0 + d.x1) / 2; })
        .attr("y", function (d) { return d.y0 - 12; })
        .attr("dy", "0.35em")
        .attr("text-anchor", "middle")
        .text(function (d) { return d.name; });

    node.append("title")
        .text(function (d) { return d.name + "\n" + (d.value); });

    var link = linkG.data(sankeyLinks)
        .enter()
        .append("g")

    link.append("path") 
        .attr("class", "sankey-link")
        .attr("d", sankeyPath)
        .style("stroke-width", function (d) { return Math.max(1, d.width); })
        .style("opacity", 0.7)
        .style("stroke", function (link, i) {
        return link.circular ? "red" : "black"
        })



    link.append("title")
        .text(function (d) {
        return d.source.name + " → " + d.target.name + "\n Index: " + (d.index);
        });


    //ARROWS
    var arrowsG = linkG.data(sankeyLinks)
        .enter()
        .append("g")
        .attr("class", "g-arrow")
        .call(appendArrows, 10, 10, 4) //arrow length, gap, arrow head size

    arrowsG.selectAll("path")
        .style("stroke-width", "10")
        //.style("stroke-dasharray", "10,10")

        arrowsG.selectAll(".arrow-head").remove()

    let duration = 5
    let maxOffset = 10;
    let percentageOffset = 1;

    var animateDash = setInterval(updateDash, duration);

    function updateDash() {

        arrowsG.selectAll("path")
        .style("stroke-dashoffset", percentageOffset * maxOffset)

        percentageOffset = percentageOffset == 0 ? 1 : percentageOffset - 0.01

    }

    function highlightNodes(node, name) {

        let opacity = 0.3

        if (node.name == name) {
        opacity = 1;
        }
        node.sourceLinks.forEach(function (link) {
        if (link.target.name == name) {
            opacity = 1;
        };
        })
        node.targetLinks.forEach(function (link) {
        if (link.source.name == name) {
            opacity = 1;
        };
        })

        return opacity;

    }
};

drawSankey();
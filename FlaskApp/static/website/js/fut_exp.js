function fut_expGraph(file, divRem, div, simulation) {
  d3.json("static/website/data/averages" + file + ".json", function(error, graph) {
    if (error) throw error;
    if (parseInt(file) < 1) {
      drawLineGraph(graph["Averages" + file], divRem, div, "", "", figtitle="Time not in MD", ytitle="% of time", xtitle="Symptoms");
    }
    else {
      drawLineGraph(graph["Averages" + file], divRem, div, graph["Paras"+file], special="specific", figtitle="Time not in MD", ytitle="% of time", xtitle="Symptoms", special="specific");
    }
  });
}
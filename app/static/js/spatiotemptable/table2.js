function getData() {
    data_keys = x_y_vars[cur_filter]
    data_table = [];
    data_keys.forEach(function(key, i) {
        data_table.push({title: key.replace("_", " "),
                         field: key, sorter:"string", 
                         headerFilter:"input", 
                         validator:"required",
                         }) // cellClick:function(e, cell){clickFunction(e, cell);}
    });

    if (cur_filter == "x_vars") {var variable = "y_vars"}
    else {var variable = "x_vars"};

    if (cur_filter == "x_vars") {
        var index = x_y_vars[variable].slice().reverse().indexOf(cur_var[variable])
    }
    else {
        var index = x_y_vars[variable].indexOf(cur_var[variable])
    }
    var tableData = []

    if (cur_filter == "x_vars") {
        var longVar = 0
        for (var x = 0; x < gridData[index].length; x++) {
            if (gridData[index][x]["factors"].length > longVar) {
                longVar = gridData[index][x]["factors"].length
            }
        }
        for (var i = 0; i < longVar; i++) {
            var tempAll = {}
            for (var x = 0; x < gridData[index].length; x++) {
                if (typeof gridData[index][x]["factors"][i] !== 'undefined') {
                    tempAll[gridData[index][x]["xvars"]] = gridData[index][x]["factors"][i]
                }
                else {tempAll[gridData[index][x]["xvars"]] = "-"}
            }
            tempAll["id"] = i
            tableData.push(tempAll)
        }
    }
    if (cur_filter == "y_vars") {
        var longVar = 0
        for (var x = 0; x < gridData.length; x++) {
            if (gridData[x][index]["factors"].length > longVar) {
                longVar = gridData[x][index]["factors"].length
            }
        }
        for (var i = 0; i < longVar; i++) {
            var tempAll = {}
            for (var x = 0; x < gridData.length; x++) {
                if (typeof gridData[x][index]["factors"][i] !== 'undefined') {
                    tempAll[gridData[x][index]["yvars"]] = gridData[x][index]["factors"][i]
                }
                else {tempAll[gridData[x][index]["yvars"]] = "-"}
            }
            tempAll["id"] = i
            tableData.push(tempAll)
        }
    }
    return [tableData, data_table]
};

function clickFunction(e, cell) {
    console.log(event.clientX, event.clientY)
    console.log(d3.event)
    var tableTip = d4.select(".tableTip");
    console.log(tableTip);
    tableTip.transition()
            .duration(500)	
            .style("display", "")
            .style("opacity", 0);
    tableTip.transition()
        .duration(200)	
        .style("opacity", .85)
        .on("end", () => d4.select("#hoverInput").node().focus());	

    tableTip.html(
        '<div id="box>' +
            '<div id="icon" onclick="closeTTip(\'.tableTip\')"><i style="color:white; margin-bottom:5px; margin-top:10px;" class="far fa-2x fa-times-circle"></i> </div>' +
            '<p style="color: white;"><b>' + cell.getValue() + '</b></p>' + 
            '<input id="hoverInput" style="margin-bottom:15px" type="text" name="factorName" id="factorInput" placeholder="Enter Factor-name"/>' +
        '</div>'
        );
    console.log(cell.getValue());
    console.log(e);
    console.log(cell);
}

var q2 = noYesBtns('#q1')
    .nTxt('Temporal')
    .yTxt('Spatial')
    .on('_click', function () {
        d3.select(this).style('background', '#FDBB30');
        if (this.firstChild.data == "Temporal") {
            cur_filter = "x_vars"
        }
        else if (this.firstChild.data == "Spatial") {
            cur_filter = "y_vars"
        }
        
        d3.select("#tableTitle").html("Filter factors on <span style='color:#FDBB30;'>" + this.firstChild.data + "</span> aspect")
        if (cur_filter == "x_vars") {var variable = "y_vars";}
        else {var variable = "x_vars"; };
        d4.select("#tableFactor").html(" (" + cur_var[variable] + ")")

        d4.selectAll("." + prev_rc).attr("rx", 0).attr("ry", 0);
        d4.selectAll("." + cur_var[variable]).attr("rx", 10).attr("ry", 10);
        prev_rc = cur_var[variable]
        
        table.destroy();
        updateTable("destroy");
        table = newTable();

    })
    .render();

d3.select('#Temporal').style('background', "#FDBB30")

function updateTable(ud) {
    if (ud == "destroy") {
        var gotD = getData();
        tableData = gotD[0];
        data_table = gotD[1];
    }
    else {
        var gotD = getData();
        tableData = gotD[0];
        data_table = gotD[1];
        table.replaceData(tableData);
    };
}

var init = 0;
var gotD = getData();
var tableData = gotD[0], 
    data_table = gotD[1];
init += 1;

var table = newTable();

function newTable() {
    var table = new Tabulator("#example-table", {
        height:425,
        data:tableData, //load initial data into table
        pagination:"local",
        paginationSize:8,
        movableColumns:true,
        layout:"fitData", //fit columns to width of table (optional)
        columns: data_table,
        clipboard:true,
        tooltips:function(cell){
            //cell - cell component

            //function should return a string for the tooltip of false to hide the tooltip
            return  cell.getColumn().getField() + " - " + cell.getValue(); //return cells "field - value";
        },
    });

    return table
}
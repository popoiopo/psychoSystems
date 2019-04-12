function getData(fieldTitle) {
    var data_table = [{title: fieldTitle,
                        field: fieldTitle, sorter:"string",
                        formatter:function(cell, formatterParams){
                            var value = cell.getValue();
                            return "<span font-weight:bold;'>" + value + "</span>";
                        },
                        headerFilter:"input", 
                        validator:"required",
                        },
                        {title: "Spatial",
                        field: "Spatial", sorter:"string", 
                        formatter:function(cell, formatterParams){
                            var value = cell.getValue();
                            return "<span style='color:steelblue; font-weight:bold;'>" + value + "</span>";
                        },
                        headerFilter:"input", 
                        validator:"required",
                        },
                        {title: "Temporal",
                        field: "Temporal", sorter:"string", 
                        formatter:function(cell, formatterParams){
                            var value = cell.getValue();
                            return "<span style='color:steelblue; font-weight:bold;'>" + value + "</span>";
                        },
                        headerFilter:"input", 
                        validator:"required",
                        }];

    var tableData = []
    for (let i = 0; i < nodes.length; i++) {
        tableData.push({[fieldTitle] : nodes[i].factor,
                        "Spatial": dropDowns["spat_aspects"][nodes[i].spat_aspect_id-1],
                        "Temporal":dropDowns["temp_aspects"][nodes[i].temp_aspect_id-1]})
    }
    return [tableData, data_table]
}

function createRel() {
    if (newFrom == newTo) {alert("Self enforcing relations can't be defined at this stage. In the next stage this is possible."); return }
    var con_strength = document.getElementById("edge-con_strength").value;
    var temp_aspect = document.getElementById("edge-temp_aspect_id").value;
    dataSankey["links"].push({ "source":newFrom, "target":newTo, "value":con_strength*10, "temp_aspect":temp_aspect});

    var sankeyNodes = [];
    dataSankey["nodes"].forEach(function(d){ sankeyNodes.push(d.name) })
    if (!sankeyNodes.includes(newFrom)) { console.log(sankeyNodes, newFrom); dataSankey["nodes"].push({"name":newFrom})};
    if (!sankeyNodes.includes(newTo)) { console.log(sankeyNodes, newTo); dataSankey["nodes"].push({"name":newTo})};

    newData.push({ "source":factorIDDict[newFrom], "target":factorIDDict[newTo], "value":con_strength, "temp_aspect":temp_aspect});

    drawSankey();
}

var init = 0;
var fromData = getData("From");
var toData = getData("To");
var tableData = {"From":{"data":fromData[0], "columns":fromData[1]}, "To":{"data":toData[0], "columns":toData[1]}}
var factorIDDict = nodes.reduce(function(obj, x) {
    obj[x["factor"]]= x["id"]; 
    return obj;
 }, {});
init += 1;

for (var key in tableData) {
    var table = newTable();

    function newTable() {
        var table = new Tabulator("#" + key + "-table", {
            height:350,
            data:tableData[key]["data"], //load initial data into table
            pagination:"local",
            paginationSize:8,
            movableColumns:true,
            selectable:1,
            layout:"fitColumns", //fit columns to width of table (optional)
            columns: tableData[key]["columns"],
            clipboard:true,
            rowClick:function(e, row){
                if (Object.keys(row._row.data)[0] == "To") { 
                    newTo = row._row.data.To; }
                else if (Object.keys(row._row.data)[0] =="From") { 
                    newFrom = row._row.data.From };
            },
        });

        return table
    }
}

function saveData() {
    console.log(newData);
    var posting = JSON.stringify(newData);
    newData = []
    $.ajax({
      url: '/submitNewEdges',
      contentType: "application/json; charset=utf-8",
      data: posting,
      type: 'POST',
      success: function(response ,jqxhr, settings) {
        newData = {}
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
function clickFunction(e, cell) {
    if (cell._cell.column.field == "To") { 
        if (prevTo) {
            prevTo.originalTarget.style.backgroundColor = "white";
        }
        newTo = cell._cell.value; 
        prevTo = e; }
    else if (cell._cell.column.field =="From") { 
        if (prevFrom) {
            prevFrom.originalTarget.style.backgroundColor = "white";
        }
        newFrom = cell._cell.value; 
        prevFrom = e;};
    e.originalTarget.style.backgroundColor = "steelblue";
    console.log(newFrom, newTo);
}

function getData(fieldTitle) {
    var data_table = [{title: fieldTitle,
                        field: fieldTitle, sorter:"string", 
                        headerFilter:"input", 
                        validator:"required",
                        cellClick:function(e, cell){clickFunction(e, cell);}
                        }];

    var tableData = []
    for (let i = 0; i < nodes.length; i++) {
        tableData.push({[fieldTitle] : nodes[i].factor})
    }
    return [tableData, data_table]
}

function createRel() {
    var con_strength = document.getElementById("edge-con_strength").value;
    var temp_aspect = document.getElementById("edge-temp_aspect_id").value;
    console.log(data);
    data.push({ "source":newFrom, "target":newTo, "value":con_strength, "temp_aspect":temp_aspect});
    newData.push({ "source":newFrom, "target":newTo, "value":con_strength, "temp_aspect":temp_aspect});
}

var init = 0; 
var fromData = getData("From");
var toData = getData("To");
var tableData = {"From":{"data":fromData[0], "columns":fromData[1]}, "To":{"data":toData[0], "columns":toData[1]}}
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
            layout:"fitColumns", //fit columns to width of table (optional)
            columns: tableData[key]["columns"],
            clipboard:true,
            tooltips:function(cell){
                //cell - cell component

                //function should return a string for the tooltip of false to hide the tooltip
                return  cell.getColumn().getField() + " - " + cell.getValue(); //return cells "field - value";
            },
        });

        return table
    }
}
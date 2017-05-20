function create_selector(values, cell, row_index) {
  var selectList = document.createElement("select");
  selectList.setAttribute("class", "name_selector");
  selectList.setAttribute("name", row_index + ".name_selector");

  cell.appendChild(selectList);
  for (var i = 0; i < values.length; i++) {
      var option = document.createElement("option");
      var text = values[i][0] + " " + values[i][1] + " " + values[i][2]
      option.value = text;
      option.text = text;
      option.setAttribute("discipline", values[i][3]);
      selectList.appendChild(option);
  }
}

function append_text_input(cell, text_class, master_id, index) {
  input = document.createElement("input");
  input.setAttribute("type", "text");
  input.setAttribute("class", text_class);
  input.setAttribute("name", index + "." + text_class);
  input.value = document.getElementById(master_id).value;
  cell.appendChild(input);
}
function create_row(entries) {
  var table = document.getElementById("main_table");
  var row = table.insertRow(-1);

  var index = 0;
  var datecell = row.insertCell(index++);
  append_text_input(datecell, "date", "master_date", row.rowIndex);

  var namecell = row.insertCell(index++);
  create_selector(entries, namecell, row.rowIndex);

  var disccell = row.insertCell(index++);
  var name = "\"" + row.rowIndex + ".discipline\"";
  disccell.innerHTML = "<input type=\"text\" class=\"discipline\" name="+ name + ">";

  var drawcell = row.insertCell(index++);
  var name = "\"" + row.rowIndex + ".dweight\"";
  drawcell.innerHTML = "<input type=\"text\" class=\"dweight\" name=" + name + ">";

  var distcell = row.insertCell(index++);
  append_text_input(distcell, "distance", "master_distance", row.rowIndex);

  var targetcell = row.insertCell(index++);
  append_text_input(targetcell, "target_size", "master_target_size", row.rowIndex);

  var tourncell = row.insertCell(index++);
  var name = "\"" + row.rowIndex + ".tournament\"";
  tourncell.innerHTML = "<input type=\"checkbox\" class=\"tournament\" name=" + name + ">";

  var scorecell = row.insertCell(index++);
  var name = "\"" + row.rowIndex + ".score\"";
  scorecell.innerHTML = "<input type=\"text\" class=\"score\" name=" + name + ">";

  var numcell = row.insertCell(index++);
  append_text_input(numcell, "num_arrows", "master_num_arrows", row.rowIndex);

  var notescell = row.insertCell(index++);
  var name = "\"" + row.rowIndex + ".notes\"";
  notescell.innerHTML = "<textarea class=\"notes\" name=" + name + "></textarea>";
}

$(document).ready(function(){
  // When master row changes, change table rows
    $("#master_date").change(function(){
        $(".date").val(this.value);
    });

    $("#master_distance").change(function(){
        $(".distance").val(this.value);
    });

    $("#master_target_size").change(function(){
        $(".target_size").val(this.value);
    });

    $("#master_tournament").change(function(){
        $(".tournament").prop("checked", this.checked);
    });

    $("#master_num_arrows").change(function(){
        $(".num_arrows").val(this.value);
    });

    // Need to use "on" so that this works with dynamically created elements
    $("form").on("change", ".name_selector", function(){
        var optionSelected = $("option:selected", this);
        var valueSelected = this.value;
        $(this).closest('td').next('td').find('input').val(
          optionSelected.attr("discipline"));
        // var cell = $(this).parent();
        // var next_cell = cell.next();
        // next_cell.
        //attr("discipline")
    });

    $(".name_selector").change(function(){
      alert("so far so good");
    });
});

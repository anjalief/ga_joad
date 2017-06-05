function build_table(data) {
    var html = "<table id=main_table><thead>\
             <tr><th></th>\
                 <th>Name</th>\
                 <th>Present?</th>\
             </tr></thead><tbody>";
    var already_entered = false;
    // iterate through rows
    for (var i = 0, len = data.length; i < len; ++i) {
        var child_count = i + 1;
        html += '<tr>';
// set up columns
        html += '<td>' + child_count + '</td>';
        html += '<td>' + data[i].firstname + " " + data[i].lastname + '</td>';
        if (data[i].checked) {
            html += '<td>' + "<input type=\"checkbox\" name=\"" + data[i].id + "_present_chx\" checked>" + '</td>';
            already_entered = true;
        } else {
            html += '<td>' + "<input type=\"checkbox\" name=\"" + data[i].id + "_present_chx\">" + '</td>';
        }
        html += "</tr>";
    }
    html += '</tbody></table>';
    if (already_entered) {
       html += '<div>Note: attendance was already entered, any changes will overwrite exisiting data</div>';
    }

    html += "<input type=hidden name=selected_date value=" + $('#datepicker').val() +  ">"
    $('#display_result').html(html);

    // set up action buttons
    var add_row_btn = '<input type=button class=add_row_btn value="Add Row">';
    $(add_row_btn).appendTo("#display_result").bind('click', create_row);

    var submit_btn = '<input type=submit value="Update attendance">';
    $(submit_btn).appendTo("#display_result");
}

function create_name_selector(archers, cell, row_index) {
  var selectList = document.createElement("select");
  selectList.setAttribute("class", "name_selector");
  selectList.setAttribute("name", row_index + "_name_selector");

  cell.appendChild(selectList);
  for (var i = 0; i < archers.length; i++) {
      var option = document.createElement("option");
      var text = archers[i].id + " " + archers[i].firstname + " " + archers[i].lastname
      option.value = text;
      option.text = text;
      selectList.appendChild(option);
  }
}

function create_date_picker(parent, id_str) {
  var inputter = document.createElement("input");

  inputter.setAttribute("type", "text");
  inputter.setAttribute("class", "date_picker");
  inputter.setAttribute("id", "date_picker_" + id_str);
  inputter.setAttribute("name", "date_picker_" + id_str);

  inputter.setAttribute("value", id_str);

  parent.appendChild(inputter);
}

function create_go_btn(parent, button_text) {
  var go_btn = document.createElement("button");
  go_btn.setAttribute("type", "submit");
  console.log(button_text);
  go_btn.innerHTML = button_text;

  parent.appendChild(go_btn);
}

function create_row() {
var table = document.getElementById("main_table");
var row = table.insertRow(-1);

var index = 0;
var countcell = row.insertCell(index++);
countcell.innerHTML = row.rowIndex;

var namecell = row.insertCell(index++);
create_name_selector($ARCHERS, namecell, row.rowIndex);

var chx_cell = row.insertCell(index++);
chx_cell.innerHTML = '<td>' + "<input type=\"checkbox\" name=\"" + "manual_" + row.rowIndex + "_present_chx\" checked>" + '</td>';
}

$(function() {
    // set up ui
    $(document).on('focus',".date_picker", function(){
        $(this).datepicker();
    });

    // set up reschedule form
    var reschedule_form = document.getElementById("reschedule_form");
    create_name_selector($ARCHERS, reschedule_form, 0);

    create_date_picker(reschedule_form, "from");
    create_date_picker(reschedule_form, "to");
    create_go_btn(reschedule_form, "Reschedule");

    // set up extra practice input
    var extra_practice_form = document.getElementById("extra_practice_form");
    create_name_selector($ARCHERS, extra_practice_form, 0);
    create_date_picker(extra_practice_form, "");
    create_go_btn(extra_practice_form, "Enter Extra Practice");


    // create bindings for dynamic elements
    // When Go! btn is clicked, query database for date
    $('#go_btn').bind('click', function() {
      $.getJSON($SCRIPT_ROOT + '/attendance_list', {
        date: $('#datepicker').val()
      }, function(data) {
        build_table(data);
      });
      return false;
    });
  });


  $("form").on("click", ".add_row_btn", function(){
    create_row();
});

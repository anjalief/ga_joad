function setField(fieldname, fieldindex, selected_entry) {
		var field = document.getElementById(fieldname);
		field.value = selected_entry[fieldindex];
}
// when an archer is selected, populate fields
// with current values for archer
function populateArcher(entrs) {
		var dropdown = document.getElementById("modifier");
		// index 1 is blank for new archer
		var OFFSET = 1;
		var index = dropdown.selectedIndex - OFFSET;

		var selected_row;
		if (index < 0) {
			selected_row = ["", "", "", "", "", "", ""];
		} else {
			selected_row = entrs[index];
		}

		setField("firstname", 1, selected_row);
		setField("lastname", 2, selected_row);
		setField("bday", 3, selected_row);
		setField("discipline", 4, selected_row);
		setField("gender", 5, selected_row);
		setField("day", 6, selected_row);
}

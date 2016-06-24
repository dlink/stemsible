function addSchoolRow() {
    document.form1.add_school_row.value = 1;
    document.form1.submit();
}
function saveNewSchool() {
    document.form1.save_new_school.value = 1;
    document.form1.submit();
}
function deleteSchool(user_school_id, school_info) {
    var r = confirm('Are you sure you want to delete\n\n' + school_info + '?');
    if (r == true) {
	document.form1.delete_user_school.value = user_school_id;
	document.form1.submit();
    }
}
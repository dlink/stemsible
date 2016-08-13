function addSchoolRow() {
    document.si_form.add_school_row.value = 1;
    document.si_form.submit();
}
function saveNewSchool() {
    document.si_form.save_new_school.value = 1;
    document.si_form.submit();
}
function deleteSchool(user_school_id, school_info) {
    var r = confirm('Are you sure you want to delete\n\n' +
                    unescape(school_info) + '?');
    if (r == true) {
	document.si_form.delete_user_school.value = user_school_id;
	document.si_form.submit();
    }
}

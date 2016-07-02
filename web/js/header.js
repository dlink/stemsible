function toggleHeaderMenu() {
    if ($('#header-menu').css('display') == 'none') {
	$('#header-menu').show();
    } else {
	$('#header-menu').hide();
    }	
}
function logout() {
    $("input[name=logout]").val('Logout');
    $("form[name=header-form]").submit();
}


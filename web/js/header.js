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

/* submit search field on enter */

$(document).ready(function() {
  $('.submit-on-enter').keydown(function(event) {
      if (event.keyCode == 13) {
          $("form[name=header-search-form]").submit();
          return false;
      }
  });
  $('#forgotpw-link').click(function(){
      $('#forgotpw-panel').toggle();
  });
});

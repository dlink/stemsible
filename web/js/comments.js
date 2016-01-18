function addComment() {
    var pos = $(document).scrollTop();
    $("input[name=scroll_pos]").val(pos);
    $("form[name=form1]").submit();
}

function toggleComments(comments_id) {
    if ($('#'+comments_id).css('display') == 'none') {
	$('#'+comments_id).show();
    } else {
	$('#'+comments_id).hide();
    }
}

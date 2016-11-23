function addComment() {
    // var pos = $(document).scrollTop();

    // comment will be at the top of page
    // scroll down 175px just below the new message card
    $("input[name=scroll_pos]").val(175);

    $("form[name=messages-form]").submit();
}

function toggleComments(comments_id) {
    if ($('#'+comments_id).css('display') == 'none') {
        $('#'+comments_id).show();
    } else {
        $('#'+comments_id).hide();
    }
}

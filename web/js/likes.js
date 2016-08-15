
function toggleLike(like_id) {
    var pos = $(document).scrollTop();
    $("input[name=scroll_pos]").val(pos);
    $("input[name=like]").val(like_id);
    $("form[name=messages-form]").submit();
}

function toggleLikers(likes_id) {
    if ($('#'+likes_id).css('display') == 'none') {
        showLikers(likes_id);
    } else {
        hideLikers(likes_id);
    }
}

function showLikers(likers_id) {
    $('#'+likers_id).show();
}

function hideLikers(likers_id) {
    $('#'+likers_id).hide();
}

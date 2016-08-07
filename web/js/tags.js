function search(search_term) {
    $('#search').val(search_term)
    $("form[name=header-search-form]").submit();
}

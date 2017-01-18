function search(search_term) {
    form = document.getElementById("header-search-form")
    form['search'].value = search_term;
    form.submit();
}
function school_search(sid) {
    form = document.getElementById("school-search-form")
    form['school_search'].value = sid
    form.submit()
}

function search(search_term) {
    form = document.getElementById("header-search-form")
    form['search'].value = search_term;
    form.submit();
}

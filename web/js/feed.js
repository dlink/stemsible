$(document).ready(function() {
    
    // Expand new message text box when you click in
    var e = document.getElementById("newMessageText");
    e.onfocus = function () {
	e.style.height = "120px";
    }

    // Expand new comment text box when you click in
    var es = document.getElementsByClassName('newCommentText');
    [].forEach.call(es, function(e) {
	e.onfocus = function () {
	    e.style.height = "120px";
	}
    });
});


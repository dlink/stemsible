$( document ).ready(function() {
    var schools = new Bloodhound({
        datumTokenizer: Bloodhound.tokenizers.whitespace,
        queryTokenizer: Bloodhound.tokenizers.whitespace,
        // url points to a json file that contains an school data
        prefetch: {
            ttl: 0, // 1,
            url: 'data/schools.json'
        }
    });

    // School Type ahead
    $('#school .typeahead').typeahead(null, {
        name: 'schools',
        source: schools
    });

    // password strength meter
    $('#password1').keyup(function(e) {
        var strongRegex = new RegExp("^(?=.{8,})(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*\\W).*$", "g");
        var mediumRegex = new RegExp("^(?=.{7,})(((?=.*[A-Z])(?=.*[a-z]))|((?=.*[A-Z])(?=.*[0-9]))|((?=.*[a-z])(?=.*[0-9]))).*$", "g");
        var enoughRegex = new RegExp("(?=.{6,}).*", "g");
        if (false == enoughRegex.test($(this).val())) {
            $('#passstrength').html('More Characters');
        } else if (strongRegex.test($(this).val())) {
            $('#passstrength').className = 'ok';
            $('#passstrength').html('Strong!');
        } else if (mediumRegex.test($(this).val())) {
            $('#passstrength').className = 'alert';
            $('#passstrength').html('Medium!');
        } else {
            $('#passstrength').className = 'error';
            $('#passstrength').html('Weak!');
        }
        return true;
    });

    $('#password2').keyup(function(e) {
        if ($('#password1').val() == $(this).val()) {
            $('#passmatch').className = 'ok';
            $('#passmatch').html('Match!');
        } else {
            $('#passmatch').className = 'error';
            $('#passmatch').html("Does not match");
        }
    });

});

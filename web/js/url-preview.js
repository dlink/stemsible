$(document).ready(function(){
    var form = $('form[name="new-card-form"]');
    var input = $('.newMessageText');

    // Embedly preview plugin
    input.preview({key:'339bba310808442c8479798d9d44126f'});

    // For testing
    input.val('https://vimeo.com/182906334').blur();
});

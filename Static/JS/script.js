$(document).ready(function() {
    $('#autocomplete').on('input', function() {
        var prefix = $(this).val();
        if (prefix.length > 0) {
            $.get('/autocomplete', { prefix: prefix }, function(data) {
                $('#suggestions').empty();
                data.forEach(function(suggestion) {
                    $('#suggestions').append('<li>' + suggestion + '</li>');
                });
            });
        } else {
            $('#suggestions').empty();
        }
    });
});
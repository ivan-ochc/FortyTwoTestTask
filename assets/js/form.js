$(function() {
    $( "#id_date_of_birth" ).datepicker({dateFormat: "yy-mm-dd"});
});

$(function() {
    var form = $("#contactform");
    form.submit(function (e) {
        $("#message").empty()
        $("#loading-div").show()
        $("#ajaxform").load(
            form.attr('action') + ' #ajaxform',
            form.serializeArray(),
            function (responseText, responseStatus) {
                $("#loading-div").hide()
                $("#message").prepend('Contact data were successfully updated')
                $( "#id_date_of_birth" ).datepicker({dateFormat: "yy-mm-dd"});
            }
        );
        e.preventDefault();
    });
});
$(document).ready(function() {
            function block_form() {
                $("#message").empty()
                $("#loading-div").show()
            }

            function unblock_form() {
                setTimeout(function() {
                        $("#loading-div").hide();
                }, 1000);
            }

            var options = {
                beforeSubmit: function(form, options) {
                    block_form();
                },
                success: function() {
                     $('.errorlist').remove();
                    unblock_form();
                    $("#message").prepend('Team was successfully created')
                },
                error:  function(resp) {
                    $('.errorlist').remove();
                    unblock_form();
                    var errors = JSON.parse(resp.responseText);
                    for (error in errors) {
                        var id = '#id_' + error;
                        $(id).parent('div').prepend(errors[error]);
                    }
                }
            };

            $('#teamform').ajaxForm(options);
        });

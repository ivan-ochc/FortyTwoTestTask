$(function() {
    $( "#id_date_of_birth" ).datepicker({dateFormat: "yy-mm-dd"});
});

$(document).ready(function() {
            function block_form() {
                $("#message").empty()
                $("#loading-div").show()
            }

            function unblock_form() {
                setTimeout(function() {
                        $("#loading-div").hide();
                }, 1000);
                $( "#id_date_of_birth" ).datepicker({dateFormat: "yy-mm-dd"});
            }

            var options = {
                beforeSubmit: function(form, options) {
                    block_form();
                },
                success: function() {
                     $('.errorlist').remove();
                    unblock_form();
                    $("#message").prepend('Contact data were successfully updated')
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

            $('#contactform').ajaxForm(options);
        });


function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();

            reader.onload = function (e) {
                $("img").show()
                $('#image_preview').attr('src', e.target.result);
            }

            reader.readAsDataURL(input.files[0]);
        }
    }
$(function() {
    $("#id_image").change(function () {
        readURL(this);
    });
});
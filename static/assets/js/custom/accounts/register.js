$(document).ready(function () {
    // ajax email validation
    $(document).on("keyup", ".js-validate-email , .js-validate-email2", function () {
        var email = $(this).val();
        var url = document.getElementById('js-validate-email-error').getAttribute('data-url');
        
        $.ajax({
            url: url,
            type: 'GET',
            data: { email: email },
            success: function (data) {
                if (data.is_email_taken) {
                    $('.js-validate-email-error').text(data.error_message).show()
                    $('#signup').attr('disabled', 'disabled');
                }
                else {
                    $('.js-validate-email-error').hide();
                    $('#signup').removeAttr('disabled');
                }
            }
        });
    });

    // ajax emails validation
    $(document).on("keyup", ".js-validate-email , .js-validate-email2", function () {
        var email1 = document.getElementById('id_email').value;
        var email2 = document.getElementById('id_email2').value;
        
        if (email1 && email2) {
            if (email1 != email2) {
                $('.js-validate-email1-error').text("The two emails don't match.").show()
                $('.js-validate-email2-error').text("The two emails don't match.").show()
                $('#signup').attr('disabled', 'disabled');
            }
            else {
                $('.js-validate-email2-error').hide();
                $('.js-validate-email1-error').hide();
                $('#signup').removeAttr('disabled');
            }
        }
        else {
            $('.js-validate-email2-error').hide();
            $('.js-validate-email1-error').hide();
            $('#signup').removeAttr('disabled');
        }
    });

    // ajax passwords validation
    $(document).on("keyup", ".js-validate-password1 , .js-validate-password2", function () {
        var password1 = document.getElementById('id_password1').value;
        var password2 = document.getElementById('id_password2').value;
        
        if (password1 && password2) {
            if (password1 != password2) {
                $('.js-validate-password1-error').text("The two passwords don't match.").show()
                $('.js-validate-password2-error').text("The two passwords don't match.").show()
                $('#signup').attr('disabled', 'disabled');
            }
            else {
                $('.js-validate-password2-error').hide();
                $('.js-validate-password1-error').hide();
                $('#signup').removeAttr('disabled');
            }
        }
        else {
            $('.js-validate-password2-error').hide();
            $('.js-validate-password1-error').hide();
            $('#signup').removeAttr('disabled');
        }
    });

})    

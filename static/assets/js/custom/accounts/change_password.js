$(document).ready(function () {

    // ajax passwords validation
    $(document).on("keyup", ".js-validate-password1 , .js-validate-password2", function () {
        var password1 = document.getElementById('id_new_password1').value;
        var password2 = document.getElementById('id_new_password2').value;
        
        if (password1 && password2) {
            if (password1 != password2) {
                $('.js-validate-password1-error').text("The two passwords don't match.").show()
                $('.js-validate-password2-error').text("The two passwords don't match.").show()
                $('#change-password').attr('disabled', 'disabled');
            }
            else {
                $('.js-validate-password2-error').hide();
                $('.js-validate-password1-error').hide();
                $('#change-password').removeAttr('disabled');
            }
        }
        else {
            $('.js-validate-password2-error').hide();
            $('.js-validate-password1-error').hide();
        }
    });

})    

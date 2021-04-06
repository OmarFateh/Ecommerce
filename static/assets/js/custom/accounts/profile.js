$(document).ready(function () {
    // tabs
    // function openTab(evt, tabName) {
    //     // Declare all variables
    //     var i, tabcontent, tablinks;
      
    //     // Get all elements with class="tabcontent" and hide them
    //     tabcontent = document.getElementsByClassName("tabcontent");
    //     for (i = 0; i < tabcontent.length; i++) {
    //       tabcontent[i].style.display = "none";
    //     }
      
    //     // Get all elements with class="tablinks" and remove the class "active"
    //     tablinks = document.getElementsByClassName("tablinks");
    //     for (i = 0; i < tablinks.length; i++) {
    //       tablinks[i].className = tablinks[i].className.replace(" active", "");
    //     }
      
    //     // Show the current tab, and add an "active" class to the button that opened the tab
    //     document.getElementById(tabName).style.display = "block";
    //     evt.currentTarget.className += " active";
    // }

    $(document).on("click", ".tablinks", function (e) {
        var tabId = $(this).data("index")
        openTab(e, tabId)
    })
    
    // ajax email validation
    $(document).on("keyup", ".js-validate-email", function () {
        var email = $(this).val();
        var url = document.getElementById('js-validate-email-error').getAttribute('data-url');

        $.ajax({
            url: url,
            type: 'GET',
            data: { email: email },
            success: function (data) {
                if (data.is_email_taken) {
                    $('.js-validate-email-error').text(data.error_message).show()
                    $('#save').attr('disabled', 'disabled');
                }
                else {
                    $('.js-validate-email-error').hide();
                    $('#save').removeAttr('disabled');
                }
            }
        });
    });

    // Update Student Profile.
    $(document).on("submit", "#update-profile-form", function () {
        var form = $(this);
        var fd = new FormData(this);

        $.ajax({
            url: form.attr("action"),
            data: fd,
            type: form.attr("method"),
            dataType: 'json',
            processData: false,
            contentType: false,
            success: function (data) {
                if (data.form_is_valid) {
                    $("#partial-profile-form").html(data.html_form);
                    $(window).scrollTop(0);
                    $('.message').text(data.success_message).show()
                    // messages timeout for 5 sec
                    setTimeout(function () { $('.message').fadeOut('slow'); }, 5000);
                }
            }
        });
        return false;
    });

    // delete item from favourite list
    $(document).on("click", ".delete-favourite-btn", function () {
        $.ajax({
            url: $('#wishlist-table').data("url"),
            type: 'POST',
            data: { 
                product_id: $(this).data("index"), 
                csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
                action: 'delete',
            },
            success: function (data) {
                $('#wishlist-table tbody').html(data.html_list_data);  
                $(".wishlist-count").text(data.wishlist_count);
            },
        }) 
    });

    /* Reviews */
    const handleStarSelect = (size) => {
        childeren =  Array.from(document.querySelectorAll('#product-review-rate input')).reverse()
        childeren[size - 1].checked = true;
    }
    
    const loadRateValue = function (productIdVal) {
        $.ajax({
            url: starRateUrl,
            type: 'GET',
            data: { product_id: productIdVal },
            success: function (response) {
                handleStarSelect(response.rate)
            },
        })
    }

    var loadForm = function (actionType, btn) {
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            data: {action: actionType},
            dataType: 'json',
            beforeSend: function () {
                $("#modal-review").modal("show");
            },
            success: function (data) {
                $("#modal-review .modal-content").html(data.html_form);
                loadRateValue(btn.attr("data-index"))
            }
        });
    };

    var saveForm = function (actionType, form, rateVal) {
        $.ajax({
            url: form.attr("action"),
            data: form.serialize() + "&action="+ actionType + "&rate="+ rateVal,
            type: form.attr("method"),
            dataType: 'json',
            success: function (data) {
                if ( data.form_is_valid ) {
                    $("#reviews-table tbody").html(data.html_reviews_list);
                    $("#modal-review").modal("hide");
                    $('.review-success-message').text(data.success_message).show()
                    // messages timeout for 5 sec
                    setTimeout(function () { $('.review-success-message').fadeOut('slow'); }, 5000);
                }
                else {
                    $("#modal-review .modal-content").html(data.html_form);
                }
            }
        });
        return false;
    };

    // update review
    $(document).on("click", ".update-review", function (e) {
        loadForm("update", $(this));
    })
    $(document).on("submit", ".js-update-review-form", function (e) {
        e.preventDefault();
        rateVal = $("input[name=rate]:checked").val()
        saveForm("update", $(this), rateVal);
    })

    // delete review
    $(document).on("click", ".delete-review", function (e) {
        loadForm("delete", $(this));
    })
    $(document).on("submit", ".js-delete-review-form", function (e) {
        e.preventDefault();
        saveForm("delete", $(this));
    })

})    

$(document).ready(function () {
    
    // fetch selected color name
    const getColorName = function (variations) {
        $(document).on("click", 'input:radio[name=option-0]', function () {
            var colorId = $("input[name=option-0]:checked").val();
            var colorName = variations.filter(obj => obj.color.id == colorId)[0].color.name;
            $('#color-name').text(colorName);
        });
    }

    // fetch colors & selected size name
    const getSizeNameColors = function (variations) {
        $(document).on("click", 'input:radio[name=option-1]', function () {
            var sizeId = $("input[name=option-1]:checked").val();
            var productVariations = variations.filter(obj => obj.size.id == sizeId);
            // fetch color of selected size
            var div_data = "";
                for (key in productVariations) {
                    if (productVariations.hasOwnProperty(key)) {
                        div_data += "<div class='swatch-element color'>";
                        div_data += "<input class='swatchInput' id='swatch-" + productVariations[key]['color']['name'] + "' type='radio' name='option-0' value='" + productVariations[key]['color']['id'] + "'>";
                        div_data += "<label class='swatchLbl small' for='swatch-" + productVariations[key]['color']['name'] + "' title='" + productVariations[key]['color']['name'] + "' style='background-color:" + productVariations[key]['color']['code'] + ";'></label>";
                        div_data += "</div>";
                    }
                }
                $("#product-color").html(div_data);
            // fetch selected size name
            var sizeName = productVariations[0].size.name;
            $('#size-name').text(sizeName);
            $('#color-name').text("");
        });
    } 

    // slick slider
    const productThumb = function (){
        $('.product-dec-slider-2').slick({
            infinite: true,
            slidesToShow: 6,
            vertical: true,
            verticalSwiping: true,
            centerPadding: '0',
            draggable: true, 
            slidesToScroll: 1
        });
    }

    // product zoom
    const productZoom = function (){
        $(".zoompro").elevateZoom({
            gallery: "gallery",
            galleryActiveClass: "active",
            zoomWindowWidth: 300,
            zoomWindowHeight: 100,
            scrollZoom: false,
            zoomType: "inner",
            cursor: "crosshair"
        });
    }

    // fetch images of size
    const getSizeImages = function (images) {
        $(document).on("click", 'input:radio[name=option-1]', function () {
            $('.product-dec-slider-2').slick('unslick');
            var sizeId = $("input[name=option-1]:checked").val();
            var sizeImages = images.filter(obj => obj.size.id == sizeId);
            var div_data = "";
            var div_data2 = "";
            var div_data3 = "<img id='zoompro' class='zoompro' src='" + sizeImages[0].image + "' data-zoom-image='" + sizeImages[0].image + "' alt=''/>";
            sizeImages.forEach(function (key, i) {
                var j = Number(i) + Number(1);
                div_data += "<a class='slick-slide' aria-hidden='true' tabindex='-1' data-image='" + key.image + "' ";
                div_data += "data-zoom-image='" + key.image + "' data-slick-index='" + j +"'>";
                div_data += "<img class='blur-up lazyload' data-src='" + key.image + "' src='" + key.image + "' alt='' />";
                div_data += "</a>";
                div_data2 += "<a href='" + key.image + "' data-size='1000x1280'></a>";
            });
            
            $("#gallery").html(div_data);
            $("#light-box-images").html(div_data2);
            $("#zoompro-span").html(div_data3);
            productThumb();
            productZoom();
            //$(".product-dec-slider-2").not('.slick-initialized').slick();
        });
    }

    // fetch images of selected color & size
    const getSizeColorImages = function (images) {
        $(document).on("click", 'input:radio[name=option-0]', function () {
            $('.product-dec-slider-2').slick('unslick');
            var colorId = $("input[name=option-0]:checked").val();
            var sizeId = $("input[name=option-1]:checked").val();
            var colorImages = images.filter(obj => obj.color.id == colorId && obj.size.id == sizeId);
            var div_data = "";
            var div_data2 = "";
            var div_data3 = "<img id='zoompro' class='zoompro' src='" + colorImages[0].image + "' data-zoom-image='" + colorImages[0].image + "' alt=''/>";
            colorImages.forEach(function (key, i) {
                var j = Number(i) + Number(1);
                div_data += "<a class='slick-slide' aria-hidden='true' tabindex='-1' data-image='" + key.image + "' ";
                div_data += "data-zoom-image='" + key.image + "' data-slick-index='" + j +"'>";
                div_data += "<img class='blur-up lazyload' data-src='" + key.image + "' src='" + key.image + "' alt='' />";
                div_data += "</a>";
                div_data2 += "<a href='" + key.image + "' data-size='1000x1280'></a>";
            });
            
            $("#gallery").html(div_data);
            $("#light-box-images").html(div_data2);
            $("#zoompro-span").html(div_data3);
            productThumb();
            productZoom();
           
        });
    }

    // fetch variation data
    var variationUrl = document.getElementById('partial-product-size').getAttribute('data-url');
    $.ajax({
        url: variationUrl,
        type: 'GET',
        success: function (response) {
            getColorName(response.data)
            getSizeNameColors(response.data)
        },
        error: function (error) {
            console.log(error)
        },
    })

    // fetch images data
    var imageUrl = document.getElementById('gallery').getAttribute('data-url');
    $.ajax({
        url: imageUrl,
        type: 'GET',
        success: function (response) {
            getSizeColorImages(response.data)
            getSizeImages(response.data)
        },
    })
    
    // add to cart 
    $(document).on("submit", '#product-form', function (e) {
        e.preventDefault();
        $.ajax({
            url: $(this).data("url"),
            type: 'POST',
            data: { 
                product_id: $("#add-to-cart-btn").val(), 
                size_id: $("input[name=option-1]:checked").val(), 
                color_id: $("input[name=option-0]:checked").val(), 
                product_qty: $("#Quantity").val(), 
                csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
            },
            success: function (data) {
                $('#minicart-drawer').html(data.html_mini_cart_data); 
                document.getElementById('cart-qty-count').innerHTML = data.qty
            },
        }) 
    })

    /* Functions */
    var loadForm = function ( btn ) {
        $.ajax({
            url: btn.attr("modal-url"),
            type: 'get',
            dataType: 'json',
            data: { product_id: $("#add-to-cart-btn").val() },
            beforeSend: function () {
                if ( btn.hasClass("delete-review") ) {
                    $("#modal-login .modal-dialog").removeClass('modal-xl');
                }
                $("#modal-login").modal("show");
            },
            success: function (data) {
                $("#modal-login .modal-content").html(data.html_form);

            }
        });
    };

    var loginForm = function () {
        var form = $(this);
        var customerEmail = $("#customer-email").val();
        var customerPassword = $("#customer-password").val();
        $.ajax({
            url: form.attr("action"),
            data: form.serialize() + "&email="+ customerEmail + "&password="+ customerPassword + "&action="+ "login",
            type: form.attr("method"),
            dataType: 'json',
            success: function (data) {
                if ( data.form_is_valid ) {
                    window.location.reload();
                }
                else {
                    $("#modal-login .modal-content").html(data.html_form);
                    $(".error-message").removeClass("d-none");
                    $(".error-message-text").text(data.error_message);
                }
            }
        });
        return false;
    };
    
    var registerForm = function () {
        var form = $(this);
        $.ajax({
            url: form.attr("action"),
            data: form.serialize() + "&action="+ "register",
            type: form.attr("method"),
            dataType: 'json',
            success: function (data) {
                if ( data.form_is_valid ) {
                    window.location.reload();
                }
                else {
                    $("#modal-login .modal-content").html(data.html_form);
                }
            }
        });
        return false;
    };

    // toggle item from favourite list
    $(document).on("click", "#add-to-wishlist-btn", function () {
        var btn = $(this);
        var userStatus = btn.data("user");
        if ( userStatus ) {
            $.ajax({
                url: btn.data("url"),
                type: 'POST',
                data: { 
                    product_id: btn.data("index"), 
                    csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
                    action: 'add',
                },
                success: function (data) {
                    if ( data.liked ) {
                        $(".add-to-wishlist-text").text('Remove from wishlist');
                        $(".add-to-wishlist-icon").removeClass("icon anm anm-heart-l");
                        $(".add-to-wishlist-icon").addClass("fa fa-heart text-danger");
                    }
                    else {
                        $(".add-to-wishlist-text").text('Add to wishlist');
                        $(".add-to-wishlist-icon").removeClass("fa fa-heart text-danger");
                        $(".add-to-wishlist-icon").addClass("icon anm anm-heart-l");
                    }
                    $(".wishlist-count").text(data.wishlist_count);
                },
            })
        }
        else {
            loadForm( btn );
            $("#modal-login").on("submit", ".js-login-form", loginForm);
            $("#modal-login").on("submit", ".js-register-form", registerForm);
        }     
    });

    /* Reviews */

    const productIdVal = $("#add-to-cart-btn").val();
    const handleStarSelect = (size) => {
        childeren =  Array.from(document.querySelectorAll('#product-review-rate input')).reverse()
        childeren[size - 1].checked = true;
    }
    
    const loadRateValue = function () {
        $.ajax({
            url: $("#partial-user-review").attr('data-url'),
            type: 'GET',
            data: { product_id: productIdVal },
            success: function (response) {
                handleStarSelect(response.rate)
            },
        })
    }

    var loadReviewForm = function ( btn ) {
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            data: { review_id: btn.data('index') },
            dataType: 'json',
            success: function (data) {
                $("#partial-user-review").html(data.html_form);
                loadRateValue()
            }
        });
    };
    
    var saveForm = function (actionType, form, productId, rateVal) {
        $.ajax({
            url: form.attr("action"),
            data: form.serialize() + "&action="+ actionType + "&product_id="+ productId + "&rate="+ rateVal,
            type: form.attr("method"),
            dataType: 'json',
            success: function (data) {
                if ( data.form_is_valid ) {
                    $("#reviews-list").html(data.html_reviews_list);
                    $("#partial-product-avg-rate").html(data.html_reviews_avg_rate);
                    $("#modal-login").modal("hide");
                    $('.review-success-message').text(data.success_message).show()
                    // messages timeout for 5 sec
                    setTimeout(function () { $('.review-success-message').fadeOut('slow'); }, 5000);
                }
            }
        });
        return false;
    };

    // add review
    $(document).on("submit", ".js-add-review-form", function (e) {
        e.preventDefault();
        rateVal = $("input[name=rate]:checked").val()
        saveForm("add", $(this), productIdVal, rateVal);
    })

    // update review
    $(document).on("click", "#update-review", function (e) {
        e.preventDefault();
        loadReviewForm($(this));
    })

    $(document).on("submit", ".js-update-review-form", function (e) {
        e.preventDefault();
        rateVal = $("input[name=rate]:checked").val()
        saveForm("update", $(this), productIdVal, rateVal);
    })

    // delete review
    $(document).on("click", "#delete-review", function (e) {
        e.preventDefault();
        loadForm($(this));
    })

    $(document).on("submit", ".js-delete-review-form", function (e) {
        e.preventDefault();
        saveForm("delete", $(this), productIdVal, 5);
    })
    
});

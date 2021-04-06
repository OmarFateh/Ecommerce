// Open account Tabs
const openTab = (evt, tabName) => {
    // Declare all variables
    var i, tabcontent, tablinks;
  
    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }
  
    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
  
    // Show the current tab, and add an "active" class to the button that opened the tab
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
}

$(document).ready(function () {
    // Remove from cart 
    $(document).on("click", '.delete-from-cart-btn', function (e) { 
        var variationId = $(this).data("index");
        $.ajax({
            url: $(this).data("url"),
            type: 'POST',
            data: { 
                variation_id: variationId, 
                csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
                action: 'delete',
            },
            success: function (data) {
                $('#minicart-drawer').html(data.html_mini_cart_data);
                $('#partial-cart').html(data.html_cart_data);  
                $(".cart-qty-count").text(data.cart_qty);
            },
        }) 
    })

    // Redirect to wishlist tab
    $(document).on("click", '.wishlist-link', function (e) { 
        document.getElementById(tabName).style.display = "block";
    })

});    
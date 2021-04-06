$(document).ready(function () {
    
    const getCartQty = function (cartQty){
        if (cartQty == 1 ) {
            $('.cart-qty-count-items').text('Item');
        }
        else {
            $('.cart-qty-count-items').text('Items');
        }
    }

    // Update cart 
    $(document).on("click", '.update-cart-btn', function (e) {
        var variationId = $(this).data("index");
        var variationQty = $(`#qty${variationId}`).val();
        $.ajax({
            url: $(this).data("url"),
            type: 'POST',
            data: { 
                variation_id: variationId,
                product_qty: variationQty,
                csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
                action: 'update',
            },
            success: function (data) {
                getCartQty(data.cart_qty);
                $(".cart-qty-count").text(data.cart_qty);
                $(`#mini-qty${variationId}`).val(variationQty);
                $(".cart-total-price").text(data.cart_total_price.toFixed(2));
                document.getElementById(`item-total-price${variationId}`).innerHTML = data.item_total_price.toFixed(2);
            },
        }) 
    })
});
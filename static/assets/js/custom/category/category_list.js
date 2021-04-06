$(document).ready(function () {
    
    // category slide toggle 
    var btn = $(".sidebar_categories .sub-level .category")
    btn.toggleClass('active');
    btn.next(".sublinks").slideToggle("slow");
    
    // price range slider
    var maxPrice = document.getElementById('slider-range').getAttribute('max-price');
    var minPrice = document.getElementById('slider-range').getAttribute('min-price');

    function price_slider(){
        $("#slider-range").slider({
            range: true,
            min: parseInt(minPrice),
            max: parseInt(maxPrice), 
            values: [parseInt(minPrice), parseInt(maxPrice)],
            slide: function(event, ui) {
                $("#amount").val("$" + ui.values[0] + " - $" + ui.values[1]);
            }
        });
        $("#amount").val("$" + $("#slider-range").slider("values", 0) +
        " - $" + $("#slider-range").slider("values", 1));
    }
    price_slider();
    
    // ajax products filter size & color 
    $(document).on("click", ".products-size , .products-color, #price-filter-btn, #price-filter-clear-btn, ul.pagination li button", function () {
        var btn = $(this);
        var sizeId = '';
        var colorId = '';
        var sizeIdsArray = [];
        var colorIdsArray = [];
        var pageUrl = '';
        var urlCurrent = '';
        var priceRange = ''; 
        var pageNumber = '';
        var url = document.getElementById('root-category').getAttribute('data-url');

        if (btn.hasClass("price-filter-btn")) {
            priceRange = $("#amount").val().split(' ').join('');
            pageUrl = addPriceParam('price');
        }
        else if (btn.hasClass("price-filter-clear-btn")) {
            pageUrl = removeParam('price');
        }
        else if (btn.hasClass("paginator")) {
            pageNumber = btn.attr('data-href');
            pageUrl = addPageParam('page');
        }
        else {
            btn.toggleClass("checked");
        }
        
        if (btn.hasClass("checked")) {
            if ( btn.hasClass("products-size")) {
                sizeId = btn.attr('value');
                pageUrl = addParam(`size=${sizeId}`);
            }
            else if (btn.hasClass("products-color")) {
                colorId = btn.attr('value');
                pageUrl = addParam(`color=${colorId}`);
            } 
        }
        else {
            if ( btn.hasClass("products-size")) {
                sizeId = btn.attr('value');
                pageUrl = removeParam(`size=${sizeId}`);
            }
            else if (btn.hasClass("products-color")) {
                colorId = btn.attr('value');
                pageUrl = removeParam(`color=${colorId}`);
            } 
        }
        window.history.replaceState('', '', pageUrl)
        
        // add page parameter to url
        function addPageParam(parameter) {
            urlCurrent = window.location.href;
            var urlParts = urlCurrent.split('?');
            var urlBase = urlParts[0];
            if (urlParts.length>=2) {
                var params = removePageParam(urlParts[1].split('&'))
                if ( parameter === "page" ) {
                    if (params.length >= 1) {
                        queryString = "?" + parameter + "=" + pageNumber + "&" + params.join("&")
                    }
                    else {
                        console.log("yesssss")
                        queryString = "?" + parameter + "=" + pageNumber
                    }
                }
            }
            else{
                queryString = "?" + parameter + "=" + pageNumber
            }
            urlNew = urlBase + queryString
            return urlNew
        }

        // remove page parameter from url 
        function removePageParam(params) {
            var i;
            for( var i = 0; i < params.length; i++){ 
                if ( params[i].split('=')[0] === "page" || params[i] === "") { 
                    params.splice(i, 1); 
                    i = -1;
                }
            }
            return params
        }

        // add price parameter to url
        function addPriceParam(parameter) {
            urlCurrent = window.location.href;
            var urlNew = "";
            var urlParts = urlCurrent.split('?');
            if (urlParts.length>=2) {
                var params = removePageParam(urlParts[1].split('&'))
                var paramsSplit = params.join('=').split('=');
                if (!paramsSplit.includes(parameter)){
                    if ( params.length >=1 ) {
                        queryString = "?" + params.join("&") + "&" + parameter + "=" + priceRange;
                    }
                    else {
                        queryString = "?" + parameter + "=" + priceRange;
                    }
                }
                else{
                    for( var i = 0; i < params.length; i++){ 
                        if ( params[i].split('=')[0] === parameter) { 
                            params[i] = parameter + "=" + priceRange
                        }
                    }
                    urlNew = "?" + params.join("&")
                    return urlNew
                }
            }
            else {
                queryString = "?" + parameter + "=" + priceRange
            }
            urlNew = urlParts[0] + queryString
            return urlNew
        }

        // add parameter to url
        function addParam(parameter) {
            urlCurrent = window.location.href;
            var urlParts = urlCurrent.split('?');
            if (urlParts.length>=2) {
                var params = removePageParam(urlParts[1].split('&'));
                if (!params.includes(parameter)){
                    if ( params.length >=1 ) {
                        queryString = "?" + params.join("&") + "&" + parameter;
                    }
                    else {
                        queryString = "?" + parameter; 
                    }
                }
                else{
                    queryString = "?" + params.join("&"); 
                }
            }
            else {
                queryString = "?" + parameter
            }
            urlNew = urlParts[0] + queryString
            return urlNew
        }

        // remove parameter from url
        function removeParam(parameter) {
            urlCurrent = window.location.href;
            var urlParts = urlCurrent.split('?');
            var urlBase = urlParts[0];
            var params = removePageParam(urlParts[1].split('&'));
            if ( parameter === "price" ) {
                for( var i = 0; i < params.length; i++){ 
                    if ( params[i].split('=')[0] === parameter) { 
                        params.splice(i, 1); 
                    }
                }
            }
            else {
                for( var i = 0; i < params.length; i++){ 
                    if ( params[i] === parameter) { 
                        params.splice(i, 1); 
                    }
                }
            }
            if (params.length >1) {
                urlNew = urlBase + '?' + params.join('&');
            }
            else if (params.length == 1) {
                urlNew = urlBase + '?' + params;
            }
            else {
                urlNew = urlBase;
            }
            return urlNew
        }

        // add parameter's values to the parameter's array
        function getArrayIds(parameter) {
            urlCurrent = window.location.href;
            var urlParts = urlCurrent.split('?'); //http://127.0.0.1:8000/Men/Clothing/?size=5&size=4
            if (urlParts.length>=2) {
                var params = urlParts[1].split('&').join('=').split('=');  // size=5&size = 4 ---> [size=5, size=4] ---> [size, 5, size, 4]
                for( var i = 0; i < params.length-1; i++){ 
                    if ( params[i] === parameter && parameter === "size") { 
                        sizeIdsArray.push(Number(params[i+1]));                
                    }
                    else if ( params[i] === parameter && parameter === "color") { 
                        colorIdsArray.push(Number(params[i+1]));
                    }
                }
            }
        }
        getArrayIds("size")
        getArrayIds("color")

        $.ajax({
            url: url,
            type: 'GET',
            data: { size: sizeIdsArray, color: colorIdsArray, price: priceRange, page: pageNumber },
            success: function (data) {
                $("#partial-product-list").html(data.html_product_list);
                $("#partial-product-paginator").html(data.html_product_pagination);
            }
        });
    });

})
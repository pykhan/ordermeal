var dateFormat = "YYYY-MM-DD";

/* http://www.daterangepicker.com/ */
$('input[id="itemDate"]').daterangepicker({
    singleDatePicker: true,
    showDropdowns: true,
    minDate: moment().add(3, 'days').format(dateFormat),
    maxDate: moment().add(21, 'days').format(dateFormat),
    locale: {
        format: dateFormat
    }
});

var addToCart = function(productId, clickedButtonId){
    $.ajax({
        url: "/add-to-cart/" + $("#child").val() + "/" + productId + "/" + $("#itemDate").val(),
        method: "GET"
    }).done(function(response){
        response.payloads.forEach(function(data){
            $("#"+clickedButtonId).notify(data.message, "success");
        });
    }).error(function(response){
        response.payloads.forEach(function(data){
            $("#"+clickedButtonId).notify(data.message, "error");
        });
    });
};


var confirmPayment = function(){
    $.ajax({
        url: "/confirm-payment/" + $("#id_checkNo").val(),
        method: "GET"
    }).done(function(response){
        var notice = "";
        var cfm = "<div>Your confirmation #: <h2>";
        response.payloads.forEach(function(data){
            $("#id_checkNo").hide();
            $("#id_paymentConfirmationButton").hide();
            $("#id_note").html(cfm + data.confirmation_no + "</h2></div>");
            $.notify(data.message, "success");
        });
    }).error(function(response){
        console.log(response);
    });
};


var showDescription = function(pid){
    $.ajax({
        url: "/product-description/" + pid,
        method: "GET"
    }).done(function(response){
        response.payloads.forEach(function(data){
            if(data.message.trim() != "")
                $("#div_"+pid).notify(data.message, "info");
            else
                $("#div_"+pid).notify("Product info is missing.\nEmail admin to add info.", "warn");
        });
    }).error(function(response){
        console.log(response);
    });
};
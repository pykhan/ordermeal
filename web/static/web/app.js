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
        response.payloads.forEach(function(data){
            $.notify(data.message, "success");
            $("#id_checkNo").hide();
            $("#id_paymentConfirmationButton").hide();
            $("#id_note").innerHtml = "Order Confirmation #<br>" + data.confirmation_no;
        });
    }).error(function(response){
        console.log(response);
    });
};
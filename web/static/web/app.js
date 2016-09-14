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
        url: "/web/api/add-to-cart/" + productId + "/" + $("#itemDate").val(),
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
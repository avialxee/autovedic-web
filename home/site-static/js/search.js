
$(document).ready(function() {
    $('#model_brand').autocomplete({
        source: function(request, response){
        var results = $.ui.autocomplete.filter(availablemodels, request.term);
        response(results.slice(0, 5));
        }
        
    })
});


$(document).ready(function(){
    

  
    var xhr = $.ajax({
                url: '/api/dtext/chooseus/0',
                method: 'GET',
                statusCode: {
                    200: function (response) {
                        
                        // console.log(response["Text"])
                        // data = JSON.parse(response["Text"])
                        
                        
                        $(function () {
                            count = 0;
                            // text = ;
                            wordsArray= Object.values(response["Text"]);
                            // console.log(Object.values(text))
                            setInterval(function () {
                            count++;
                            $("#choose-us-text").fadeOut(400, function () {
                                $(this).text(wordsArray[count % wordsArray.length]).fadeIn(400);
                            });
                            }, 4000);
                        });
                    }
                }
            })
});
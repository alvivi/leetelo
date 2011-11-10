

$('.close').live('click', function() {
    $(this).parent().slideUp();
});



$(document).ready(function() {
        $(".sortable").tablesorter();
        
        if(window.location.pathname == "/profile/copyoffers") {
            var buttons = $("#exchange-buttons");
            $("#offersTable input[type=radio]").live('click', function () {
                var rows = $(".offer-state-column");
                var flag = false;
                for (var i = 0; i < rows.length; i++) {
                    if ($(rows[i]).text() == "Negociando") {
                        flag = true;
                    }
                }
            
                if(flag)
                    $(buttons).children().last().removeClass("disabled");
                else
                    $(buttons).children().removeClass("disabled");
            });       
        }
        
        if(window.location.pathname == "/profile/appliantcopies") {
            var user = (RegExp("appliant=(.*)").exec(window.location.href.slice(window.location.href.indexOf('?') + 1).split('&')[1]))[1];
            var rows = $(".appliant-column-name");
            
            for (var i = 0; i < rows.length; i++) {
                if ($(rows[i]).text() == user) {
                    $(rows[i]).parent().children().first().children().first().attr("checked", "");
                }
            }
            $("#exchange-buttons").children().removeClass("disabled");
            
            var buttons = $("#exchange-buttons2");
            $("#appliantCopiesTable input[type=radio]").live('click', function () {
                $(buttons).children().removeClass("disabled");
            });  
        }
        if(window.location.pathname == "/profile/applications") {
            var button = $ ("#confirmRequestResponse");
            $("#requestsTable input[type=radio]").live('click', function () {
                $(button).children().removeClass("disabled");
            });  

        }
});


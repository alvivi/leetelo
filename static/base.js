

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
            
            var appliants = $(".appliant-column-name");
            var inputs = $("#offersTable input[type=radio]");
            
            for (var i = 0; i <appliants.length; i++) {
                if ($(appliants[i]).text() == user) {
                    $(inputs[i]).attr("checked", "");
                }
            }
            $("#exchange-buttons").children().removeClass("disabled");
            
            var buttons = $("#exchange-buttons2");
            $("#appliantCopiesTable input[type=radio]").live('click', function () {
                $(buttons).children().removeClass("disabled");
            });  
        }
        
        if(window.location.pathname == "/profile/applicationcontent") {
            var owner = (RegExp("owner=(.*)").exec(window.location.href.slice(window.location.href.indexOf('?') + 1).split('&')[1]))[1];
            var copy = (RegExp("selectedCopyTitle=(.*)").exec(window.location.href.slice(window.location.href.indexOf('?') + 1).split('&')[0]))[1];
            var owners = $(".request-owner-column");
            var copies = $(".request-copy-column");
            var inputs = $("#requestsTable input[type=radio]");
            
            for (var i = 0; i < owners.length; i++) {
                if ( $(owners[i]).text() == owner && $(copies[i]).text() == copy) {
                    $(inputs[i]).attr("checked", "");
                }
            }
        }
        
       

});




/* Objeto que contiene las acciones a ejecutar en cada vista, de forma local. */
var localScripts = {

    "/profile/appliantcopies" : function () {
        var user = (RegExp("appliant=(.*)").exec(window.location.href.slice(
            window.location.href.indexOf('?') + 1).split('&')[1]))[1];
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
    },

    "/profile/copies" : function () {
        var button = $('#remove-copies-button');
        var alertbox = $('#modal-remove');
        var count = 0;

        alertbox.modal({backdrop: true, modal: true});

        button.live('click', function (e) {
            e.preventDefault();
            if (!$(this).hasClass('disabled')) {
                alertbox.modal('show');
            }
        });

        $("input[type=checkbox]").live('click', function (e) {
            console.log(count);
            if ($(this).attr('checked')) {
                button.removeClass('disabled');
                count++;
            }
            else {
                count--;
                if (count <= 0) {
                    button.addClass('disabled');
                }
            }
        });

        $('#modal-remove .primary').live('click', function (e) {
            var keys = '';
            $('input[type=checkbox]').each(function (i, c) {
                if ($(c).attr('checked')) {
                    keys = (keys == '') ? keys : keys + ',';
                    keys += $(c).parent().parent().find('span').text();
                }
            });
            $.ajax({
                url  : '/profile/copies/delete',
                data : {selected : keys},
                type : 'POST',
                success : function (data) {
                    var table = $('table');
                    table.fadeOut(function () {table.remove();});
                    table.before($(data).find('table')).hide().fadeIn();
                    $('#modal-remove').modal('hide');
                    button.addClass('disabled');
                }
            });
        });
    },

    "/profile/applicationcontent" : function () {
        var owner = (RegExp("owner=(.*)").exec(window.location.href.slice(window.location.href.indexOf('?') + 1).split('&')[1]))[1];
        var copy = decodeURI((RegExp("selectedCopyTitle=(.*)").exec(window.location.href.slice(window.location.href.indexOf('?') + 1).split('&')[0]))[1]);         
        var owners = $(".request-owner-column");
        var copies = $(".request-copy-column");
        var inputs = $("#requestsTable input[type=radio]");

        for (var i = 0; i < owners.length; i++) {
            if ( $(owners[i]).text() == owner && $(copies[i]).text() == copy) {
                $(inputs[i]).attr("checked", "");
            }
        }
    },

    "/profile/copyoffers" : function () {
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
};


$(document).ready(function() {
    $(".sortable").tablesorter();
    $(".alert-message").alert();

    for (var path in localScripts) {
        if(window.location.pathname == path)
            localScripts[path]();
    };
});

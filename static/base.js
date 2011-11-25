

var JSTipoOferta = function() {
    var opc_sel=$('#TipoOferta').attr('value');
     $("#idprecio").toggle(opc_sel == 'Venta');
     $("#idfecha").toggle(opc_sel != 'Ninguna');
}

/* Objeto que contiene las acciones a ejecutar en cada vista, de forma local. */
var localScripts = {

    "/book/new" : function () {
        if(/.*error=true.*/.test(location.href)) {
            $("#error-message").show();
        }
        if(/.*errorrepeat=true.*/.test(location.href)) {
            $('#title').parent().parent().addClass('error');
            $('#title').twipsy({trigger: 'manual'});
            $('#title').twipsy('show')
        }
    },

    "/book/details" : function () {
        var modalError = $('#modal-error');
        modalError.modal({backdrop: true, modal: true});

        $('#modal-error .close').live('click', function() {
            modalError.modal('hide');
        });
        $('#modal-error .btn').live('click', function() {
            modalError.modal('hide');
        });

        $('table .btn').live('click', function() {
            $.ajax({
                    url  : '/profile/applications/new',
                    data : {copy : $(this).parent().find('span').text()},
                    type : 'POST',
                    success : function (data) {
                        if (data == 'OK') {
                            location.href = '/profile/applications';
                        }
                        else {
                            modalError.find('p').text(data);
                            modalError.modal('show');
                        }
                    }
                });
        });
    },

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
        var offset = 0; var doing = false; var doing = false;
        $(window).scroll(function () {
            if ($('.loading').offset().top <= $(window).height() + window.pageYOffset && !doing) {
                doing = true;
                offset += 10;
                $.ajax({
                    url  : '/profile/copies',
                    data : {offset : offset},
                    type : 'GET',
                    success : function (data) {
                        var rows = $(data).find('tbody').children();
                        var count = rows.length;
                        if (count > 0) {
                            rows.addClass('new-rows');
                            $('tbody').append(rows);
                            $('.new-rows').hide().fadeIn(function () {
                                $('.new-rows').removeClass('new-rows');
                                doing = false;
                            });
                        }
                        else {
                            $('.loading').fadeOut();
                        }
                    }
                });
            }
        });

        var button = $('#remove-copies-button');
        var alertbox = $('#modal-remove');
        var count = 0;

         $('#modal-remove').modal({backdrop: true, modal: true});

        button.live('click', function (e) {
            e.preventDefault();
            if (!$(this).hasClass('disabled')) {
                alertbox.modal('show');
            }
        });

        $("input[type=checkbox]").live('click', function (e) {
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

        $('#modal-remove .close').live('click', function (e) {
            $('#modal-remove').modal('hide');
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

    "/profile/newclub" : function () {
        $('#nuevo-invitado').live('click', function (e) {
            e.preventDefault();
            var nuevo = $($('.invitados')[0]).clone();
            var nombre = $('#invitacion').val();
            nuevo.find('span').text(nombre);
            $('.invitados').after(nuevo);
            nuevo.fadeIn('slow');
            $('#invitaciones').val(($('#invitaciones').val() == "") ? $('#invitaciones').val() + nombre : $('#invitaciones').val() + ',' + nombre);
        });

        $('#optiones_genero').live('click', function (e) {
            var keys = '';
            $('input[type=checkbox]').each(function (i, c) {
                if ($(c).attr('checked')) {
                    keys = (keys == '') ? keys : keys + ',';
                    //keys += $(c).parent().parent().find('span').text();
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

        buttons.live('click', function(e) {
            if ($(this).children().hasClass('disabled')){
                e.preventDefault();
                e.stopPropagation();
            }
        });
    },

    "/profile/newcopy" : function () {
        $("#fechaLimite").datepicker();

        var getParameter = function (parameter) {
            // Obtiene la cadena completa de URL
            var url = location.href;
            /* Obtiene la posicion donde se encuentra el signo ?,
               ahi es donde empiezan los parametros */
            var index = url.indexOf("?");
            /* Obtiene la posicion donde termina el nombre del parametro
               e inicia el signo = */
            index = url.indexOf(parameter,index) + parameter.length;
            /* Verifica que efectivamente el valor en la posicion actual
               es el signo = */
            if (url.charAt(index) == "=") {
                // Obtiene el valor del parametro
                var result = url.indexOf("&",index);
                if (result == -1){result=url.length;};
                // Despliega el valor del parametro
                return (url.substring(index + 1,result));
            }
            return "";
        }

        var ShowSelected = function ()
        {
            var combo = document.getElementById("titleBook");
            var selected = combo.options[combo.selectedIndex].text;
            window.location="/profile/newcopy?selectedCopyTitle=" + selected;
        }

        $('#titleBook').live('change', ShowSelected);
        $('#TipoOferta').live('change', JSTipoOferta);

        /*Ocultar/Mostra los campos segun valores de select*/
        JSTipoOferta();
    },

    "/profile/editcopy" : function () {
        $('#TipoOferta').live('change', JSTipoOferta);
        var opc_sel=$('#TipoOferta').attr('value');
        $("#idprecio").toggle(opc_sel == 'Venta');
        $("#idfecha").toggle(opc_sel != 'Ninguna');
        $("#fechaLimite").datepicker();
    }
}

jQuery(function($){
    $.datepicker.regional['es'] = {
        closeText: 'Cerrar',
        prevText: '&#x3c;Ant',
        nextText: 'Sig&#x3e;',
        minDate: 0,
        currentText: 'Hoy',
        monthNames: ['Enero','Febrero','Marzo','Abril','Mayo','Junio',
        'Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre'],
        monthNamesShort: ['Ene','Feb','Mar','Abr','May','Jun',
        'Jul','Ago','Sep','Oct','Nov','Dic'],
        dayNames: ['Domingo','Lunes','Martes','Mi&eacute;rcoles','Jueves','Viernes','S&aacute;bado'],
        dayNamesShort: ['Dom','Lun','Mar','Mi&eacute;','Juv','Vie','S&aacute;b'],
        dayNamesMin: ['Do','Lu','Ma','Mi','Ju','Vi','S&aacute;'],
        weekHeader: 'Sm',
        dateFormat: 'dd/mm/yy',
        firstDay: 1,
        isRTL: false,
        showMonthAfterYear: false,
        yearSuffix: ''};
    $.datepicker.setDefaults($.datepicker.regional['es']);
});

$(document).ready(function() {
    $(".sortable").tablesorter();
    $(".alert-message").alert();

    for (var path in localScripts) {
        if(window.location.pathname == path)
            localScripts[path]();
    };
});

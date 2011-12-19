

var JSTipoOferta = function() {
    var opc_sel=$('#TipoOferta').attr('value');
     $("#idprecio").toggle(opc_sel == 'Venta');
     $("#idfecha").toggle(opc_sel != 'Ninguna');
}

function pagination(url, size) {
    function loadingPosition() { return $('.loading').offset().top; }
    function pagePosition() { return $(window).height() + window.pageYOffset; }

    var offset = 0; var doing = false; var doing = false;

    if (loadingPosition() < pagePosition()) {
        $('.loading').hide();
    }
    else {
        $(window).scroll(function () {
            if (loadingPosition() <= pagePosition() && !doing) {
                doing = true;
                offset += size;
                setTimeout( function () {
                    $.ajax({
                        url  : url,
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
                }, 1000);
            }
        });
    }
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


    "/club" : function () {
        var modalError = $('#modal-club-error');
        var selectedClub;
        modalError.modal({backdrop: true, modal: true});

        $('#modal-club-error .close').live('click', function() {
            modalError.modal('hide');
        });
        $('#modal-club-error .btn').live('click', function() {
            modalError.modal('hide');
        });

        $('table .btn').live('click', function() {
            selectedClub = $(this).parent().find('span').text();
            $.ajax({
                    url  : '/club/requestparticipation',
                    data : {selected : selectedClub},
                    type : 'POST',
                    success : function (data) {
                        if (data == 'OK') {
                            location.href = '/profile/club/disabledcontent?selectedClub=' + selectedClub;
                        }
                        else {
                            modalError.find('p').text(data);
                            modalError.modal('show');
                        }
                    }
                });
        });
    },

    "/profile/copies" : function () {
        pagination('/profile/copies', 10);

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
            debugger;
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

    "/profile/club" : function () {
        pagination('/profile/club',10);
        var disable_modal = $('#modal-disable-club');
        var enable_modal = $('#modal-enable-club');
        var participation_modal = $('#modal-cancel-participation');
        var selected_club = null;
        var count = 0;

        disable_modal.modal({backdrop: true, modal: true});
        enable_modal.modal({backdrop: true, modal: true});
        participation_modal.modal({backdrop: true, modal: true});
        $('#accept-invitation-link').live('click',function(e) {
            selected_club = $(this).children().text();
            $.ajax({
                url  : '/profile/club/answerinvitation',
                data : {selected : selected_club, option : 'Aceptar'},
                type : 'POST',
                success : function (data) {
                    var table = $('table');
                    table.fadeOut(function () {table.remove();});
                    table.before($(data).find('table')).hide().fadeIn();
                }
            });

        });

        $('#reject-invitation-link').live('click',function(e) {
            selected_club = $(this).children().text();
            $.ajax({
                url  : '/profile/club/answerinvitation',
                data : {selected : selected_club, option : 'Rechazar'},
                type : 'POST',
                success : function (data) {
                    var table = $('table');
                    table.fadeOut(function () {table.remove();});
                    table.before($(data).find('table')).hide().fadeIn();
                }
            });

        });

        $('#disable-club-link').live('click', function (e) {
            e.preventDefault();
            selected_club = $(this).children().text();
            disable_modal.modal('show');
        });
        $('#enable-club-link').live('click', function (e) {
            e.preventDefault();
            selected_club = $(this).children().text();
            enable_modal.modal('show');
        });
        $('#cancel-participation-link').live('click', function (e) {
            e.preventDefault();
            selected_club = $(this).children().text();
            participation_modal.modal('show');
        });
        $('#delete-participation-link').live('click', function (e) {
            e.preventDefault();
            selected_club = $(this).children().text();
            $.ajax({
                url  : '/profile/club/deleteparticipation',
                data : {selected : selected_club},
                type : 'POST',
                success : function (data) {
                    var table = $('table');
                    table.fadeOut(function () {table.remove();});
                    table.before($(data).find('table')).hide().fadeIn();
                }
            });
        });

        $('#modal-disable-club .close').live('click', function (e) {
            disable_modal.modal('hide');
        });
        $('#modal-enable-club .close').live('click', function (e) {
            enable_modal.modal('hide');
        });
        $('#modal-cancel-participation .close').live('click', function (e) {
            participation_modal.modal('hide');
        });

        $('#modal-disable-club .primary').live('click', function (e) {
            $.ajax({
                url  : '/profile/club/disable',
                data : {selected : selected_club},
                type : 'POST',
                success : function (data) {
                    var table = $('table');
                    table.fadeOut(function () {table.remove();});
                    table.before($(data).find('table')).hide().fadeIn();
                    disable_modal.modal('hide');
                }
            });
        });
        $('#modal-enable-club .primary').live('click', function (e) {
            $.ajax({
                url  : '/profile/club/disable',
                data : {selected : selected_club},
                type : 'POST',
                success : function (data) {
                    var table = $('table');
                    table.fadeOut(function () {table.remove();});
                    table.before($(data).find('table')).hide().fadeIn();
                    enable_modal.modal('hide');
                }
            });
        });
        $('#modal-cancel-participation .primary').live('click', function (e) {
            $.ajax({
                url  : '/profile/club/deleteparticipation',
                data : {selected : selected_club},
                type : 'POST',
                success : function (data) {
                    var table = $('table');
                    table.fadeOut(function () {table.remove();});
                    table.before($(data).find('table')).hide().fadeIn();
                    participation_modal.modal('hide');
                }
            });
        });
    },


    "/profile/club/edit" : function () {

         $('#nuevo-invitado').live('click', function (e) {
            e.preventDefault();
            var repetido=0;
            var nuevo = $($('.invitados')[0]).clone();
            var nombre = $('#invitacion').val();

            /*
             * Miramos si el email ya existe en los ya invitados
             */
            $("#invitados option").each(function(){
            	var email = $(this).text();
            	if($.trim(email) == nombre )
            		repetido=1;
            });


            /*
             * Miramos si el email ya existe en los nuevos
             */
            $('.invitados span').each(function(){
            	if((this).innerHTML==nombre)
            		repetido=1;
            });

            /*Si no existe lo a?adimos*/
            if(!repetido)
            {
	            nuevo.find('span').text(nombre);
	            $('.invitados').after(nuevo);
	            nuevo.fadeIn('slow');
	            $('#invitaciones').val(($('#invitaciones').val() == "") ? $('#invitaciones').val() + nombre : $('#invitaciones').val() + ',' + nombre);
            }
        });

        /*$('#optionsGener').live('click', function (e){
         var arr = $("input:checked").getCheckboxValues();
           $('#selectedGener').val(arr);

       });*/
        $('#optionsGeners').live('click', function (e){
           $("#resultado").val($('#optionsGeners').val());
        });


    },



    "/profile/club/content" : function () {
        var selected_club = null;
        var count = 0;

        $('#newcomment').live('click', function(e) {
            e.preventDefault();
            $(this).slideToggle();
            $('#commentform').slideToggle();
        });

        $('#accept-request-link').live('click',function(e) {
            participation = $(this).children().text();
            $.ajax({
                url  : '/profile/club/answerrequest',
                data : {selected : participation, option : 'Aceptar'},
                type : 'POST',
                success : function (data) {
                    var table = $('table');
                    table.fadeOut(function () {table.remove();});
                    table.before($(data).find('table')).hide().fadeIn();
                }
            });

        });
        $('#reject-request-link').live('click',function(e) {
            participation = $(this).children().text();
            $.ajax({
                url  : '/profile/club/answerrequest',
                data : {selected : participation, option : 'Rechazar'},
                type : 'POST',
                success : function (data) {
                    var table = $('table');
                    table.fadeOut(function () {table.remove();});
                    table.before($(data).find('table')).hide().fadeIn();
                }
            });

        });
    },






    "/profile/club/new" : function () {

        var invs = [];

        if(/.*errorrepeat=true.*/.test(location.href)) {

            $('#nombreClub').twipsy({trigger: 'manual'});
            $('#nombreClub').twipsy('show')
        }

        $('.eliminar-invitado').live('click', function (e) {
            e.preventDefault();
            var self = this;
            $(self).parent().fadeOut(function (e) {
                $(self).parent().remove();
            });
            var i = invs.indexOf($(this).parent().find('span').text());
            invs.splice(i, 1);
            $('#invitaciones').val(invs.join(','));
        });

        $('#nuevo-invitado').live('click', function (e) {
            e.preventDefault();
            var nombre = $('#invitacion').val();

            if (nombre === "") {
                $('#invitacion').twipsy({fallback : 'Introduce un nombre válido', trigger: 'manual', placement: 'right'});
                $('#invitacion').twipsy('show');
                return;
            } else {
                $('#invitacion').twipsy('hide');
            }
            var repetido=0;
            var nuevo = $($('.invitados')[0]).clone();


            /*Si no existe lo a?adimos*/
            if(invs.indexOf(nombre) < 0) {
	            nuevo.find('span').text(nombre);
                nuevo.find('img').attr('src', nuevo.find('img').attr('src') + nombre);
	            $('.invitados').after(nuevo);
	            nuevo.fadeIn('slow');
                invs.push(nombre);
                $('#invitaciones').val(invs.join(','));
	            //$('#invitaciones').val(($('#invitaciones').val() == "") ? $('#invitaciones').val() + nombre : $('#invitaciones').val() + ',' + nombre);
            } else {
                $('#invitacion').twipsy({fallback : 'Este usuario ya está invitado', trigger: 'manual', placement: 'right'});
                $('#invitacion').twipsy('show');
            }
        });

        /*$('#optionsGener').live('click', function (e){
         var arr = $("input:checked").getCheckboxValues();
           $('#selectedGener').val(arr);

       });*/

         $('#optionsGeners').live('click', function (e){
           $("#resultado").val($('#optionsGeners').val());
             });

    },

    "/profile/applicationcontent" : function () {
        var owner = $('#owner').val();
        var copy = $('#selectedCopyTitle').val();
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
        var acceptButton = $("#accept-offer-button");
        var rejectButton = $("#reject-offer-button");
        var selectedCopyKey = $("#selected-copy-key").text();
        var directExchangeButton = $("#direct-exchange-button");
        var actionText;
        
        $("#appliantCopiesTable input[type=radio]").live('click', function () {
            var rows = $(".offer-state-column");
            var flag = false;
            for (var i = 0; i < rows.length; i++) {
                if ($(rows[i]).text() == "Negociando") {
                    flag = true;
                }
            }
            if(flag)
            {
                if($("#offersTable input[type=radio]:checked").parent().parent().children(".offer-state-column").text() == "Negociando")
                    $(directExchangeButton).removeClass("disabled");
            }
            else
                $(directExchangeButton).removeClass("disabled");
        });
        
        $("#offersTable input[type=radio]").live('click', function () {
            var rows = $(".offer-state-column");
            var flag = false;
            for (var i = 0; i < rows.length; i++) {
                if ($(rows[i]).text() == "Negociando") {
                    flag = true;
                }
            }
            
            $(directExchangeButton).addClass("disabled");
            
            if(flag)
                $(rejectButton).removeClass("disabled");
            else
            {
                $(acceptButton).removeClass("disabled");
                $(rejectButton).removeClass("disabled");
            }
            
            if($('#transaction-type').text()=="Intercambio")
            {
                $.ajax({
                    url  : '/profile/appliantcopies',
                    data : {requestKey : $('input[name="offersRadios"]:checked').val(), selectedCopy: selectedCopyKey},
                    type : 'GET',
                    success : function (data) {
                        $('#appliantCopies').remove();
                        var appliantCopies = $(data).find('#appliantCopies');
                        $("#exchange-buttons2").before(appliantCopies);
                        $("#exchange-buttons2").removeClass('hide');
                    }
                });
            }
        });
        
        acceptButton.live('click',function(e) {
            actionText=$(this).text();
            if ($(this).hasClass('disabled')){
                e.preventDefault();
                e.stopPropagation();
            }
            else{
                $.ajax({
                    url  : '/profile/copyoffers',
                    data : {action : actionText, requestKey : $('input[name="offersRadios"]:checked').val(), selectedCopy: selectedCopyKey},
                    type : 'POST',
                    success : function (data) {
                        var table = $('#offersTable');
                        table.fadeOut(function () {table.remove();});
                        table.before($(data).find('#offersTable')).hide().fadeIn();
                        $('#appliantCopies').remove();
                        $("#exchange-buttons2").addClass('hide');
                    }
                });
                $(acceptButton).addClass("disabled");
                $(rejectButton).addClass("disabled");
            }
        });
        rejectButton.live('click',function(e) {
            actionText=$(this).text()
            if ($(this).hasClass('disabled')){
                e.preventDefault();
                e.stopPropagation();
            }
            else{
                $.ajax({
                    url  : '/profile/copyoffers',
                    data : {action : actionText, requestKey : $('input[name="offersRadios"]:checked').val(), selectedCopy: selectedCopyKey},
                    type : 'POST',
                    success : function (data) {
                        var table = $('#offersTable');
                        table.fadeOut(function () {table.remove();});
                        table.before($(data).find('#offersTable')).hide().fadeIn();
                    }
                });
                $(acceptButton).addClass("disabled");
                $(rejectButton).addClass("disabled");
            }
        });
        directExchangeButton.live('click',function(e) {
            actionText=$(this).text()
            if ($(this).hasClass('disabled')){
                e.preventDefault();
                e.stopPropagation();
            }
            else{
                $.ajax({
                    url  : '/profile/copyoffers',
                    data : {action : actionText, requestKey : $('input[name="offersRadios"]:checked').val(), selectedCopy: selectedCopyKey, appliantSelectedCopy: $('input[name="appliantCopiesRadios"]:checked').val()},
                    type : 'POST',
                    success : function(data) {
                        var table = $('#offersTable');
                        table.fadeOut(function () {table.remove();});
                        table.before($(data).find('#offersTable')).hide().fadeIn();
                        $('#appliantCopies').remove();
                        $("#exchange-buttons2").addClass('hide');
                    }
                });
                $(acceptButton).addClass("disabled");
                $(rejectButton).addClass("disabled");
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

        var showSelected = function(event, ui)
        {
            var edit = $('#titleBook');
            edit.val(ui.item.value);
            window.location="/profile/newcopy?selectedCopyTitle=" + edit.val();
        }

        $('#TipoOferta').live('change', JSTipoOferta);
        var titleEdit = $('#titleBook');
        titleEdit.live('click', function() {titleEdit.focus(); titleEdit.select();});

        /*Ocultar/Mostra los campos segun valores de select*/
        JSTipoOferta();

        $.ajax({
            url: '/api/books/title',
            dataType: 'json',
            success: function(data) {
                titleEdit.autocomplete({
                    source: data,
                    minLength: 2
                });
            }
        });

        $( "#titleBook" ).live("autocompleteselect", showSelected);

    },

    "/profile/editcopy" : function () {
        $('#TipoOferta').live('change', JSTipoOferta);
        var opc_sel=$('#TipoOferta').attr('value');
        $("#idprecio").toggle(opc_sel == 'Venta');
        $("#idfecha").toggle(opc_sel != 'Ninguna');
        $("#fechaLimite").datepicker();
    }
}



jQuery.fn.getCheckboxValues = function(){
    var values = [];
    var i = 0;
    this.each(function(){
        // guarda los valores en un array
        values[i++] = $(this).val();
    });
    // devuelve un array con los checkboxes seleccionados
    return values;
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

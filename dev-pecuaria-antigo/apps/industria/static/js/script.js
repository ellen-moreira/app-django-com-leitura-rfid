$(document).ready(function () {
    $('#example').DataTable({
        language: {
            url: 'https://cdn.datatables.net/plug-ins/1.13.6/i18n/pt-BR.json',
            decimal: ',',
            thousands: '.'
        },
        order: [[0, 'asc']],
        stateSave: true,
    });

    setTimeout(function () {
        $("#message").alert('close');
    }, 3000);

    $('.inlineform').each(function() {
        var lastMb3 = $(this).find('.row .mb-3:last');
        lastMb3.hide();
    });

    $('.inlineform-procedimento').each(function() {
        var lastMb3 = $(this).find('.row .mb-3:last');
        lastMb3.hide();
    });

    $('.inlineform-produto').each(function () {
        var lastMb3 = $(this).find('.row .mb-3:last');
        lastMb3.hide();
    });
});
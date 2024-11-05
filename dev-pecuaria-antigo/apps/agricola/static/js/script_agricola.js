$(document).ready(function () {
    $('#lote-table').DataTable({
        language: {
            url: 'https://cdn.datatables.net/plug-ins/1.13.6/i18n/pt-BR.json',
            decimal: ',',
            thousands: '.'
        },
        order: [[0, 'desc']],
        columnDefs: [
            {orderable: false, targets: [1, 2]}
        ],
        columns: [
            {searchable: true},
            {searchable: true},
            {searchable: false}
        ]
    });

    $('#parto-table').DataTable({
        language: {
            url: 'https://cdn.datatables.net/plug-ins/1.13.6/i18n/pt-BR.json',
            decimal: ',',
            thousands: '.'
        },
        order: [[0, 'desc']],
        columnDefs: [
            {orderable: false, targets: [1, 2, 3, 4, 5, 6, 8, 9]}
        ],
        columns: [
            {searchable: true},
            {searchable: true},
            {searchable: true},
            {searchable: false},
            {searchable: false},
            {searchable: false},
            {searchable: false},
            {searchable: false},
            {searchable: false},
            {searchable: false}
        ]
    });

    $('#manejo-table').DataTable({
        language: {
            url: 'https://cdn.datatables.net/plug-ins/1.13.6/i18n/pt-BR.json',
            decimal: ',',
            thousands: '.'
        },
        order: [[0, 'desc']],
        columnDefs: [
            {orderable: false, targets: [2, 3, 4, 5, 6]}
        ],
        columns: [
            {searchable: true},
            {searchable: true},
            {searchable: true},
            {searchable: true},
            {searchable: false},
            {searchable: false},
            {searchable: false}
        ]
    });

    $('#animal-table').DataTable({
        language: {
            url: 'https://cdn.datatables.net/plug-ins/1.13.6/i18n/pt-BR.json',
            decimal: ',',
            thousands: '.'
        },
        order: [[7, 'desc']],
        columns: [
            {searchable: true},
            {searchable: true},
            {searchable: true},
            {searchable: true},
            {searchable: true},
            {searchable: false},
            {searchable: true},
            {searchable: true},
            {searchable: true},
            {searchable: true},
            {searchable: true}
        ]
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
$(document).ready(function() {
    // Close alert message after 3 seconds
    setTimeout(function () {
        $('#message').alert('close');
    }, 3000);

    // DataTables config
    $('#table-pecuaria').DataTable({
        language: {
            url: 'https://cdn.datatables.net/plug-ins/1.13.6/i18n/pt-BR.json',
            decimal: ',',
            thousands: '.'
        },
        responsive: true,
    });

    // Add event to delete button
    $('.btn-delete').click(function(){
        return confirm('Tem certeza que deseja excluir este registro?');
    });
});
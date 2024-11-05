$(document).ready(function(){
    // Fechamento automático de mensagens de alerta após 3 segundos
    setTimeout(function () {
        $('#message').alert('close');
    }, 3000);

    // Configuração do DataTable
    $('#table-pecuaria').DataTable({
        language: {
            url: 'https://cdn.datatables.net/plug-ins/1.13.6/i18n/pt-BR.json',
            decimal: ',',
            thousands: '.'
        },
        responsive: true,
    });

    // Adicionar evento de click no botão de excluir (abrir alert padrão do js para confirmar a exclusão). Só excluir se o usuário confirmar.
    $('.btn-delete').click(function(){
        return confirm('Tem certeza que deseja excluir este registro?');
    });

    // Adciionar interceptação no clique do link de navegação para verificar se o usuário tem permissão para acessar a página
    $('.nav-link').on('click', function(event) {
        event.preventDefault(); // Intercepta o clique no link

        var url = $(this).attr('href') + '?ajax=1';

        $.ajax({
            url: url,
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            },
            success: function(data) {
                if (data.permissao) {
                    window.location.href = url.replace('?ajax=1', ''); // Redireciona para a URL se tiver permissão
                } else {
                    alert(data.mensagem || "Você não tem permissão para acessar esta página.");
                }
            },
            error: function(xhr, status, error) {
                console.error('Erro:', error);
                alert("Ocorreu um erro ao verificar a permissão.");
            }
        });
    });
});
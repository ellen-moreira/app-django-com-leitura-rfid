// Certifique-se de que os dados estão sendo capturados corretamente
console.log("Data: " + $(this).data('data'));
console.log("Entrada: " + $(this).data('entrada'));
console.log("Saida: " + $(this).data('saida'));

// Obtém os dados do botão que acionou o modal
var data = $(this).data('data');
var entrada = $(this).data('entrada');
var saida = $(this).data('saida');

// Preenche os campos hidden do formulário no modal correspondente
var modal = $($(this).data('bs-target')); // Encontra o modal correto
modal.find('.data-input').val(data);
modal.find('.entrada-input').val(entrada);
modal.find('.saida-input').val(saida);

function openFormModal(salaId, data, entrada, saida) {
const url = `/amem/?salaId=${salaId}&data=${data}&entrada=${entrada}&saida=${saida}`;
const formWindow = window.open(url, "Formulário", "width=500,height=600");

formWindow.onunload = function () {
location.reload(); // Recarrega a página quando a janela pop-out é fechada
};
}

// Adicione esta função em vez da duplicada
function openFormInModal(salaId, data, entrada, saida) {
// Use o ID do modal para abrir
var modal = document.getElementById(`modal${salaId}Formulario`);

// Modifica os campos no formulário dentro do modal
modal.querySelector('.data-input').value = data;
modal.querySelector('.entrada-input').value = entrada;
modal.querySelector('.saida-input').value = saida;

// Abre o modal
var modalInstance = new bootstrap.Modal(modal);
modalInstance.show();
};


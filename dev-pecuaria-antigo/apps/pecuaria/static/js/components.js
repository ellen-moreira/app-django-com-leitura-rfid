/**
 * Classe para criar uma tabela dinâmica em um elemento container.
 */
class CreateDynamicTable {
    /**
     * Construtor da classe CreateDynamicTable.
     * 
     * @param {string} containerId - O ID do elemento container onde a tabela será inserida.
     * @param {string} tableId - O ID a ser atribuído à tabela.
     * @param {Array<string>} tableClass - As classes CSS a serem atribuídas à tabela.
     * @param {string} captionText - O texto do cabeçalho (caption) da tabela.
     * @param {number} numberofColumns - O número de colunas da tabela.
     * @param {Array<string>} namesOfColumns - Os nomes das colunas da tabela.
     * @param {Array<Object>} data - Os dados para popular a tabela.
     */
    constructor(containerId, tableId, tableClass, captionText, numberofColumns, namesOfColumns, data) {
        this.containerId = containerId;           // ID do elemento container onde a tabela será inserida
        this.tableId = tableId;                   // ID a ser atribuído à tabela
        this.tableClass = tableClass;             // Classe(s) a ser(em) atribuída(s) à tabela
        this.captionText = captionText;           // Texto do cabeçalho (caption) da tabela
        this.numberofColumns = numberofColumns;   // Número de colunas da tabela
        this.namesOfColumns = namesOfColumns;     // Nomes das colunas da tabela
        this.data = data;                         // Dados para popular a tabela
    }

    /**
     * Cria e insere a tabela dinâmica no elemento container.
     * 
     * @throws {Error} Se o container não for encontrado pelo ID fornecido.
     * @throws {Error} Se tableClass não for um array.
     * @throws {Error} Se tableClass não for fornecido.
     * @throws {Error} Se data não for fornecido.
     */
    createTable() {
        // Obtém o elemento container pelo ID
        const container = document.getElementById(this.containerId);

        // Verifica se o container foi encontrado, se não for, exibe um erro
        if (!container) {
            console.error('Erro ao tentar encontrar o container para a tabela dinâmica. Verifique o ID informado.');
            return;
        }

         // Cria o elemento da tabela
        const table = document.createElement('table');

        // Define o ID da tabela
        table.setAttribute('id', this.tableId);

        // Verifica se a classe foi fornecida
        if (this.tableClass) {

            // Verifica se tableClass é um array
            if (this.tableClass instanceof Array) {

                // Se houver mais de uma classe, adiciona todas
                if (this.tableClass.length > 1) {
                    this.tableClass.forEach(c => table.classList.add(c));
                } else {
                    // Se houver apenas uma classe, adiciona a única classe
                    table.classList.add(this.tableClass[0]);
                }
            } else {
                // Se tableClass não for um array, exibe um erro
                console.error('Erro ao tentar adicionar a(s) classe(s) na tabela dinâmica. Verifique o tipo informado. Tipo esperado: Array.');
            }
        } else {
            // Se tableClass não for fornecido, exibe um erro
            console.error('Erro ao tentar adicionar a(s) classe(s) na tabela dinâmica. Verifique se a classe foi informada.');
        }

        // Cria o elemento caption e o adiciona à tabela
        const caption = this.createCaption();
        table.appendChild(caption);

        // Cria o elemento thead e o adiciona à tabela
        const thead = this.createThead();
        table.appendChild(thead);

        // Cria o elemento tbody e o adiciona à tabela
        const tbody = this.createTbody();
        table.appendChild(tbody);

        // Adiciona a tabela completa ao container
        container.appendChild(table);
    }

    /**
     * Cria o elemento caption da tabela.
     * 
     * @returns {HTMLElement} O elemento caption criado.
     */
    createCaption() {
        const caption = document.createElement('caption');

        // Define o texto do caption
        caption.textContent = this.captionText;

        return caption;
    }

    /**
     * Cria o elemento thead da tabela.
     * 
     * @returns {HTMLElement} O elemento thead criado.
     */
    createThead() {
        const thead = document.createElement('thead');
        const trHead = document.createElement('tr');

        // Adiciona os nomes das colunas ao thead
        for (let i = 0; i < this.numberofColumns; i++) {
            const th = document.createElement('th');
            th.textContent = this.namesOfColumns[i];
            trHead.appendChild(th);
        }

        // Adiciona a linha de cabeçalho ao thead
        thead.appendChild(trHead);

        return thead;
    }

    /**
     * Cria o elemento tbody da tabela.
     * 
     * @returns {HTMLElement} O elemento tbody criado.
     * 
     * @throws {Error} Se data não for fornecido ou estiver vazio.
     */
    createTbody() {
        const tbody = document.createElement('tbody');

        // Verifica se os dados foram fornecidos
        if (this.data) {

            // Verifica se há dados para popular a tabela
            if (this.data.length > 0) {

                // Adiciona cada linha de dados ao tbody
                this.data.forEach(row => {
                    const tr = this.createRow(row);
                    tbody.appendChild(tr);
                });
            }
        } else {

            // Se os dados não foram fornecidos, exibe um erro
            console.error('Erro ao tentar criar a tabela dinâmica. Não foi possível encontrar dados para popular a tabela.');
        }

        return tbody;
    }

    /**
     * Cria uma linha da tabela com os dados fornecidos.
     * 
     * @param {Object} rowData - Os dados da linha a ser criada.
     * @returns {HTMLElement} O elemento tr criado.
     */
    createRow(rowData) {
        const tr = document.createElement('tr');

        // Adiciona cada célula da linha
        for (let key in rowData) {
            const td = document.createElement('td');

            // Verifica se o dado é um array
            if (Array.isArray(rowData[key])) {

                // Se for, adiciona os elementos do array como texto da célula, separando-os por quebras de linha
                td.innerHTML = rowData[key].map(item => item.title ? item.title : item).join('<br>');
                td.style.whiteSpace = 'pre-line';
            } else {
                // Se não for, adiciona o dado como texto da célula
                td.textContent = rowData[key];
            }

            tr.appendChild(td);
        }

        return tr;
    }
}

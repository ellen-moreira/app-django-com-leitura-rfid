class JsonModifier:
    def __init__(self, data):
        if not isinstance(data, (dict, list)):
            raise ValueError("Os dados devem ser um dicionário ou uma lista de dicionários")
        self.data = data

    def remove_keys(self, keys):
        if isinstance(keys, str):
            keys = [keys]
        if isinstance(keys, list):
            for item in self.data:
                for key in keys:
                    item.pop(key, None)
        else:
            raise ValueError("As chaves devem ser uma string ou uma lista de strings")
        
    def add_keys(self, keys):
        if isinstance(keys, dict):
            self.data.update(keys)
        elif isinstance(keys, list):
            for key in keys:
                self.data.update(key)
        else:
            raise ValueError("As chaves devem ser um dicionário ou uma lista de dicionários")
        
    def keep_keys(self, keys_to_keep):
        if isinstance(keys_to_keep, str):
            keys_to_keep = [keys_to_keep]
        if isinstance(keys_to_keep, list):
            for item in self.data:
                for key in list(item.keys()):
                    if key not in keys_to_keep:
                        item.pop(key, None)
        else:
            raise ValueError("As chaves devem ser uma string ou uma lista de strings")
        
    def add_calculation_to_dict(self, calculations):
        for calculation in calculations:
            expression = calculation['expression']
            relation = calculation['relation']
            new_key = calculation['new_key']
            for item in self.data:
                local_vars = {key: float(item[val]) for key, val in relation.items()}
                item[new_key] = eval(expression, {}, local_vars)

    def get_json(self):
        return self.data
    
# -----------------------------------------------------------------------------------------------------
    
# Exemplo de uso em conjunto com a API de produtos:

# def produtos(request):
#     produtos_api = requests.get('http://127.0.0.1:8000/api/industria/produtos/') # Guarda a resposta da API em uma variável

#     # Verifica se a resposta foi bem sucedida
#     if produtos_api.status_code == 200: 
#         # Converte a resposta em um dicionário
#         produtos = produtos_api.json()

#         # Instancia a classe JsonModifier
#         objeto_classe = JsonModifier(produtos)

#         # Variável que guarda os cálculos a serem feitos
#         calculos = [
#             {
#                 'expression': 'valor * quantidade',
#                 'relation': {'valor': 'valor', 'quantidade': 'quantidade'},
#                 'new_key': 'total'
#             },
#             {
#                 'expression': 'valor * quantidade * 0.1',
#                 'relation': {'valor': 'valor', 'quantidade': 'quantidade'},
#                 'new_key': 'desconto'
#             }
#         ]

#         # Chama o método da classe que adiciona os cálculos ao dicionário
#         objeto_classe.add_calculation_to_dict(calculos)

#         # Variáveis que guardam o número de colunas e os nomes das colunas
#         number_of_columns = len(produtos[0].keys())
#         name_of_columns = list(produtos[0].keys())

#     # Contexto que será passado para o template
#     context = {
#         'produtos': json.dumps(produtos, indent=4, ensure_ascii=False), # Converte o dicionário em uma string JSON
#         'number_of_columns': number_of_columns, # Número de colunas
#         'name_of_columns': name_of_columns # Nomes das colunas
#     }

#     # Renderiza o template 'produtos.html' com o contexto
#     return render(request, 'produtos.html', context)
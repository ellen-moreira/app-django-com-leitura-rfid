from app.models import *
from django.contrib import admin
from django.utils.safestring import mark_safe
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget

# Funções auxiliares

def get_setor(user):
    """
    Recupera o primeiro setor associado a um usuário específico.

    Esta função realiza uma consulta no banco de dados para encontrar os setores que 
    possuem o usuário informado e retorna o primeiro setor encontrado.

    Parâmetros:
    - user (User): Instância do usuário para o qual se deseja recuperar o setor associado.

    Retorno:
    - Setor: Instância do setor associado ao usuário informado.
    - None: Caso o usuário não possua setores associados.

    Exemplo:
    >>> setor = get_setor(user)
    >>> if setor:
    >>>     print(setor.nome)
    >>> else:
    >>>     print('Usuário não possui setores associados.')
    """

    return Setor.objects.filter(usuarios=user).first() if user else None

# Importação e Exportação de Dados (Depende das planilhas passadas pelos setores)

class AnimalExportResource(resources.ModelResource):
    """
    Classe utilizada para gerenciar a exportação de dados do modelo `Animal` no Django Admin.

    A `AnimalExportResource` permite mapear campos do modelo `Animal` para arquivos de exportação
    (como CSV ou Excel), realizando formatações e transformações antes de gerar o arquivo.

    Atributos:
    - model (Model): Modelo do Django que será utilizado para exportação.
    - fields (List): Lista de campos do modelo que serão exportados.
    - export_order (List): Ordem de exportação dos campos.

    Métodos:
    - export_data: Exporta dados para um arquivo de dados.

    Exemplo:
    >>> resource = AnimalExportResource()
    >>> dataset = resource.export_data(Animal.objects.all())
    >>> with open('animais.csv', 'w') as file:
    >>>     file.write(dataset.csv)

    Referências:
    - https://django-import-export.readthedocs.io/en/latest/resources.html
    - https://django-import-export.readthedocs.io/en/latest/api_resources.html
    """

    especie = fields.Field(
        column_name='especie',
        attribute='especie',
        widget=ForeignKeyWidget(Especie, 'nome')
    )

    raca = fields.Field(
        column_name='raca',
        attribute='raca',
        widget=ForeignKeyWidget(Raca, 'nome')
    )

    tipo = fields.Field(
        column_name='tipo',
        attribute='tipo',
        widget=ForeignKeyWidget(Tipo, 'nome')
    )

    setor = fields.Field(
        column_name='setor',
        attribute='setor',
        widget=ForeignKeyWidget(Setor, 'nome')
    )

    class Meta:
        """
        Configurações da exportação, definindo o modelo `Animal` e os campos a serem exportados.

        Atributos:
        - model: Especifica que o modelo `Animal` será utilizado para a exportação.
        - fields: Lista de campos a serem exportados: `id`, `identificacao_unica`, `rfid`, `especie`, `raca`, `tipo`, `sexo`, `peso_de_nascimento`, `data_hora_de_nascimento`, `mae`, `pai`, `status`, `observacao`, `setor`.
        - export_order: Define a ordem de exportação dos campos.
        """

        model = Animal
        fields = ['id', 'identificacao_unica', 'rfid', 'especie', 'raca', 'tipo', 'sexo', 'peso_de_nascimento', 'data_hora_de_nascimento', 'mae', 'pai', 'status', 'observacao', 'setor']
        export_order = ['id', 'identificacao_unica', 'rfid', 'especie', 'raca', 'tipo', 'sexo', 'peso_de_nascimento', 'data_hora_de_nascimento', 'mae', 'pai', 'status', 'observacao', 'setor']

class SuinoImportResource(resources.ModelResource):
    """
    Classe utilizada para gerenciar a importação de dados do modelo `Suino` no Django Admin.

    A `SuinoImportResource` permite mapear campos de arquivos de importação (como CSV ou Excel) 
    para o modelo `Suino`, realizando validações e formatações antes de salvar os dados no banco.

    Atributos:
    - model (Model): Modelo do Django que será utilizado para importação.
    - fields (List): Lista de campos do modelo que serão importados.
    - import_order (List): Ordem de importação dos campos.

    Métodos:
    - before_import_row: Executado antes de importar uma linha de dados.
    - after_import_row: Executado após importar uma linha de dados.
    - import_data: Importa dados de um arquivo de dados.

    Exemplo:
    >>> resource = SuinoImportResource()
    >>> dataset = Dataset()
    >>> dataset.load(open('suinos.csv').read())
    >>> result = resource.import_data(dataset)
    
    Referências:
    - https://django-import-export.readthedocs.io/en/latest/resources.html
    - https://django-import-export.readthedocs.io/en/latest/api_resources.html
    """

    tipo = fields.Field(
        column_name='tipo',
        attribute='tipo',
        widget=ForeignKeyWidget(Tipo, 'nome')
    )

    def before_import_row(self, row, **kwargs):
        """
        Método chamado antes de importar cada linha de dados.

        - Formata o campo `identificacao_unica` para garantir que seja uma string, 
          removendo decimais quando necessário.
        - Garante que o tipo especificado na linha de importação exista no banco de dados; 
          se não existir, cria um novo registro de `Tipo`.

        Parâmetros:
        - row (dict): Dicionário representando os dados da linha atual da importação.
        - kwargs: Parâmetros adicionais que podem ser passados para o método.

        Operações:
        1. Verifica se `identificacao_unica` é um float e, se for, converte-o para string.
        2. Verifica se o `Tipo` correspondente ao nome fornecido existe no banco; se não, cria-o.
        """

        row['identificacao_unica'] = str(int(row['identificacao_unica'])) if isinstance(row['identificacao_unica'], float) else row['identificacao_unica']
        Tipo.objects.get_or_create(nome=row['tipo'], defaults={'nome': row['tipo']})

    class Meta:
        """
        Configurações da importação, definindo o modelo `Suino` e os campos a serem importados.

        Atributos:
        - model: Especifica que o modelo `Suino` será utilizado para a importação.
        - fields: Lista de campos a serem importados: `id`, `identificacao_unica`, `tipo`, `sexo`.
        - import_order: Define a ordem de importação dos campos.
        """

        model = Suino
        fields = ['id', 'identificacao_unica', 'tipo', 'sexo']
        import_order = ['id', 'identificacao_unica', 'tipo', 'sexo']

class SuinoExportResource(AnimalExportResource):
    """
    Classe utilizada para gerenciar a exportação de dados do modelo `Suino` no Django Admin.

    A `SuinoExportResource` estende a classe `AnimalExportResource` e adiciona campos específicos
    do modelo `Suino` que devem ser exportados para arquivos de dados.

    Atributos:
    - model (Model): Modelo do Django que será utilizado para exportação.
    - fields (List): Lista de campos do modelo que serão exportados.
    - export_order (List): Ordem de exportação dos campos.

    Métodos:
    - export_data: Exporta dados para um arquivo de dados.

    Exemplo:
    >>> resource = SuinoExportResource()
    >>> dataset = resource.export_data(Suino.objects.all())
    >>> with open('suinos.csv', 'w') as file:
    >>>     file.write(dataset.csv)

    Referências:
    - https://django-import-export.readthedocs.io/en/latest/resources.html
    - https://django-import-export.readthedocs.io/en/latest/api_resources.html
    """

    class Meta:
        """
        Configurações da exportação, definindo o modelo `Suino` e os campos a serem exportados.

        Atributos:
        - model: Especifica que o modelo `Suino` será utilizado para a exportação.
        - fields: Lista de campos a serem exportados: `id`, `identificacao_unica`, `rfid`, `especie`, `raca`, `tipo`, `sexo`, `peso_de_nascimento`, `data_hora_de_nascimento`, `mae`, `pai`, `status`, `observacao`, `setor`.
        - export_order: Define a ordem de exportação dos campos.
        """

        model = Suino
        fields = AnimalExportResource.Meta.fields
        export_order = AnimalExportResource.Meta.export_order

class BovinoCorteImportResource(resources.ModelResource):
    """
    Classe utilizada para gerenciar a importação de dados do modelo `BovinoCorte` no Django Admin.

    A `BovinoCorteImportResource` permite mapear campos de arquivos de importação (como CSV ou Excel)
    para o modelo `BovinoCorte`, realizando validações e formatações antes de salvar os dados no banco.

    Atributos:
    - model (Model): Modelo do Django que será utilizado para importação.
    - fields (List): Lista de campos do modelo que serão importados.
    - import_order (List): Ordem de importação dos campos.

    Métodos:
    - before_import_row: Executado antes de importar uma linha de dados.
    - after_import_row: Executado após importar uma linha de dados.
    - import_data: Importa dados de um arquivo de dados.

    Exemplo:
    >>> resource = BovinoCorteImportResource()
    >>> dataset = Dataset()
    >>> dataset.load(open('bovinos_corte.csv').read())
    >>> result = resource.import_data(dataset)

    Referências:
    - https://django-import-export.readthedocs.io/en/latest/resources.html
    - https://django-import-export.readthedocs.io/en/latest/api_resources.html
    """

    raca = fields.Field(
        column_name='raca',
        attribute='raca',
        widget=ForeignKeyWidget(Raca, 'nome')
    )

    tipo = fields.Field(
        column_name='tipo',
        attribute='tipo',
        widget=ForeignKeyWidget(Tipo, 'nome')
    )

    def before_import_row(self, row, **kwargs):
        """
        Método chamado antes de importar cada linha de dados.

        - Formata o campo `identificacao_unica` para garantir que seja uma string,
          removendo decimais quando necessário.

        Parâmetros:
        - row (dict): Dicionário representando os dados da linha atual da importação.
        - kwargs: Parâmetros adicionais que podem ser passados para o método.

        Operações:
        1. Verifica se `identificacao_unica` é um float e, se for, converte-o para string.
        2. Verifica se o `Tipo` e a `Raça` correspondentes aos nomes fornecidos existem no banco;
        """

        row['identificacao_unica'] = str(int(row['identificacao_unica'])) if isinstance(row['identificacao_unica'], float) else str(row['identificacao_unica'])

        row['data_hora_de_nascimento'] = timezone.make_aware(row['data_hora_de_nascimento'])

        Raca.objects.get_or_create(nome=row['raca'], defaults={'nome': row['raca']})
        Tipo.objects.get_or_create(nome=row['tipo'], defaults={'nome': row['tipo']})

    class Meta:
        """
        Configurações da importação, definindo o modelo `BovinoCorte` e os campos a serem importados.

        Atributos:
        - model: Especifica que o modelo `BovinoCorte` será utilizado para a importação.
        - fields: Lista de campos a serem importados: `id`, `identificacao_unica`, `raca`, `tipo`, `sexo`, `data_hora_de_nascimento`, `observacao`, `modo_de_criacao`, `local`.
        - import_order: Define a ordem de importação dos campos.
        """

        model = BovinoCorte
        fields = ['id', 'identificacao_unica', 'raca', 'tipo', 'sexo', 'data_hora_de_nascimento', 'observacao', 'modo_de_criacao', 'local']
        import_order = ['id', 'identificacao_unica', 'raca', 'tipo', 'sexo', 'data_hora_de_nascimento', 'observacao', 'modo_de_criacao', 'local']

class BovinoCorteExportResource(AnimalExportResource):
    """
    Classe utilizada para gerenciar a exportação de dados do modelo `BovinoCorte` no Django Admin.

    A `BovinoCorteExportResource` estende a classe `AnimalExportResource` e adiciona campos específicos
    do modelo `BovinoCorte` que devem ser exportados para arquivos de dados.

    Atributos:
    - model (Model): Modelo do Django que será utilizado para exportação.
    - fields (List): Lista de campos do modelo que serão exportados.
    - export_order (List): Ordem de exportação dos campos.

    Métodos:
    - export_data: Exporta dados para um arquivo de dados.

    Exemplo:
    >>> resource = BovinoCorteExportResource()
    >>> dataset = resource.export_data(BovinoCorte.objects.all())
    >>> with open('bovinos_corte.csv', 'w') as file:
    >>>     file.write(dataset.csv)

    Referências:
    - https://django-import-export.readthedocs.io/en/latest/resources.html
    - https://django-import-export.readthedocs.io/en/latest/api_resources.html
    """

    class Meta:
        """
        Configurações da exportação, definindo o modelo `BovinoCorte` e os campos a serem exportados.

        Atributos:
        - model: Especifica que o modelo `BovinoCorte` será utilizado para a exportação.
        - fields: Lista de campos a serem exportados: `id`, `identificacao_unica`, `rfid`, `especie`, `raca`, `tipo`, `sexo`, `peso_de_nascimento`, `data_hora_de_nascimento`, `mae`, `pai`, `status`, `observacao`, `setor`, `modo_de_criacao`, `local`.
        - export_order: Define a ordem de exportação dos campos.
        """

        model = BovinoCorte
        fields = AnimalExportResource.Meta.fields + ['modo_de_criacao', 'local']
        export_order = AnimalExportResource.Meta.export_order + ['modo_de_criacao', 'local']

class BovinoLeiteImportResource(resources.ModelResource):
    """
    Classe utilizada para gerenciar a importação de dados do modelo `BovinoLeite` no Django Admin.

    A `BovinoLeiteImportResource` permite mapear campos de arquivos de importação (como CSV ou Excel)
    para o modelo `BovinoLeite`, realizando validações e formatações antes de salvar os dados no banco.

    Atributos:
    - model (Model): Modelo do Django que será utilizado para importação.
    - fields (List): Lista de campos do modelo que serão importados.
    - import_order (List): Ordem de importação dos campos.

    Métodos:
    - before_import_row: Executado antes de importar uma linha de dados.
    - after_import_row: Executado após importar uma linha de dados.
    - import_data: Importa dados de um arquivo de dados.

    Exemplo:
    >>> resource = BovinoLeiteImportResource()
    >>> dataset = Dataset()
    >>> dataset.load(open('bovinos_leite.csv').read())
    >>> result = resource.import_data(dataset)

    Referências:
    - https://django-import-export.readthedocs.io/en/latest/resources.html
    - https://django-import-export.readthedocs.io/en/latest/api_resources.html
    """

    raca = fields.Field(
        column_name='raca',
        attribute='raca',
        widget=ForeignKeyWidget(Raca, 'nome')
    )

    def before_import_row(self, row, **kwargs):
        """
        Método chamado antes de importar cada linha de dados.

        - Formata o campo `identificacao_unica` para garantir que seja uma string,
          removendo decimais quando necessário.
        - Garante que a `Raça` correspondente ao nome fornecido exista no banco.

        Parâmetros:
        - row (dict): Dicionário representando os dados da linha atual da importação.
        - kwargs: Parâmetros adicionais que podem ser passados para o método.

        Operações:
        1. Verifica se `identificacao_unica` é um float e, se for, converte-o para string.
        2. Verifica se a `Raça` correspondente ao nome fornecido existe no banco; se não, cria um novo registro de `Raça`.
        """

        row['identificacao_unica'] = str(int(row['identificacao_unica'])) if isinstance(row['identificacao_unica'], float) else str(row['identificacao_unica'])
        Raca.objects.get_or_create(nome=row['raca'], defaults={'nome': row['raca']})


    class Meta:
        """
        Configurações da importação, definindo o modelo `BovinoLeite` e os campos a serem importados.

        Atributos:
        - model: Especifica que o modelo `BovinoLeite` será utilizado para a importação.
        - fields: Lista de campos a serem importados: `id`, `identificacao_unica`, `raca`, `sexo`, `data_hora_de_nascimento`, `observacao`, `nome`, `grau_de_sangue`, `pelagem`.
        - import_order: Define a ordem de importação dos campos.
        """

        model = BovinoLeite
        fields = ['id', 'identificacao_unica', 'raca', 'sexo', 'data_hora_de_nascimento', 'observacao', 'nome', 'grau_de_sangue', 'pelagem']
        import_order = ['id', 'identificacao_unica', 'raca', 'sexo', 'data_hora_de_nascimento', 'observacao', 'nome', 'grau_de_sangue', 'pelagem']

class BovinoLeiteExportResource(AnimalExportResource):
    """
    Classe utilizada para gerenciar a exportação de dados do modelo `BovinoLeite` no Django Admin.

    A `BovinoLeiteExportResource` estende a classe `AnimalExportResource` e adiciona campos específicos
    do modelo `BovinoLeite` que devem ser exportados para arquivos de dados.

    Atributos:
    - model (Model): Modelo do Django que será utilizado para exportação.
    - fields (List): Lista de campos do modelo que serão exportados.
    - export_order (List): Ordem de exportação dos campos.

    Métodos:
    - export_data: Exporta dados para um arquivo de dados.

    Exemplo:
    >>> resource = BovinoLeiteExportResource()
    >>> dataset = resource.export_data(BovinoLeite.objects.all())
    >>> with open('bovinos_leite.csv', 'w') as file:
    >>>     file.write(dataset.csv)

    Referências:
    - https://django-import-export.readthedocs.io/en/latest/resources.html
    - https://django-import-export.readthedocs.io/en/latest/api_resources.html
    """

    class Meta:
        model = BovinoLeite
        fields = AnimalExportResource.Meta.fields + ['nome', 'grau_de_sangue', 'pelagem']
        export_order = AnimalExportResource.Meta.export_order + ['nome', 'grau_de_sangue', 'pelagem']

class LoteImportResource(resources.ModelResource):
    """
    Classe utilizada para gerenciar a importação de dados do modelo `Lote` no Django Admin.

    A `LoteImportResource` permite mapear campos de arquivos de importação (como CSV ou Excel)
    para o modelo `Lote`, realizando validações e formatações antes de salvar os dados no banco.

    Atributos:
    - model (Model): Modelo do Django que será utilizado para importação.
    - fields (List): Lista de campos do modelo que serão importados.
    - import_order (List): Ordem de importação dos campos.

    Métodos:
    - before_import_row: Executado antes de importar uma linha de dados.
    - after_import_row: Executado após importar uma linha de dados.
    - import_data: Importa dados de um arquivo de dados.

    Exemplo:
    >>> resource = LoteImportResource()
    >>> dataset = Dataset()
    >>> dataset.load(open('lotes.csv').read())
    >>> result = resource.import_data(dataset)

    Referências:
    - https://django-import-export.readthedocs.io/en/latest/resources.html
    - https://django-import-export.readthedocs.io/en/latest/api_resources.html
    """

    baia = fields.Field(
        column_name='baia',
        attribute='baia',
        widget=ForeignKeyWidget(Baia, 'numero')
    )

    setor = fields.Field(
        column_name='setor',
        attribute='setor',
        widget=ForeignKeyWidget(Setor, 'nome')
    )

    def before_import_row(self, row, **kwargs):
        """
        Método chamado antes de importar cada linha de dados.

        - Garante que a `Baia` e o `Setor` correspondentes aos números fornecidos existam no banco.

        Parâmetros:
        - row (dict): Dicionário representando os dados da linha atual da importação.
        - kwargs: Parâmetros adicionais que podem ser passados para o método.

        Operações:
        1. Verifica se a `Baia` e o `Setor` correspondentes aos números fornecidos existem no banco;
        2. Verifica se a `Setor` correspondente ao nome fornecido existe no banco; se não, cria um novo registro de `Setor`.
        """

        Baia.objects.get_or_create(numero=row['baia'], defaults={'numero': row['baia']})
        Setor.objects.get_or_create(nome=row['setor'], defaults={'nome': row['setor']})

    class Meta:
        """
        Configurações da importação, definindo o modelo `Lote` e os campos a serem importados.
        
        Atributos:
        - model: Especifica que o modelo `Lote` será utilizado para a importação.
        - fields: Lista de campos a serem importados: `id`, `numero`, `baia`, `setor`.
        - import_order: Define a ordem de importação dos campos.
        """

        model = Lote
        fields = ['id', 'numero', 'baia', 'setor']
        import_order = ['id', 'numero', 'baia', 'setor']

class LoteExportResource(resources.ModelResource):
    """
    Classe utilizada para gerenciar a exportação de dados do modelo `Lote` no Django Admin.

    A `LoteExportResource` permite mapear campos do modelo `Lote` para arquivos de exportação
    (como CSV ou Excel), realizando formatações e transformações antes de gerar o arquivo.

    Atributos:
    - model (Model): Modelo do Django que será utilizado para exportação.
    - fields (List): Lista de campos do modelo que serão exportados.
    - export_order (List): Ordem de exportação dos campos.

    Métodos:
    - export_data: Exporta dados para um arquivo de dados.

    Exemplo:
    >>> resource = LoteExportResource()
    >>> dataset = resource.export_data(Lote.objects.all())
    >>> with open('lotes.csv', 'w') as file:
    >>>     file.write(dataset.csv)

    Referências:
    - https://django-import-export.readthedocs.io/en/latest/resources.html
    - https://django-import-export.readthedocs.io/en/latest/api_resources.html
    """

    baia = fields.Field(
        column_name='baia',
        attribute='baia',
        widget=ForeignKeyWidget(Baia, 'numero')
    )

    setor = fields.Field(
        column_name='setor',
        attribute='setor',
        widget=ForeignKeyWidget(Setor, 'nome')
    )

    class Meta:
        """
        Configurações da exportação, definindo o modelo `Lote` e os campos a serem exportados.

        Atributos:
        - model: Especifica que o modelo `Lote` será utilizado para a exportação.
        - fields: Lista de campos a serem exportados: `id`, `numero`, `baia`, `setor`.
        - export_order: Define a ordem de exportação dos campos.
        """

        model = Lote
        fields = ['id', 'numero', 'baia', 'setor']
        export_order = ['id', 'numero', 'baia', 'setor']

class LoteExportResource(resources.ModelResource):
    """
    Classe utilizada para gerenciar a exportação de dados do modelo `Lote` no Django Admin.

    A `LoteExportResource` permite mapear campos do modelo `Lote` para arquivos de exportação
    (como CSV ou Excel), realizando formatações e transformações antes de gerar o arquivo.

    Atributos:
    - model (Model): Modelo do Django que será utilizado para exportação.
    - fields (List): Lista de campos do modelo que serão exportados.
    - export_order (List): Ordem de exportação dos campos.

    Métodos:
    - export_data: Exporta dados para um arquivo de dados.

    Exemplo:
    >>> resource = LoteExportResource()
    >>> dataset = resource.export_data(Lote.objects.all())
    >>> with open('lotes.csv', 'w') as file:
    >>>     file.write(dataset.csv)

    Referências:
    - https://django-import-export.readthedocs.io/en/latest/resources.html
    - https://django-import-export.readthedocs.io/en/latest/api_resources.html
    """

    baia = fields.Field(
        column_name='baia',
        attribute='baia',
        widget=ForeignKeyWidget(Baia, 'numero')
    )

    setor = fields.Field(
        column_name='setor',
        attribute='setor',
        widget=ForeignKeyWidget(Setor, 'nome')
    )

    class Meta:
        """
        Configurações da exportação, definindo o modelo `Lote` e os campos a serem exportados.

        Atributos:
        - model: Especifica que o modelo `Lote` será utilizado para a exportação.
        - fields: Lista de campos a serem exportados: `id`, `numero`, `baia`, `setor`.
        - export_order: Define a ordem de exportação dos campos.
        """

        model = Lote
        fields = ['id', 'numero', 'baia', 'setor']
        export_order = ['id', 'numero', 'baia', 'setor']

class PartoImportResource(resources.ModelResource):
    """
    Classe utilizada para gerenciar a importação de dados do modelo `Parto` no Django Admin.

    A `PartoImportResource` permite mapear campos de arquivos de importação (como CSV ou Excel)
    para o modelo `Parto`, realizando validações e formatações antes de salvar os dados no banco.

    Atributos:
    - model (Model): Modelo do Django que será utilizado para importação.
    - fields (List): Lista de campos do modelo que serão importados.
    - import_order (List): Ordem de importação dos campos.

    Métodos:
    - before_import_row: Executado antes de importar uma linha de dados.
    - after_import_row: Executado após importar uma linha de dados.
    - import_data: Importa dados de um arquivo de dados.

    Exemplo:
    >>> resource = PartoImportResource()
    >>> dataset = Dataset()
    >>> dataset.load(open('partos.csv').read())
    >>> result = resource.import_data(dataset)

    Referências:
    - https://django-import-export.readthedocs.io/en/latest/resources.html
    - https://django-import-export.readthedocs.io/en/latest/api_resources.html
    """

    setor = fields.Field(
        column_name='setor',
        attribute='setor',
        widget=ForeignKeyWidget(Setor, 'nome')
    )

    def before_import_row(self, row, **kwargs):
        """
        Método chamado antes de importar cada linha de dados.

        - Garante que o `Setor` correspondente ao nome fornecido exista no banco.

        Parâmetros:
        - row (dict): Dicionário representando os dados da linha atual da importação.
        - kwargs: Parâmetros adicionais que podem ser passados para o método.

        Operações:
        1. Verifica se o `Setor` correspondente ao nome fornecido existe no banco; se não, cria um novo registro de `Setor`.
        """

        Setor.objects.get_or_create(nome=row['setor'], defaults={'nome': row['setor']})

    class Meta:
        """
        Configurações da importação, definindo o modelo `Parto` e os campos a serem importados.

        Atributos:
        - model: Especifica que o modelo `Parto` será utilizado para a importação.
        - fields: Lista de campos a serem importados: `id`, `femea`, `macho`, `data_hora_do_parto`, `tipo`, `quantidade_de_filhotes_vivos`, `quantidade_de_filhotes_mortos`, `quantidade_de_filhotes_mumificados`, `setor`, `observacao`.
        - import_order: Define a ordem de importação dos campos.
        """

        model = Parto
        fields = ['id', 'femea', 'macho', 'data_hora_do_parto', 'tipo', 'quantidade_de_filhotes_vivos', 'quantidade_de_filhotes_mortos', 'quantidade_de_filhotes_mumificados', 'setor', 'observacao']
        import_order = ['id', 'femea', 'macho', 'data_hora_do_parto', 'tipo', 'quantidade_de_filhotes_vivos', 'quantidade_de_filhotes_mortos', 'quantidade_de_filhotes_mumificados', 'setor', 'observacao']

class PartoExportResource(resources.ModelResource):
    """
    Classe utilizada para gerenciar a exportação de dados do modelo `Parto` no Django Admin.

    A `PartoExportResource` permite mapear campos do modelo `Parto` para arquivos de exportação
    (como CSV ou Excel), realizando formatações e transformações antes de gerar o arquivo.

    Atributos:
    - model (Model): Modelo do Django que será utilizado para exportação.
    - fields (List): Lista de campos do modelo que serão exportados.
    - export_order (List): Ordem de exportação dos campos.

    Métodos:
    - export_data: Exporta dados para um arquivo de dados.

    Exemplo:
    >>> resource = PartoExportResource()
    >>> dataset = resource.export_data(Parto.objects.all())
    >>> with open('partos.csv', 'w') as file:
    >>>     file.write(dataset.csv)

    Referências:
    - https://django-import-export.readthedocs.io/en/latest/resources.html
    - https://django-import-export.readthedocs.io/en/latest/api_resources.html
    """

    femea = fields.Field(
        column_name='femea',
        attribute='femea',
        widget=ForeignKeyWidget(Animal, 'identificacao_unica')
    )

    macho = fields.Field(
        column_name='macho',
        attribute='macho',
        widget=ForeignKeyWidget(Animal, 'identificacao_unica')
    )

    setor = fields.Field(
        column_name='setor',
        attribute='setor',
        widget=ForeignKeyWidget(Setor, 'nome')
    )

    class Meta:
        """
        Configurações da exportação, definindo o modelo `Parto` e os campos a serem exportados.

        Atributos:
        - model: Especifica que o modelo `Parto` será utilizado para a exportação.
        - fields: Lista de campos a serem exportados: `id`, `femea`, `macho`, `data_hora_do_parto`, `tipo`, `quantidade_de_filhotes_vivos`, `quantidade_de_filhotes_mortos`, `quantidade_de_filhotes_mumificados`, `setor`, `observacao`.
        - export_order: Define a ordem de exportação dos campos.
        """

        model = Parto
        fields = ['id', 'femea', 'macho', 'data_hora_do_parto', 'tipo', 'quantidade_de_filhotes_vivos', 'quantidade_de_filhotes_mortos', 'quantidade_de_filhotes_mumificados', 'setor', 'observacao']
        export_order = ['id', 'femea', 'macho', 'data_hora_do_parto', 'tipo', 'quantidade_de_filhotes_vivos', 'quantidade_de_filhotes_mortos', 'quantidade_de_filhotes_mumificados', 'setor', 'observacao']

class ManejoImportResource(resources.ModelResource):
    """
    Classe utilizada para gerenciar a importação de dados do modelo `Manejo` no Django Admin.

    A `ManejoImportResource` permite mapear campos de arquivos de importação (como CSV ou Excel)
    para o modelo `Manejo`, realizando validações e formatações antes de salvar os dados no banco.

    Atributos:
    - model (Model): Modelo do Django que será utilizado para importação.
    - fields (List): Lista de campos do modelo que serão importados.
    - import_order (List): Ordem de importação dos campos.

    Métodos:
    - before_import_row: Executado antes de importar uma linha de dados.
    - after_import_row: Executado após importar uma linha de dados.
    - import_data: Importa dados de um arquivo de dados.

    Exemplo:
    >>> resource = ManejoImportResource()
    >>> dataset = Dataset()
    >>> dataset.load(open('manejos.csv').read())
    >>> result = resource.import_data(dataset)

    Referências:
    - https://django-import-export.readthedocs.io/en/latest/resources.html
    - https://django-import-export.readthedocs.io/en/latest/api_resources.html
    """

    funcionario = fields.Field(
        column_name='funcionario',
        attribute='funcionario',
        widget=ForeignKeyWidget(Funcionario, 'nome')
    )

    animal = fields.Field(
        column_name='animal',
        attribute='animal',
        widget=ForeignKeyWidget(Animal, 'identificacao_unica')
    )

    setor = fields.Field(
        column_name='setor',
        attribute='setor',
        widget=ForeignKeyWidget(Setor, 'nome')
    )

    def before_import_row(self, row, **kwargs):
        """
        Método chamado antes de importar cada linha de dados.

        - Garante que o `Funcionario` e o `Setor` correspondentes aos nomes fornecidos existam no banco.

        Parâmetros:
        - row (dict): Dicionário representando os dados da linha atual da importação.
        - kwargs: Parâmetros adicionais que podem ser passados para o método.

        Operações:
        1. Verifica se o `Funcionario` e o `Setor` correspondentes aos nomes fornecidos existem no banco;
        """

        Funcionario.objects.get_or_create(nome=row['funcionario'], defaults={'nome': row['funcionario']})
        Setor.objects.get_or_create(nome=row['setor'], defaults={'nome': row['setor']})

    class Meta:
        model = Manejo
        fields = ['id', 'funcionario', 'data_hora_do_manejo', 'animal', 'lote', 'setor', 'observacao']
        import_order = ['id', 'funcionario', 'data_hora_do_manejo', 'animal', 'lote', 'setor', 'observacao']

class ManejoExportResource(resources.ModelResource):
    """
    Classe utilizada para gerenciar a exportação de dados do modelo `Manejo` no Django Admin.

    A `ManejoExportResource` permite mapear campos do modelo `Manejo` para arquivos de exportação
    (como CSV ou Excel), realizando formatações e transformações antes de gerar o arquivo.

    Atributos:
    - model (Model): Modelo do Django que será utilizado para exportação.
    - fields (List): Lista de campos do modelo que serão exportados.
    - export_order (List): Ordem de exportação dos campos.

    Métodos:
    - export_data: Exporta dados para um arquivo de dados.

    Exemplo:
    >>> resource = ManejoExportResource()
    >>> dataset = resource.export_data(Manejo.objects.all())
    >>> with open('manejos.csv', 'w') as file:
    >>>     file.write(dataset.csv)

    Referências:
    - https://django-import-export.readthedocs.io/en/latest/resources.html
    - https://django-import-export.readthedocs.io/en/latest/api_resources.html
    """

    funcionario = fields.Field(
        column_name='funcionario',
        attribute='funcionario',
        widget=ForeignKeyWidget(Funcionario, 'nome')
    )

    animal = fields.Field(
        column_name='animal',
        attribute='animal',
        widget=ForeignKeyWidget(Animal, 'identificacao_unica')
    )

    setor = fields.Field(
        column_name='setor',
        attribute='setor',
        widget=ForeignKeyWidget(Setor, 'nome')
    )

    class Meta:
        model = Manejo
        fields = ['id', 'funcionario', 'data_hora_do_manejo', 'animal', 'lote', 'setor', 'observacao']
        export_order = ['id', 'funcionario', 'data_hora_do_manejo', 'animal', 'lote', 'setor', 'observacao']

# Register your models here.
@admin.register(Setor)
class SetorAdmin(admin.ModelAdmin):
    """
    Administração do modelo Setor no Django Admin.
    """

    # Exibe os usuários associados ao setor em um widget de seleção múltipla horizontal
    filter_horizontal = ['usuarios']
    
    # Campos que serão exibidos na lista de setores
    list_display = ['nome', 'get_usuarios']
    
    # Campos que serão links para a página de edição
    list_display_links = ['nome']
    
    # Filtros laterais para facilitar a busca
    list_filter = ['nome', 'usuarios']
    
    # Define a paginação para 10 itens por página
    list_per_page = 10
    
    # Ordenação padrão dos setores no admin
    ordering = ['id']
    
    # Campos pelos quais é possível buscar setores
    search_fields = ['nome', 'usuarios__username']
    
    # Exibe a contagem completa de resultados na paginação
    show_full_result_count = True

    def get_usuarios(self, obj):
        """
        Retorna uma lista de usuários associados ao setor, separados por linha.

        Args:
            obj (Setor): O objeto Setor.

        Returns:
            str: String com nomes de usuários separados por <br>.
        """
        return mark_safe('<br>'.join([usuario.username for usuario in obj.usuarios.all()]))
    
    # Define a descrição da coluna no admin
    get_usuarios.short_description = 'Usuários'


@admin.register(Galpao)
class GalpaoAdmin(admin.ModelAdmin):
    """
    Administração do modelo Galpão no Django Admin.
    """

    # Campos que serão exibidos na lista de galpões
    list_display = ['nome', 'setor']
    
    # Campos que serão links para a página de edição
    list_display_links = ['nome']
    
    # Filtros laterais para facilitar a busca
    list_filter = ['nome', 'setor']
    
    # Define a paginação para 10 itens por página
    list_per_page = 10
    
    # Ordenação padrão dos galpões no admin
    ordering = ['id']
    
    # Campos pelos quais é possível buscar galpões
    search_fields = ['nome', 'setor__nome']
    
    # Exibe a contagem completa de resultados na paginação
    show_full_result_count = True


@admin.register(Sala)
class SalaAdmin(admin.ModelAdmin):
    """
    Administração do modelo Sala no Django Admin.
    """

    # Campos que serão exibidos na lista de salas
    list_display = ['numero', 'galpao', 'get_setor']
    
    # Campos que serão links para a página de edição
    list_display_links = ['numero']
    
    # Filtros laterais para facilitar a busca
    list_filter = ['numero', 'galpao', 'galpao__setor']
    
    # Define a paginação para 10 itens por página
    list_per_page = 10
    
    # Ordenação padrão das salas no admin
    ordering = ['id']
    
    # Campos pelos quais é possível buscar salas
    search_fields = ['numero', 'galpao__nome', 'galpao__setor__nome']
    
    # Exibe a contagem completa de resultados na paginação
    show_full_result_count = True

    def get_setor(self, obj):
        """
        Retorna o nome do setor associado ao galpão da sala.

        Args:
            obj (Sala): O objeto Sala.

        Returns:
            str: Nome do setor ou '-' se não houver setor associado.
        """
        return obj.galpao.setor.nome if obj.galpao and obj.galpao.setor else '-'
    
    # Define a descrição da coluna no admin
    get_setor.short_description = 'Setor'


@admin.register(Baia)
class BaiaAdmin(admin.ModelAdmin):
    """
    Administração do modelo Baia no Django Admin.
    """

    # Campos que serão exibidos na lista de baias
    list_display = ['numero', 'sala', 'get_galpao', 'get_setor']
    
    # Campos que serão links para a página de edição
    list_display_links = ['numero']
    
    # Filtros laterais para facilitar a busca
    list_filter = ['numero', 'sala', 'sala__galpao', 'sala__galpao__setor']
    
    # Define a paginação para 10 itens por página
    list_per_page = 10
    
    # Ordenação padrão das baias no admin
    ordering = ['id']
    
    # Campos pelos quais é possível buscar baias
    search_fields = ['numero', 'sala__numero', 'sala__galpao__nome', 'sala__galpao__setor__nome']
    
    # Exibe a contagem completa de resultados na paginação
    show_full_result_count = True

    def get_galpao(self, obj):
        """
        Retorna o nome do galpão associado à sala da baia.

        Args:
            obj (Baia): O objeto Baia.

        Returns:
            str: Nome do galpão ou '-' se não houver galpão associado.
        """
        return obj.sala.galpao.nome if obj.sala and obj.sala.galpao else '-'
    
    def get_setor(self, obj):
        """
        Retorna o nome do setor associado ao galpão da sala da baia.

        Args:
            obj (Baia): O objeto Baia.

        Returns:
            str: Nome do setor ou '-' se não houver setor associado.
        """
        return obj.sala.galpao.setor.nome if obj.sala and obj.sala.galpao and obj.sala.galpao.setor else '-'
    
    # Define a descrição das colunas no admin
    get_galpao.short_description = 'Galpão'
    get_setor.short_description = 'Setor'

 # Animais
    
@admin.register(Especie)
class EspecieAdmin(admin.ModelAdmin):
    """
    Administração do modelo Especie no Django Admin.
    """

    # Campos que serão exibidos na lista de espécies
    list_display = ['nome']
    
    # Campos que serão links para a página de edição
    list_display_links = ['nome']
    
    # Filtros laterais para facilitar a busca
    list_filter = ['nome']
    
    # Define a paginação para 10 itens por página
    list_per_page = 10
    
    # Ordenação padrão das espécies no admin
    ordering = ['id']
    
    # Campos pelos quais é possível buscar espécies
    search_fields = ['nome']
    
    # Exibe a contagem completa de resultados na paginação
    show_full_result_count = True


@admin.register(Raca)
class RacaAdmin(admin.ModelAdmin):
    """
    Administração do modelo Raca no Django Admin.
    """

    # Campos que serão exibidos na lista de raças
    list_display = ['nome']
    
    # Campos que serão links para a página de edição
    list_display_links = ['nome']
    
    # Filtros laterais para facilitar a busca
    list_filter = ['nome']
    
    # Define a paginação para 10 itens por página
    list_per_page = 10
    
    # Ordenação padrão das raças no admin
    ordering = ['id']
    
    # Campos pelos quais é possível buscar raças
    search_fields = ['nome']
    
    # Exibe a contagem completa de resultados na paginação
    show_full_result_count = True


@admin.register(Tipo)
class TipoAdmin(admin.ModelAdmin):
    """
    Administração do modelo Tipo no Django Admin.
    """

    # Campos que serão exibidos na lista de tipos
    list_display = ['nome']
    
    # Campos que serão links para a página de edição
    list_display_links = ['nome']
    
    # Filtros laterais para facilitar a busca
    list_filter = ['nome']
    
    # Define a paginação para 10 itens por página
    list_per_page = 10
    
    # Ordenação padrão dos tipos no admin
    ordering = ['id']
    
    # Campos pelos quais é possível buscar tipos
    search_fields = ['nome']
    
    # Exibe a contagem completa de resultados na paginação
    show_full_result_count = True


@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    """
    Administração do modelo Animal no Django Admin.
    """

    # Campo que permite navegação por data e hora de nascimento no topo
    date_hierarchy = 'data_hora_de_nascimento'
    
    # Campos que serão exibidos na lista de animais
    list_display = [
        'id', 'identificacao_unica', 'rfid', 'especie', 'raca', 'tipo', 'sexo',
        'peso_de_nascimento', 'data_hora_de_nascimento', 'mae', 'pai', 'status',
        'setor', 'observacao'
    ]
    
    # Campos que serão links para a página de edição
    list_display_links = ['identificacao_unica']
    
    # Filtros laterais para facilitar a busca
    list_filter = ['especie', 'raca', 'tipo', 'sexo', 'data_hora_de_nascimento', 'status', 'setor']
    
    # Define a paginação para 10 itens por página
    list_per_page = 10
    
    # Ordenação padrão dos animais no admin
    ordering = ['id']
    
    # Campos pelos quais é possível buscar animais
    search_fields = [
        'identificacao_unica', 'rfid', 'especie__nome', 'raca__nome', 'tipo__nome'
    ]
    
    # Exibe a contagem completa de resultados na paginação
    show_full_result_count = True

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        Define o setor inicial como o setor do usuário logado e desativa o campo de setor na edição.

        Args:
            db_field: Campo do banco de dados.
            request: Objeto de requisição HTTP.
            kwargs: Argumentos adicionais.

        Returns:
            FormField: Campo de formulário personalizado.
        """
        if db_field.name == 'setor':
            kwargs['initial'] = get_setor(request.user)
            kwargs['disabled'] = True

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Suino)
class SuinoAdmin(AnimalAdmin, ImportExportModelAdmin):
    """
    Administração do modelo Suino no Django Admin com funcionalidades de importação/exportação.
    """

    # Define as classes de recursos para importação e exportação
    resource_classes = [SuinoImportResource, SuinoExportResource]


@admin.register(BovinoCorte)
class BovinoCorteAdmin(AnimalAdmin, ImportExportModelAdmin):
    """
    Administração do modelo BovinoCorte no Django Admin com funcionalidades de importação/exportação.
    """

    # Adiciona campos específicos de BovinoCorte à lista de exibição e filtros
    list_display = AnimalAdmin.list_display + ['modo_de_criacao', 'local']
    list_filter = AnimalAdmin.list_filter + ['modo_de_criacao', 'local']
    
    # Define as classes de recursos para importação e exportação
    resource_classes = [BovinoCorteImportResource, BovinoCorteExportResource]


@admin.register(BovinoLeite)
class BovinoLeiteAdmin(AnimalAdmin, ImportExportModelAdmin):
    """
    Administração do modelo BovinoLeite no Django Admin com funcionalidades de importação/exportação.
    """

    # Adiciona campos específicos de BovinoLeite à lista de exibição e filtros
    list_display = AnimalAdmin.list_display + ['nome', 'grau_de_sangue', 'pelagem']
    list_filter = AnimalAdmin.list_filter + ['nome', 'grau_de_sangue', 'pelagem']
    
    # Define as classes de recursos para importação e exportação
    resource_classes = [BovinoLeiteImportResource, BovinoLeiteExportResource]

# Lotes
    
class LoteImportExportModelAdmin(admin.ModelAdmin):
    """
    Classe base para administrar o modelo Lote no Django Admin.
    """
    pass

@admin.register(Lote)
class LoteAdmin(LoteImportExportModelAdmin, ImportExportModelAdmin):
    """
    Administração do modelo Lote no Django Admin com funcionalidades de importação/exportação.
    """

    class AnimalInline(admin.StackedInline):
        """
        Define um inline para adicionar ou editar os animais associados ao lote.
        """

        # Relacionamento através do campo many-to-many `Lote.animais`
        model = Lote.animais.through
        extra = 0  # Não adicionar campos extra

        def formfield_for_foreignkey(self, db_field, request, **kwargs):
            """
            Filtra os animais mostrados no inline para que correspondam ao setor do usuário logado.

            Args:
                db_field: Campo de chave estrangeira.
                request: Objeto de requisição HTTP.
                kwargs: Argumentos adicionais.

            Returns:
                FormField: Campo de formulário filtrado.
            """
            if db_field.name == 'animal':
                # Filtra os animais pelo setor do usuário
                kwargs['queryset'] = Animal.objects.filter(setor=get_setor(request.user))
            return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # Exclui o campo `animais` da visualização direta, pois ele será gerenciado via inline
    exclude = ['animais']
    
    # Adiciona o inline definido acima para gerenciar os animais do lote
    inlines = [AnimalInline]

    # Campos que serão exibidos na lista de lotes
    list_display = ['numero', 'baia', 'get_animais', 'setor']
    
    # Campos que serão links para a página de edição
    list_display_links = ['numero']
    
    # Filtros laterais para facilitar a busca
    list_filter = ['numero', 'baia', 'setor']
    
    # Define a paginação para 10 itens por página
    list_per_page = 10
    
    # Ordenação padrão dos lotes no admin
    ordering = ['id']

    # Define as classes de recursos para importação e exportação
    resource_classes = [LoteImportResource, LoteExportResource]

    # Campos pelos quais é possível buscar lotes
    search_fields = [
        'numero', 'baia__numero', 'baia__sala__numero', 
        'baia__sala__galpao__nome', 'baia__sala__galpao__setor__nome'
    ]
    
    # Exibe a contagem completa de resultados na paginação
    show_full_result_count = True

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        Define o setor inicial como o setor do usuário logado e desativa o campo de setor na edição.

        Args:
            db_field: Campo do banco de dados.
            request: Objeto de requisição HTTP.
            kwargs: Argumentos adicionais.

        Returns:
            FormField: Campo de formulário personalizado.
        """
        if db_field.name == 'setor':
            kwargs['initial'] = get_setor(request.user)
            kwargs['disabled'] = True
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_animais(self, obj):
        """
        Retorna uma lista dos animais associados ao lote em forma de string HTML.

        Args:
            obj: Instância do modelo Lote.

        Returns:
            str: HTML seguro contendo uma lista dos IDs únicos dos animais.
        """
        return mark_safe('<br>'.join([str(animal.identificacao_unica) for animal in obj.animais.all()])) if obj.animais.exists() else '-'
    
    get_animais.short_description = 'Animais'

# Partos

class PartoImportExportModelAdmin(admin.ModelAdmin):
    """
    Classe base para administrar o modelo Parto no Django Admin com funcionalidades de importação/exportação.
    """
    pass

@admin.register(Parto)
class PartoAdmin(PartoImportExportModelAdmin, ImportExportModelAdmin):
    """
    Administração do modelo Parto no Django Admin com funcionalidades de importação/exportação.
    """
    
    class SuinoInline(admin.StackedInline):
        """
        Inline para editar Suínos associados ao parto diretamente na página de edição de Parto.
        """
        model = Suino
        extra = 0  # Não adicionar campos extra
    
    class BovinoCorteInline(admin.StackedInline):
        """
        Inline para editar Bovinos de Corte associados ao parto diretamente na página de edição de Parto.
        """
        model = BovinoCorte
        extra = 0  # Não adicionar campos extra
    
    class BovinoLeiteInline(admin.StackedInline):
        """
        Inline para editar Bovinos de Leite associados ao parto diretamente na página de edição de Parto.
        """
        model = BovinoLeite
        extra = 0  # Não adicionar campos extra

    # Hierarquia de data para facilitar a navegação por datas
    date_hierarchy = 'data_hora_do_parto'
    
    # Campos exibidos na lista de partos
    list_display = [
        'femea', 'macho', 'data_hora_do_parto', 'tipo', 
        'quantidade_de_filhotes_vivos', 'quantidade_de_filhotes_mortos', 
        'quantidade_de_filhotes_mumificados', 'setor', 'observacao'
    ]
    
    # Campos que serão links para a página de edição
    list_display_links = ['femea', 'macho', 'data_hora_do_parto']
    
    # Filtros laterais para facilitar a busca
    list_filter = ['femea', 'macho', 'data_hora_do_parto', 'tipo', 'setor']
    
    # Define a paginação para 10 itens por página
    list_per_page = 10
    
    # Ordenação padrão dos partos no admin
    ordering = ['id']
    
    # Define as classes de recursos para importação e exportação
    resource_classes = [PartoImportResource, PartoExportResource]
    
    # Campos pelos quais é possível buscar partos
    search_fields = ['femea', 'macho', 'data_hora_do_parto', 'tipo', 'setor']
    
    # Exibe a contagem completa de resultados na paginação
    show_full_result_count = True
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        Filtra os campos de chave estrangeira para mostrar apenas animais do setor e sexo apropriados.

        Args:
            db_field: Campo de chave estrangeira.
            request: Objeto de requisição HTTP.
            kwargs: Argumentos adicionais.

        Returns:
            FormField: Campo de formulário filtrado.
        """
        if db_field.name == 'femea':
            kwargs['queryset'] = Animal.objects.filter(sexo='Fêmea', setor=get_setor(request.user))
        elif db_field.name == 'macho':
            kwargs['queryset'] = Animal.objects.filter(sexo='Macho', setor=get_setor(request.user))
        elif db_field.name == 'setor':
            kwargs['initial'] = get_setor(request.user)
            kwargs['disabled'] = True
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def get_formsets_with_inlines(self, request, obj=None):
        """
        Retorna os formsets com inlines apropriados com base no setor do usuário.

        Args:
            request: Objeto de requisição HTTP.
            obj: Instância do modelo (opcional).

        Returns:
            Gerador de formsets e inlines.
        """
        setor = get_setor(request.user)
        inlines = []

        if setor:
            if setor.nome == 'Suinocultura':
                inlines = [self.SuinoInline]
            elif setor.nome == 'Bovinocultura de Corte':
                inlines = [self.BovinoCorteInline]
            elif setor.nome == 'Bovinocultura de Leite':
                inlines = [self.BovinoLeiteInline]

        for inline in inlines:
            yield inline(self.model, self.admin_site).get_formset(request, obj), inline(self.model, self.admin_site)

# Manejos
            
class ManejoImportExportModelAdmin(admin.ModelAdmin):
    """
    Classe base para administrar o modelo Manejo no Django Admin com funcionalidades de importação/exportação.
    """
    pass

@admin.register(Manejo)
class ManejoAdmin(ManejoImportExportModelAdmin, ImportExportModelAdmin):
    """
    Administração do modelo Manejo no Django Admin com funcionalidades de importação/exportação.
    """
    
    class ProcedimentoManejoInline(admin.TabularInline):
        """
        Inline para editar os ProcedimentosManejo associados ao Manejo diretamente na página de edição de Manejo.
        """
        model = ProcedimentoManejo
        extra = 0  # Não adicionar campos extra
    
    class ProdutoManejoInline(admin.TabularInline):
        """
        Inline para editar os ProdutosManejo associados ao Manejo diretamente na página de edição de Manejo.
        """
        model = ProdutoManejo
        extra = 0  # Não adicionar campos extra
    
    # Hierarquia de data para facilitar a navegação por datas
    date_hierarchy = 'data_hora_do_manejo'
    
    # Adiciona os inlines de procedimentos e produtos ao Manejo
    inlines = [ProcedimentoManejoInline, ProdutoManejoInline]
    
    # Campos exibidos na lista de manejos
    list_display = [
        'funcionario', 'data_hora_do_manejo', 'animal', 
        'lote', 'setor', 'observacao'
    ]
    
    # Campos que serão links para a página de edição
    list_display_links = ['funcionario']
    
    # Filtros laterais para facilitar a busca
    list_filter = ['funcionario', 'data_hora_do_manejo', 'animal', 'lote', 'setor']
    
    # Define a paginação para 10 itens por página
    list_per_page = 10
    
    # Ordenação padrão dos manejos no admin
    ordering = ['id']
    
    # Campos pelos quais é possível buscar manejos
    search_fields = ['funcionario']
    
    # Exibe a contagem completa de resultados na paginação
    show_full_result_count = True
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        Filtra os campos de chave estrangeira para mostrar apenas os Animais e Lotes do setor apropriado.

        Args:
            db_field: Campo de chave estrangeira.
            request: Objeto de requisição HTTP.
            kwargs: Argumentos adicionais.

        Returns:
            FormField: Campo de formulário filtrado.
        """
        if db_field.name == 'animal':
            kwargs['queryset'] = Animal.objects.filter(setor=get_setor(request.user))
        elif db_field.name == 'lote':
            kwargs['queryset'] = Lote.objects.filter(setor=get_setor(request.user))
        elif db_field.name == 'setor':
            kwargs['initial'] = get_setor(request.user)
            kwargs['disabled'] = True
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
# Saída
    
class SaidaImportExportModelAdmin(admin.ModelAdmin):
    """
    Classe base para administrar o modelo Saida no Django Admin com funcionalidades de importação/exportação.
    """
    pass

@admin.register(Saida)
class SaidaAdmin(SaidaImportExportModelAdmin, ImportExportModelAdmin):
    """
    Administração do modelo Saida no Django Admin com funcionalidades de importação/exportação.
    """
    
    class AnimalInline(admin.StackedInline):
        """
        Inline para editar os Animais associados à Saida diretamente na página de edição de Saida.
        """
        model = Saida.animais.through
        extra = 0  # Não adicionar campos extra
    
        def formfield_for_foreignkey(self, db_field, request, **kwargs):
            """
            Filtra o campo de chave estrangeira para mostrar apenas os Animais do setor apropriado.

            Args:
                db_field: Campo de chave estrangeira.
                request: Objeto de requisição HTTP.
                kwargs: Argumentos adicionais.

            Returns:
                FormField: Campo de formulário filtrado.
            """
            if db_field.name == 'animal':
                kwargs['queryset'] = Animal.objects.filter(setor=get_setor(request.user))
            return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # Campos a serem excluídos da edição
    exclude = ['animais']
    
    # Adiciona o inline de animais à página de edição de Saida
    inlines = [AnimalInline]
    
    # Hierarquia de data para facilitar a navegação por datas
    date_hierarchy = 'data_hora_da_saida'
    
    # Campos exibidos na lista de saídas
    list_display = [
        'id', 'get_animais', 'data_hora_da_saida', 'tipo', 
        'setor', 'observacao'
    ]
    
    # Campos que serão links para a página de edição
    list_display_links = ['id']
    
    # Filtros laterais para facilitar a busca
    list_filter = ['data_hora_da_saida', 'tipo', 'setor']
    
    # Define a paginação para 10 itens por página
    list_per_page = 10
    
    # Ordenação padrão das saídas no admin
    ordering = ['id']
    
    # Campos pelos quais é possível buscar saídas
    search_fields = ['data_hora_da_saida', 'tipo', 'setor', 'observacao']
    
    # Exibe a contagem completa de resultados na paginação
    show_full_result_count = True
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        Filtra os campos de chave estrangeira para mostrar apenas os Animais e Setores do setor apropriado.

        Args:
            db_field: Campo de chave estrangeira.
            request: Objeto de requisição HTTP.
            kwargs: Argumentos adicionais.

        Returns:
            FormField: Campo de formulário filtrado.
        """
        if db_field.name == 'animal':
            kwargs['queryset'] = Animal.objects.filter(setor=get_setor(request.user))
        elif db_field.name == 'setor':
            kwargs['initial'] = get_setor(request.user)
            kwargs['disabled'] = True
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_animais(self, obj):
        """
        Retorna uma string formatada com as identificações dos Animais associados à Saida.

        Args:
            obj: Instância do modelo Saida.

        Returns:
            str: Identificações dos Animais associados, separadas por quebras de linha.
        """
        return mark_safe('<br>'.join([str(animal.identificacao_unica) for animal in obj.animais.all()])) if obj.animais.exists() else '-'
    
    get_animais.short_description = 'Animais'
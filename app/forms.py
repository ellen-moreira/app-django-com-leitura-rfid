from app.models import *
from django import forms
from django.forms import BaseInlineFormSet, inlineformset_factory

# Formulário base para todos os animais, herdando de ModelForm
class AnimalForm(forms.ModelForm):
    """
    Este formulário base utiliza o ModelForm para criar campos a partir do modelo Animal.
    Ele inclui campos básicos comuns a todos os tipos de animais registrados no sistema.
    """
    class Meta:
        model = Animal # Define o modelo associado ao formulário
        fields = ['id', 'identificacao_unica', 'rfid', 'especie', 'raca', 'tipo', 'sexo', 'peso_de_nascimento', 'data_hora_de_nascimento', 'mae', 'pai', 'parto', 'status', 'setor', 'observacao'] # Campos incluídos no formulário

# Formulário específico para o registro de Suínos, herdando do formulário base AnimalForm
class SuinoForm(AnimalForm):
    """
    Formulário específico para a modelagem de suínos.
    Este formulário herda do AnimalForm e exclui campos não relevantes para suínos.
    """
    class Meta:
        model = Suino # Define o modelo Suino associado ao formulário
        fields = AnimalForm.Meta.fields # Herda todos os campos do AnimalForm
        exclude = ['rfid', 'especie', 'raca', 'tipo', 'data_hora_de_nascimento', 'mae', 'pai', 'parto', 'setor', 'observacao'] # Campos excluídos por não serem aplicáveis aos suínos

# Formulário para o registro de Bovinos de Corte, herdando do formulário base AnimalForm
class BovinoCorteForm(AnimalForm):
    """
    Formulário específico para a modelagem de bovinos de corte.
    Adiciona campos específicos como modo_de_criacao e exclui campos irrelevantes.
    """
    class Meta:
        model = BovinoCorte  # Define o modelo BovinoCorte associado ao formulário
        fields = AnimalForm.Meta.fields + ['modo_de_criacao']  # Inclui campo específico modo_de_criacao
        exclude = ['rfid', 'especie', 'raca', 'tipo', 'data_hora_de_nascimento', 'mae', 'pai', 'parto', 'setor', 'observacao'] # Exclui campos não relevantes para bovinos de corte

# Formulário para o registro de Bovinos de Leite, herdando do formulário base AnimalForm
class BovinoLeiteForm(AnimalForm):
    """
    Formulário específico para a modelagem de bovinos de leite.
    Adiciona campos como nome, grau_de_sangue, e pelagem, e exclui campos irrelevantes.
    """
    class Meta:
        model = BovinoLeite  # Define o modelo BovinoLeite associado ao formulário
        fields = AnimalForm.Meta.fields + ['nome', 'grau_de_sangue', 'pelagem']  # Inclui campos específicos
        exclude = ['rfid', 'especie', 'raca', 'tipo', 'data_hora_de_nascimento', 'mae', 'pai', 'parto', 'setor', 'observacao'] # Exclui campos não aplicáveis a bovinos de leite

# Formulário para o registro de Lotes, herdando de ModelForm
class LoteForm(forms.ModelForm):
    """
    Este formulário gerencia os lotes de animais.
    Utiliza o ModelForm para gerar os campos com base no modelo Lote.
    """
    class Meta:
        model = Lote  # Define o modelo Lote associado ao formulário
        fields = '__all__'  # Inclui todos os campos do modelo
        widgets = {
            'observacao': forms.Textarea(attrs={'rows': 5}),  # Personaliza o campo observacao como um Textarea com 5 linhas
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Extrai o usuário dos argumentos passados

        super().__init__(*args, **kwargs)  # Inicializa o formulário

        if user:
            setor = user.setor_usuarios.first()  # Obtém o primeiro setor associado ao usuário

            if setor:
                # Filtra os animais do lote pelo setor do usuário
                self.fields['animais'].queryset = Animal.objects.filter(setor=setor)

# Formulário para o registro de Partos, herdando de ModelForm
class PartoForm(forms.ModelForm):
    """
    Este formulário gerencia os registros de partos.
    Inclui personalização do campo data_hora_do_parto com um widget de seleção de data e hora.
    """
    data_hora_do_parto = forms.DateTimeField(
        widget=forms.TextInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M:%S']  # Define o formato de entrada para data e hora
    )

    class Meta:
        model = Parto  # Define o modelo Parto associado ao formulário
        fields = '__all__'  # Inclui todos os campos do modelo
        widgets = {
            'observacao': forms.Textarea(attrs={'rows': 5}),  # Personaliza o campo observacao como um Textarea com 5 linhas
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Extrai o usuário dos argumentos passados

        super().__init__(*args, **kwargs)  # Inicializa o formulário

        if user:
            setor = user.setor_usuarios.first()  # Obtém o primeiro setor associado ao usuário

            if setor:
                # Filtra a fêmea e o macho do parto pelo setor do usuário e pelo sexo
                self.fields['femea'].queryset = Animal.objects.filter(setor=setor, sexo='Fêmea')
                self.fields['macho'].queryset = Animal.objects.filter(setor=setor, sexo='Macho')

# Formulário para o registro de Manejos, herdando de ModelForm
class ManejoForm(forms.ModelForm):
    """
    Este formulário gerencia os registros de manejos.
    Inclui personalização do campo data_hora_do_manejo com um widget de seleção de data e hora.
    """
    data_hora_do_manejo = forms.DateTimeField(
        widget=forms.TextInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M:%S']  # Define o formato de entrada para data e hora
    )

    class Meta:
        model = Manejo  # Define o modelo Manejo associado ao formulário
        fields = '__all__'  # Inclui todos os campos do modelo
        widgets = {
            'observacao': forms.Textarea(attrs={'rows': 5}),  # Personaliza o campo observacao como um Textarea com 5 linhas
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Extrai o usuário dos argumentos passados

        super().__init__(*args, **kwargs)  # Inicializa o formulário

        if user:
            setor = user.setor_usuarios.first()  # Obtém o primeiro setor associado ao usuário

            if setor:
                # Filtra os animais do manejo pelo setor do usuário
                self.fields['animal'].queryset = Animal.objects.filter(setor=setor)

                if setor.nome != 'Suinocultura':
                    # Desabilita o campo lote se o setor não for Suinocultura
                    self.fields['lote'].widget.attrs['disabled'] = 'disabled'
                else:
                    # Filtra os lotes pelo setor do usuário
                    self.fields['lote'].queryset = Lote.objects.filter(setor=setor)

# Formulário para Procedimentos de Manejo, herdando de ModelForm
class ProcedimentoManejoForm(forms.ModelForm):
    """
    Este formulário gerencia os procedimentos de manejo.
    Utiliza o ModelForm para gerar os campos com base no modelo ProcedimentoManejo.
    """
    class Meta:
        model = ProcedimentoManejo  # Define o modelo ProcedimentoManejo associado ao formulário
        fields = '__all__'  # Inclui todos os campos do modelo

# Formulário para Produtos de Manejo, herdando de ModelForm
class ProdutoManejoForm(forms.ModelForm):
    """
    Este formulário gerencia os produtos utilizados no manejo.
    Utiliza o ModelForm para gerar os campos com base no modelo ProdutoManejo.
    """
    class Meta:
        model = ProdutoManejo  # Define o modelo ProdutoManejo associado ao formulário
        fields = '__all__'  # Inclui todos os campos do modelo

# Formulário para o registro de Saídas, herdando de ModelForm
class SaidaForm(forms.ModelForm):
    """
    Este formulário gerencia os registros de saídas de animais.
    Ele utiliza o ModelForm para criar campos baseados no modelo Saida e personaliza 
    os widgets de data e hora e observações.
    """
    class Meta:
        model = Saida  # Define o modelo Saida associado ao formulário
        fields = '__all__'  # Inclui todos os campos do modelo
        widgets = {
            'data_hora_da_saida': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            # Personaliza o campo data_hora_da_saida com um widget de seleção de data e hora
            'observacao': forms.Textarea(attrs={'rows': 5}),  # Personaliza o campo observacao como um Textarea com 5 linhas
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Extrai o usuário dos argumentos passados

        super().__init__(*args, **kwargs)  # Inicializa o formulário

        if user:
            setor = user.setor_usuarios.first()  # Obtém o primeiro setor associado ao usuário

            if setor:
                # Filtra os animais disponíveis para saída pelo setor do usuário
                self.fields['animais'].queryset = Animal.objects.filter(setor=setor)

# Classe base customizada para InlineFormSet
class CustomBaseInlineFormSet(BaseInlineFormSet):
    """
    Esta classe personaliza o comportamento padrão de BaseInlineFormSet.
    Ela define que os formulários vazios não são permitidos, garantindo que todos 
    os formulários preenchidos sejam validados.
    """
    def __init__(self, *args, **kwargs):
        super(CustomBaseInlineFormSet, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False  # Nenhum formulário vazio é permitido

# Função para criar um formset inline customizado
def custom_formset_factory(parent_model, model, form, formset=BaseInlineFormSet, **kwargs):
    """
    Função que cria um formset inline customizado, ocultando o campo DELETE nos formulários.
    
    :param parent_model: Modelo pai associado ao formset
    :param model: Modelo associado ao formset
    :param form: Formulário base utilizado no formset
    :param formset: Classe base para o formset, padrão BaseInlineFormSet
    :param kwargs: Argumentos adicionais para inlineformset_factory
    :return: Classe CustomFormSet personalizada
    """
    FormSet = inlineformset_factory(parent_model, model, form=form, formset=formset, **kwargs)

    class CustomFormSet(FormSet):
        def add_fields(self, form, index):
            """
            Método para adicionar campos ao formulário, incluindo a customização do campo DELETE.
            """
            super().add_fields(form, index)
            form.fields['DELETE'].widget = forms.HiddenInput()  # Oculta o campo DELETE

    return CustomFormSet

# FormSet customizado para LoteAnimal, herdando de CustomBaseInlineFormSet
class CustomLoteAnimalFormSet(CustomBaseInlineFormSet):
    """
    Este formset customizado é utilizado para gerenciar os animais associados a um lote.
    Filtra os animais disponíveis para o usuário atual com base no setor ao qual ele pertence.
    """
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Extrai o usuário dos argumentos passados
        super().__init__(*args, **kwargs)

        if self.user:
            setor = self.user.setor_usuarios.first()  # Obtém o primeiro setor associado ao usuário
            for form in self.forms:
                if setor:
                    # Filtra os animais pelo setor do usuário
                    form.fields['animal'].queryset = Animal.objects.filter(setor=setor)
                else:
                    form.fields['animal'].queryset = Animal.objects.none()  # Nenhum animal se o setor for None

# FormSet customizado para SaidaAnimal, herdando de CustomBaseInlineFormSet
class CustomSaidaAnimalFormSet(CustomBaseInlineFormSet):
    """
    Este formset customizado é utilizado para gerenciar os animais associados a uma saída.
    Filtra os animais disponíveis para o usuário atual com base no setor ao qual ele pertence.
    """
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Extrai o usuário dos argumentos passados
        super().__init__(*args, **kwargs)

        if self.user:
            setor = self.user.setor_usuarios.first()  # Obtém o primeiro setor associado ao usuário
            for form in self.forms:
                if setor:
                    # Filtra os animais pelo setor do usuário
                    form.fields['animal'].queryset = Animal.objects.filter(setor=setor)
                else:
                    form.fields['animal'].queryset = Animal.objects.none()  # Nenhum animal se o setor for None

# FormSet para cadastrar animais em um lote, permitindo a adição de 1 novo animal
CadastrarLoteAnimalFormSet = custom_formset_factory(
    Lote,
    Lote.animais.through,
    form=LoteForm,
    extra=1,  # Permite adicionar 1 animal extra
    can_delete=True,  # Permite deletar animais do lote
    can_delete_extra=True,
    formset=CustomLoteAnimalFormSet
)

# FormSet para atualizar os animais de um lote existente, sem adicionar novos por padrão
AtualizarLoteAnimalFormSet = custom_formset_factory(
    Lote,
    Lote.animais.through,
    form=LoteForm,
    extra=0,  # Não adiciona novos animais por padrão
    can_delete=True,  # Permite deletar animais do lote
    can_delete_extra=True,
    formset=CustomLoteAnimalFormSet
)

# FormSet para cadastrar suínos em um parto, permitindo a adição de 1 novo suíno
CadastrarPartoSuinoFormSet = custom_formset_factory(
    Parto,
    Suino,
    form=SuinoForm,
    extra=1,  # Permite adicionar 1 suíno extra
    can_delete=True,  # Permite deletar suínos do parto
    can_delete_extra=True,
    formset=CustomBaseInlineFormSet
)

# FormSet para atualizar suínos em um parto existente, sem adicionar novos por padrão
AtualizarPartoSuinoFormSet = custom_formset_factory(
    Parto,
    Suino,
    form=SuinoForm,
    extra=0,  # Não adiciona novos suínos por padrão
    can_delete=True,  # Permite deletar suínos do parto
    can_delete_extra=True,
    formset=CustomBaseInlineFormSet
)

# FormSet para cadastrar bovinos de corte em um parto, permitindo a adição de 1 novo bovino
CadastrarPartoBovinoCorteFormSet = custom_formset_factory(
    Parto,
    BovinoCorte,
    form=BovinoCorteForm,
    extra=1,  # Permite adicionar 1 bovino de corte extra
    can_delete=True,  # Permite deletar bovinos do parto
    can_delete_extra=True,
    formset=CustomBaseInlineFormSet
)

# FormSet para atualizar bovinos de corte em um parto existente, sem adicionar novos por padrão
AtualizarPartoBovinoCorteFormSet = custom_formset_factory(
    Parto,
    BovinoCorte,
    form=BovinoCorteForm,
    extra=0,  # Não adiciona novos bovinos de corte por padrão
    can_delete=True,  # Permite deletar bovinos do parto
    can_delete_extra=True,
    formset=CustomBaseInlineFormSet
)

# FormSet para cadastrar bovinos de leite em um parto, permitindo a adição de 1 novo bovino
CadastrarPartoBovinoLeiteFormSet = custom_formset_factory(
    Parto,
    BovinoLeite,
    form=BovinoLeiteForm,
    extra=1,  # Permite adicionar 1 bovino de leite extra
    can_delete=True,  # Permite deletar bovinos do parto
    can_delete_extra=True,
    formset=CustomBaseInlineFormSet
)

# FormSet para atualizar bovinos de leite em um parto existente, sem adicionar novos por padrão
AtualizarPartoBovinoLeiteFormSet = custom_formset_factory(
    Parto,
    BovinoLeite,
    form=BovinoLeiteForm,
    extra=0,  # Não adiciona novos bovinos de leite por padrão
    can_delete=True,  # Permite deletar bovinos do parto
    can_delete_extra=True,
    formset=CustomBaseInlineFormSet
)

# FormSet para cadastrar procedimentos de manejo, permitindo a adição de 1 novo procedimento
CadastrarProcedimentoManejoFormSet = custom_formset_factory(
    Manejo,
    ProcedimentoManejo,
    form=ProcedimentoManejoForm,
    extra=1,  # Permite adicionar 1 procedimento extra
    can_delete=True,  # Permite deletar procedimentos
    can_delete_extra=True,
    formset=CustomBaseInlineFormSet
)

# FormSet para atualizar procedimentos de manejo existentes, sem adicionar novos por padrão
AtualizarProcedimentoManejoFormSet = custom_formset_factory(
    Manejo,
    ProcedimentoManejo,
    form=ProcedimentoManejoForm,
    extra=0,  # Não adiciona novos procedimentos por padrão
    can_delete=True,  # Permite deletar procedimentos
    can_delete_extra=True,
    formset=CustomBaseInlineFormSet
)

# FormSet para cadastrar produtos de manejo, permitindo a adição de 1 novo produto
CadastrarProdutoManejoFormSet = custom_formset_factory(
    Manejo,
    ProdutoManejo,
    form=ProdutoManejoForm,
    extra=1,  # Permite adicionar 1 produto extra
    can_delete=True,  # Permite deletar produtos
    can_delete_extra=True,
    formset=CustomBaseInlineFormSet
)

# FormSet para atualizar produtos de manejo existentes, sem adicionar novos por padrão
AtualizarProdutoManejoFormSet = custom_formset_factory(
    Manejo,
    ProdutoManejo,
    form=ProdutoManejoForm,
    extra=0,  # Não adiciona novos produtos por padrão
    can_delete=True,  # Permite deletar produtos
    can_delete_extra=True,
    formset=CustomBaseInlineFormSet
)

# FormSet para cadastrar animais em uma saída, permitindo a adição de 1 novo animal
CadastrarSaidaFormSet = custom_formset_factory(
    Saida,
    Saida.animais.through,
    form=SaidaForm,
    extra=1,  # Permite adicionar 1 animal extra
    can_delete=True,  # Permite deletar animais da saída
    can_delete_extra=True,
    formset=CustomSaidaAnimalFormSet
)

# FormSet para atualizar animais em uma saída existente, sem adicionar novos por padrão
AtualizarSaidaFormSet = custom_formset_factory(
    Saida,
    Saida.animais.through,
    form=SaidaForm,
    extra=0,  # Não adiciona novos animais por padrão
    can_delete=True,  # Permite deletar animais da saída
    can_delete_extra=True,
    formset=CustomSaidaAnimalFormSet
)
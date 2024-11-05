from .models import *
from django.contrib.auth.models import User
from django import forms
from django.forms import BaseInlineFormSet, inlineformset_factory

# Form

class AnimalForm(forms.ModelForm):
	class Meta:
		model = Animal
		fields = ['identificacao_unica', 'rfid', 'especie', 'raca', 'tipo', 'sexo', 'peso_nascimento', 'data_hora_nascimento', 'mae', 'pai', 'setor']

class SuinoForm(AnimalForm):
	class Meta:
		model = Suino
		fields = AnimalForm.Meta.fields
		exclude = ['rfid', 'especie', 'raca', 'tipo', 'data_hora_nascimento', 'mae', 'pai', 'parto', 'setor']

class BovinoCorteForm(AnimalForm):
	class Meta:
		model = BovinoCorte
		fields = AnimalForm.Meta.fields + ['modo_criacao']
		exclude = ['rfid', 'especie', 'raca', 'tipo', 'data_hora_nascimento', 'mae', 'pai', 'parto', 'setor']

class BovinoLeiteForm(AnimalForm):
	class Meta:
		model = BovinoLeite
		fields = AnimalForm.Meta.fields + ['nome', 'grau_sangue', 'pelagem']
		exclude = ['rfid', 'especie', 'raca', 'tipo', 'data_hora_nascimento', 'mae', 'pai', 'parto', 'setor']

class LoteForm(forms.ModelForm):
	class Meta:
		model = Lote
		fields = '__all__'
		exclude = ['animais', 'setor']
		
	def __init__(self, *args, **kwargs):
		user = kwargs.pop('user', None)
		super().__init__(*args, **kwargs)

		if user:
			setor_usuario = user.setor.first()

			if setor_usuario:
				self.fields['animais'].queryset = Animal.objects.filter(setor=setor_usuario)

class PartoForm(forms.ModelForm):
	data_hora_parto = forms.DateTimeField(widget=forms.TextInput(attrs={'type': 'datetime-local'}), input_formats=['%Y-%m-%dT%H:%M:%S'])

	class Meta:
		model = Parto
		fields = '__all__'

	def __init__(self, *args, **kwargs):
		user = kwargs.pop('user', None)
		super().__init__(*args, **kwargs)

		if user:
			setor_usuario = user.setor.first()

			if setor_usuario:
				self.fields['femea'].queryset = Animal.objects.filter(sexo='Fêmea', setor=setor_usuario)
				self.fields['macho'].queryset = Animal.objects.filter(sexo='Macho', setor=setor_usuario)

class ManejoForm(forms.ModelForm):
	data_hora_manejo = forms.DateTimeField(widget=forms.TextInput(attrs={'type': 'datetime-local'}), input_formats=['%Y-%m-%dT%H:%M:%S'])

	class Meta:
		model = ManejoPecuaria
		fields = '__all__'

	def __init__(self, *args, **kwargs):
		user = kwargs.pop('user', None)
		super().__init__(*args, **kwargs)

		if user:
			setor_usuario = user.setor.first()
			print(setor_usuario)

			if setor_usuario:
				self.fields['animal'].queryset = Animal.objects.filter(setor=setor_usuario)
				# Adicione o atributo disabled ao campo lote se o usuário não for do setor 'Suínocultura'
				if setor_usuario.nome != 'Suínocultura':
					self.fields['lote'].widget.attrs['disabled'] = 'disabled'
				else:
					self.fields['lote'].queryset = Lote.objects.filter(setor=setor_usuario)

class ProcedimentoManejoForm(forms.ModelForm):
	class Meta:
		model = ProcedimentoManejo
		fields = '__all__'

class ProdutoManejoForm(forms.ModelForm):
	class Meta:
		model = ProdutoManejo
		fields = '__all__'
		
class SaidaForm(forms.ModelForm):
	data_hora_saida = forms.DateTimeField(widget=forms.TextInput(attrs={'type': 'datetime-local'}), input_formats=['%Y-%m-%dT%H:%M:%S'])

	class Meta:
		model = Saida
		fields = '__all__'
		widgets = {
			'setor': forms.Select(attrs={'disabled': 'disabled'}),
			'observacao': forms.Textarea(attrs={'rows': 5}),
		}

	def __init__(self, *args, **kwargs):
		user = kwargs.pop('user', None)
		super().__init__(*args, **kwargs)

		if user:
			setor_usuario = user.setor.first()

			if setor_usuario:
				self.fields['animal'].queryset = Animal.objects.filter(setor=setor_usuario)

# Inline formset

class CustomBaseInlineFormSet(BaseInlineFormSet):
	def __init__(self, *args, **kwargs):
		super(CustomBaseInlineFormSet, self).__init__(*args, **kwargs)
		for form in self.forms:
			form.empty_permitted = False

def custom_formset_factory(parent_model, model, form, formset=BaseInlineFormSet, **kwargs):
	FormSet = inlineformset_factory(parent_model, model, form=form, formset=formset, **kwargs)

	class CustomFormSet(FormSet):
		def add_fields(self, form, index):
			super().add_fields(form, index)
			form.fields['DELETE'].widget = forms.HiddenInput()

	return CustomFormSet

class CustomLoteAnimalFormSet(CustomBaseInlineFormSet):
	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user', None)
		super().__init__(*args, **kwargs)
		
		if self.user:
			setor_usuario = self.user.setor.first()
			for form in self.forms:
				if setor_usuario:
					form.fields['animal'].queryset = Animal.objects.filter(setor=setor_usuario) # .exclude(id__in=Lote.animais.through.objects.values_list('animal_id', flat=True))
				else:
					form.fields['animal'].queryset = Animal.objects.none()


AdicionarLoteAnimalFormSet = custom_formset_factory(
	Lote,
	Lote.animais.through,
	form=LoteForm,
	extra=1,
	can_delete=True,
	can_delete_extra=True,
	formset=CustomLoteAnimalFormSet
)

EditarLoteAnimalFormSet = custom_formset_factory(
	Lote,
	Lote.animais.through,
	form=LoteForm,
	extra=0,
	can_delete=True,
	can_delete_extra=True,
	formset=CustomLoteAnimalFormSet
)

AdicionarPartoSuinoFormSet = custom_formset_factory(
	Parto,
	Suino,
	form=SuinoForm,
	extra=1,
	can_delete=True,
	can_delete_extra=True,
	formset=CustomBaseInlineFormSet
)

EditarPartoSuinoFormSet = custom_formset_factory(
	Parto,
	Suino,
	form=SuinoForm,
	extra=0,
	can_delete=True,
	can_delete_extra=True,
	formset=CustomBaseInlineFormSet
)

AdicionarPartoBovinoCorteFormSet = custom_formset_factory(
	Parto,
	BovinoCorte,
	form=BovinoCorteForm,
	extra=1,
	can_delete=True,
	can_delete_extra=True,
	formset=CustomBaseInlineFormSet
)

EditarPartoBovinoCorteFormSet = custom_formset_factory(
	Parto,
	BovinoCorte,
	form=BovinoCorteForm,
	extra=0,
	can_delete=True,
	can_delete_extra=True,
	formset=CustomBaseInlineFormSet
)

AdicionarPartoBovinoLeiteFormSet = custom_formset_factory(
	Parto,
	BovinoLeite,
	form=BovinoLeiteForm,
	extra=1,
	can_delete=True,
	can_delete_extra=True,
	formset=CustomBaseInlineFormSet
)

EditarPartoBovinoLeiteFormSet = custom_formset_factory(
	Parto,
	BovinoLeite,
	form=BovinoLeiteForm,
	extra=0,
	can_delete=True,
	can_delete_extra=True,
	formset=CustomBaseInlineFormSet
)

AdicionarProcedimentoManejoFormSet = custom_formset_factory(
	ManejoPecuaria,
	ProcedimentoManejo,
	form=ProcedimentoManejoForm,
	extra=1,
	can_delete=True,
	can_delete_extra=True,
	formset=CustomBaseInlineFormSet
)

EditarProcedimentoManejoFormSet = custom_formset_factory(
	ManejoPecuaria,
	ProcedimentoManejo,
	form=ProcedimentoManejoForm,
	extra=0,
	can_delete=True,
	can_delete_extra=True,
	formset=CustomBaseInlineFormSet
)

AdicionarProdutoManejoFormSet = custom_formset_factory(
	ManejoPecuaria,
	ProdutoManejo,
	form=ProdutoManejoForm,
	extra=1,
	can_delete=True,
	can_delete_extra=True,
	formset=CustomBaseInlineFormSet
)

EditarProdutoManejoFormSet = custom_formset_factory(
	ManejoPecuaria,
	ProdutoManejo,
	form=ProdutoManejoForm,
	extra=0,
	can_delete=True,
	can_delete_extra=True,
	formset=CustomBaseInlineFormSet
)
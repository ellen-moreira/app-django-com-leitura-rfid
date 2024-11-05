from .models import *
from django.contrib import admin
from django.utils.safestring import mark_safe
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget

# Register your models here.

# Funções Auxiliares

def get_user_setor(user):
        return SetorPecuaria.objects.filter(usuarios=user).first()

# Importação e Exportação

class SuinoImportResource(resources.ModelResource):
    tipo = fields.Field(
        column_name='tipo',
        attribute='tipo',
        widget=ForeignKeyWidget(Tipo, 'nome')
    )

    def before_import_row(self, row, **kwargs):
        row['identificacao_unica'] = str(int(row['identificacao_unica'])) if isinstance(row['identificacao_unica'], float) else row['identificacao_unica']
        Tipo.objects.get_or_create(nome=row['tipo'], defaults={'nome': row['tipo']})

    class Meta:
        model = Suino
        fields = ['id', 'identificacao_unica', 'tipo', 'sexo']
        import_order = ['id', 'identificacao_unica', 'tipo', 'sexo']

class SuinoExportResource(resources.ModelResource):
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
        widget=ForeignKeyWidget(SetorPecuaria, 'nome')
    )

    class Meta:
        model = Suino
        fields = ['id', 'identificacao_unica', 'rfid', 'especie', 'raca', 'tipo', 'sexo', 'peso_nascimento', 'data_hora_nascimento', 'mae', 'pai', 'observacao', 'setor']
        export_order = ['id', 'identificacao_unica', 'rfid', 'especie', 'raca', 'tipo', 'sexo', 'peso_nascimento', 'data_hora_nascimento', 'mae', 'pai', 'observacao', 'setor']

class BovinoCorteImportResource(resources.ModelResource):
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
        row['identificacao_unica'] = str(int(row['identificacao_unica'])) if isinstance(row['identificacao_unica'], float) else str(row['identificacao_unica'])
        Raca.objects.get_or_create(nome=row['raca'], defaults={'nome': row['raca']})
        Tipo.objects.get_or_create(nome=row['tipo'], defaults={'nome': row['tipo']})

    class Meta:
        model = BovinoCorte
        fields = ['id', 'identificacao_unica', 'raca', 'tipo', 'sexo', 'data_hora_nascimento', 'observacao', 'modo_criacao', 'local']
        import_order = ['id', 'identificacao_unica', 'raca', 'tipo', 'sexo', 'data_hora_nascimento', 'observacao', 'modo_criacao', 'local']

class BovinoCorteExportResource(resources.ModelResource):
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
        widget=ForeignKeyWidget(SetorPecuaria, 'nome')
    )

    class Meta:
        model = BovinoCorte
        fields = ['id', 'identificacao_unica', 'rfid', 'especie', 'raca', 'tipo', 'sexo', 'peso_nascimento', 'data_hora_nascimento', 'mae', 'pai', 'modo_criacao', 'local', 'observacao', 'setor']
        export_order = ['id', 'identificacao_unica', 'rfid', 'especie', 'raca', 'tipo', 'sexo', 'peso_nascimento', 'data_hora_nascimento', 'mae', 'pai', 'modo_criacao', 'local', 'observacao', 'setor']

class BovinoLeiteImportResource(resources.ModelResource):
    raca = fields.Field(
        column_name='raca',
        attribute='raca',
        widget=ForeignKeyWidget(Raca, 'nome')
    )

    def before_import_row(self, row, **kwargs):
        row['identificacao_unica'] = str(int(row['identificacao_unica'])) if isinstance(row['identificacao_unica'], float) else str(row['identificacao_unica'])
        Raca.objects.get_or_create(nome=row['raca'], defaults={'nome': row['raca']})

    class Meta:
        model = BovinoLeite
        fields = ['id', 'identificacao_unica', 'raca', 'sexo', 'data_hora_nascimento', 'observacao', 'nome', 'grau_sangue', 'pelagem']
        import_order = ['id', 'identificacao_unica', 'raca', 'sexo', 'data_hora_nascimento', 'observacao', 'nome', 'grau_sangue', 'pelagem']

class BovinoLeiteExportResource(resources.ModelResource):
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

    setor = fields.Field(
        column_name='setor',
        attribute='setor',
        widget=ForeignKeyWidget(SetorPecuaria, 'nome')
    )

    class Meta:
        model = BovinoLeite
        fields = ['id', 'identificacao_unica', 'rfid', 'especie', 'raca', 'sexo', 'peso_nascimento', 'data_hora_nascimento', 'mae', 'pai', 'observacao', 'nome', 'grau_sangue', 'pelagem', 'setor']
        export_order = ['id', 'identificacao_unica', 'rfid', 'especie', 'raca', 'sexo', 'peso_nascimento', 'data_hora_nascimento', 'mae', 'pai', 'observacao', 'nome', 'grau_sangue', 'pelagem', 'setor']

class LoteImportResource(resources.ModelResource):
    baia = fields.Field(
        column_name='baia',
        attribute='baia',
        widget=ForeignKeyWidget(Baia, 'numero')
    )

    setor = fields.Field(
        column_name='setor',
        attribute='setor',
        widget=ForeignKeyWidget(SetorPecuaria, 'nome')
    )

    def before_import_row(self, row, **kwargs):
        Baia.objects.get_or_create(numero=row['baia'], defaults={'numero': row['baia']})
        SetorPecuaria.objects.get_or_create(nome=row['setor'], defaults={'nome': row['setor']})

    class Meta:
        model = Lote
        fields = ['id', 'numero', 'baia', 'setor']
        import_order = ['id', 'numero', 'baia', 'setor']

class LoteExportResource(resources.ModelResource):
    baia = fields.Field(
        column_name='baia',
        attribute='baia',
        widget=ForeignKeyWidget(Baia, 'numero')
    )

    setor = fields.Field(
        column_name='setor',
        attribute='setor',
        widget=ForeignKeyWidget(SetorPecuaria, 'nome')
    )

    class Meta:
        model = Lote
        fields = ['id', 'numero', 'baia', 'setor']
        export_order = ['id', 'numero', 'baia', 'setor']

class PartoImportResource(resources.ModelResource):
    setor = fields.Field(
        column_name='setor',
        attribute='setor',
        widget=ForeignKeyWidget(SetorPecuaria, 'nome')
    )

    def before_import_row(self, row, **kwargs):
        SetorPecuaria.objects.get_or_create(nome=row['setor'], defaults={'nome': row['setor']})

    class Meta:
        model = Parto
        fields = ['id', 'femea', 'macho', 'data_hora_parto', 'tipo', 'setor', 'quantidade_filhotes_vivos', 'quantidade_filhotes_mortos', 'quantidade_filhotes_mumificados']
        import_order = ['id', 'femea', 'macho', 'data_hora_parto', 'tipo', 'setor', 'quantidade_filhotes_vivos', 'quantidade_filhotes_mortos', 'quantidade_filhotes_mumificados']

class PartoExportResource(resources.ModelResource):
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
        widget=ForeignKeyWidget(SetorPecuaria, 'nome')
    )

    class Meta:
        model = Parto
        fields = ['id', 'femea', 'macho', 'data_hora_parto', 'tipo', 'setor', 'quantidade_filhotes_vivos', 'quantidade_filhotes_mortos', 'quantidade_filhotes_mumificados']
        export_order = ['id', 'femea', 'macho', 'data_hora_parto', 'tipo', 'setor', 'quantidade_filhotes_vivos', 'quantidade_filhotes_mortos', 'quantidade_filhotes_mumificados']

class ManejoPecuariaImportResource(resources.ModelResource):
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
        widget=ForeignKeyWidget(SetorPecuaria, 'nome')
    )

    def before_import_row(self, row, **kwargs):
        Funcionario.objects.get_or_create(nome=row['funcionario'], defaults={'nome': row['funcionario']})
        SetorPecuaria.objects.get_or_create(nome=row['setor'], defaults={'nome': row['setor']})

    class Meta:
        model = ManejoPecuaria
        fields = ['id', 'funcionario', 'observacao', 'animal', 'lote', 'data_hora_manejo', 'setor']
        import_order = ['id', 'funcionario', 'observacao', 'animal', 'lote', 'data_hora_manejo', 'setor']

class ManejoPecuariaExportResource(resources.ModelResource):
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
        widget=ForeignKeyWidget(SetorPecuaria, 'nome')
    )

    class Meta:
        model = ManejoPecuaria
        fields = ['id', 'funcionario', 'observacao', 'animal', 'lote', 'data_hora_manejo', 'setor']
        export_order = ['id', 'funcionario', 'observacao', 'animal', 'lote', 'data_hora_manejo', 'setor']

# Locais

class SetorPecuariaAdmin(admin.ModelAdmin):
    filter_horizontal = ['usuarios']
    list_display = ['nome', 'get_usuarios']
    list_display_links = ['nome']
    list_filter = ['nome', 'usuarios']
    list_per_page = 10
    ordering = ['id']
    search_fields = ['nome', 'usuarios__username']
    show_full_result_count = True

    def get_usuarios(self, obj):
        return mark_safe('<br>'.join([usuario.username for usuario in obj.usuarios.all()]))
    
    get_usuarios.short_description = 'Usuários'

class GalpaoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'setor']
    list_display_links = ['nome']
    list_filter = ['nome', 'setor']
    list_per_page = 10
    ordering = ['id']
    search_fields = ['nome', 'setor__nome']
    show_full_result_count = True

class SalaAdmin(admin.ModelAdmin):
    list_display = ['numero', 'galpao', 'get_setor']
    list_display_links = ['numero']
    list_filter = ['numero', 'galpao', 'galpao__setor']
    list_per_page = 10
    ordering = ['id']
    search_fields = ['numero', 'galpao__nome', 'galpao__setor__nome']
    show_full_result_count = True

    def get_setor(self, obj):
        return obj.galpao.setor.nome if obj.galpao and obj.galpao.setor else '-'
    
    get_setor.short_description = 'Setor'

class BaiaAdmin(admin.ModelAdmin):
    list_display = ['numero', 'sala', 'get_galpao', 'get_setor']
    list_display_links = ['numero']
    list_filter = ['numero', 'sala', 'sala__galpao', 'sala__galpao__setor']
    list_per_page = 10
    ordering = ['id']
    search_fields = ['numero', 'sala__numero', 'sala__galpao__nome', 'sala__galpao__setor__nome']
    show_full_result_count = True

    def get_galpao(self, obj):
        return obj.sala.galpao.nome if obj.sala and obj.sala.galpao else '-'
    
    def get_setor(self, obj):
        return obj.sala.galpao.setor.nome if obj.sala and obj.sala.galpao and obj.sala.galpao.setor else '-'
    
    get_galpao.short_description = 'Galpão'
    get_setor.short_description = 'Setor'

# Animais

class EspecieAdmin(admin.ModelAdmin):
    list_display = ['nome']
    list_display_links = ['nome']
    list_filter = ['nome']
    list_per_page = 10
    ordering = ['id']
    search_fields = ['nome']
    show_full_result_count = True

class RacaAdmin(admin.ModelAdmin):
    list_display = ['nome']
    list_display_links = ['nome']
    list_filter = ['nome']
    list_per_page = 10
    ordering = ['id']
    search_fields = ['nome']
    show_full_result_count = True

class TipoAdmin(admin.ModelAdmin):
    list_display = ['nome']
    list_display_links = ['nome']
    list_filter = ['nome']
    list_per_page = 10
    ordering = ['id']
    search_fields = ['nome']
    show_full_result_count = True

class AnimalAdmin(admin.ModelAdmin):
    date_hierarchy = 'data_hora_nascimento'
    list_display = ['id', 'identificacao_unica', 'rfid', 'especie', 'raca', 'tipo', 'sexo', 'peso_nascimento', 'data_hora_nascimento', 'mae', 'pai', 'status', 'setor']
    list_display_links = ['identificacao_unica']
    list_filter = ['especie', 'raca', 'tipo', 'sexo', 'data_hora_nascimento', 'status', 'setor']
    list_per_page = 10
    ordering = ['id']
    search_fields = ['identificacao_unica', 'rfid', 'especie__nome', 'raca__nome', 'tipo__nome']
    show_full_result_count = True

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'setor':
            kwargs['initial'] = get_user_setor(request.user)
            kwargs['disabled'] = True

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class SuinoAdmin(AnimalAdmin, ImportExportModelAdmin):
    date_hierarchy = AnimalAdmin.date_hierarchy
    list_display = AnimalAdmin.list_display
    list_display_links = AnimalAdmin.list_display_links
    list_filter = AnimalAdmin.list_filter
    list_per_page = AnimalAdmin.list_per_page
    ordering = AnimalAdmin.ordering
    resource_classes = [SuinoImportResource, SuinoExportResource]
    search_fields = AnimalAdmin.search_fields
    show_full_result_count = AnimalAdmin.show_full_result_count

class BovinoCorteAdmin(AnimalAdmin, ImportExportModelAdmin):
    date_hierarchy = AnimalAdmin.date_hierarchy
    list_display = AnimalAdmin.list_display + ['modo_criacao', 'local']
    list_display_links = AnimalAdmin.list_display_links
    list_filter = AnimalAdmin.list_filter + ['modo_criacao', 'local']
    list_per_page = AnimalAdmin.list_per_page
    ordering = AnimalAdmin.ordering
    resource_classes = [BovinoCorteImportResource, BovinoCorteExportResource]
    search_fields = AnimalAdmin.search_fields
    show_full_result_count = AnimalAdmin.show_full_result_count

class BovinoLeiteAdmin(AnimalAdmin, ImportExportModelAdmin):
    date_hierarchy = AnimalAdmin.date_hierarchy
    list_display = AnimalAdmin.list_display + ['nome', 'grau_sangue', 'pelagem']
    list_display_links = AnimalAdmin.list_display_links
    list_filter = AnimalAdmin.list_filter + ['nome', 'grau_sangue', 'pelagem']
    list_per_page = AnimalAdmin.list_per_page
    ordering = AnimalAdmin.ordering
    resource_classes = [BovinoLeiteImportResource, BovinoLeiteExportResource]
    search_fields = AnimalAdmin.search_fields
    show_full_result_count = AnimalAdmin.show_full_result_count

# Lotes

class LoteImportExportModelAdmin(admin.ModelAdmin):
    pass

class LoteAdmin(LoteImportExportModelAdmin, ImportExportModelAdmin):
    class AnimalInline(admin.StackedInline):
        model = Lote.animais.through
        extra = 0

        def formfield_for_foreignkey(self, db_field, request, **kwargs):
            if db_field.name == 'animal':
                kwargs['queryset'] = Animal.objects.filter(setor=get_user_setor(request.user))
            return super().formfield_for_foreignkey(db_field, request, **kwargs)

    exclude = ['animais']
    inlines = [AnimalInline]
    list_display = ['numero', 'baia', 'get_animais', 'setor']
    list_display_links = ['numero']
    list_filter = ['numero', 'baia', 'setor']
    list_per_page = 10
    ordering = ['id']
    resource_classes = [LoteImportResource, LoteExportResource]
    search_fields = ['numero', 'baia__numero', 'baia__sala__numero', 'baia__sala__galpao__nome', 'baia__sala__galpao__setor__nome']
    show_full_result_count = True

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'setor':
            kwargs['initial'] = get_user_setor(request.user)
            kwargs['disabled'] = True
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_animais(self, obj):
        return mark_safe('<br>'.join([str(animal.identificacao_unica) for animal in obj.animais.all()])) if obj.animais.exists() else '-'
    
    get_animais.short_description = 'Animais'

# Partos

class PartoImportExportModelAdmin(admin.ModelAdmin):
    pass

class PartoAdmin(PartoImportExportModelAdmin, ImportExportModelAdmin):
    class SuinoInline(admin.StackedInline):
        model = Suino
        extra = 0

    class BovinoCorteInline(admin.StackedInline):
        model = BovinoCorte
        extra = 0

    class BovinoLeiteInline(admin.StackedInline):
        model = BovinoLeite
        extra = 0

    date_hierarchy = 'data_hora_parto'
    list_display = ['femea', 'macho', 'data_hora_parto', 'tipo', 'setor', 'quantidade_filhotes_vivos', 'quantidade_filhotes_mortos', 'quantidade_filhotes_mumificados']
    list_display_links = ['femea', 'macho', 'data_hora_parto']
    list_filter = ['femea', 'macho', 'data_hora_parto', 'tipo', 'setor']
    list_per_page = 10
    ordering = ['id']
    resource_classes = [PartoImportResource, PartoExportResource]
    search_fields = ['femea', 'macho', 'data_hora_parto', 'tipo', 'setor']
    show_full_result_count = True
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'femea':
            kwargs['queryset'] = Animal.objects.filter(sexo='Fêmea', setor=get_user_setor(request.user))
        elif db_field.name == 'macho':
            kwargs['queryset'] = Animal.objects.filter(sexo='Macho', setor=get_user_setor(request.user))
        elif db_field.name == 'setor':
            kwargs['initial'] = get_user_setor(request.user)
            kwargs['disabled'] = True
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def get_formsets_with_inlines(self, request, obj=None):
        setor = get_user_setor(request.user)
        inlines = []

        if setor:
            if setor.nome == 'Suínocultura':
                inlines = [self.SuinoInline]
            elif setor.nome == 'Bovinocultura de Corte':
                inlines = [self.BovinoCorteInline]
            elif setor.nome == 'Bovinocultura de Leite':
                inlines = [self.BovinoLeiteInline]

        for inline in inlines:
            yield inline(self.model, self.admin_site).get_formset(request, obj), inline(self.model, self.admin_site)

# Manejos

class ManejoAdmin(admin.ModelAdmin):
    list_display = ['funcionario', 'observacao']
    list_display_links = ['funcionario']
    list_filter = ['funcionario']
    list_per_page = 10
    ordering = ['id']
    search_fields = ['funcionario']
    show_full_result_count = True

class ManejoPecuariaAdmin(ManejoAdmin, ImportExportModelAdmin):
    class ProcedimentoManejoInline(admin.TabularInline):
        model = ProcedimentoManejo
        extra = 0

    class ProdutoManejoInline(admin.TabularInline):
        model = ProdutoManejo
        extra = 0

    date_hierarchy = 'data_hora_manejo'
    inlines = [ProcedimentoManejoInline, ProdutoManejoInline]
    list_display = ManejoAdmin.list_display + ['animal', 'lote', 'data_hora_manejo', 'setor']
    list_display_links = ManejoAdmin.list_display_links
    list_filter = ManejoAdmin.list_filter + ['animal', 'lote', 'data_hora_manejo', 'setor']
    list_per_page = ManejoAdmin.list_per_page
    ordering = ManejoAdmin.ordering
    resource_classes = [ManejoPecuariaImportResource, ManejoPecuariaExportResource]
    search_fields = ManejoAdmin.search_fields + ['animal', 'lote', 'data_hora_manejo', 'setor']
    show_full_result_count = ManejoAdmin.show_full_result_count

    def get_user_setor(self, user):
        return SetorPecuaria.objects.filter(usuarios=user).first()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'animal':
            kwargs['queryset'] = Animal.objects.filter(setor=get_user_setor(request.user))
        elif db_field.name == 'lote':
            kwargs['queryset'] = Lote.objects.filter(setor=get_user_setor(request.user))
        elif db_field.name == 'setor':
            kwargs['initial'] = get_user_setor(request.user)
            kwargs['disabled'] = True
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
# Coberturas

class CoberturaAdmin(admin.ModelAdmin):
    date_hierarchy = 'data_hora_cobertura'
    list_display = ['id', 'femea', 'macho', 'data_hora_cobertura', 'setor']
    list_display_links = ['id']
    list_filter = ['femea', 'macho', 'data_hora_cobertura', 'setor']
    list_per_page = 10
    ordering = ['id']
    search_fields = ['femea', 'macho', 'data_hora_cobertura', 'setor']
    show_full_result_count = True
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'femea':
            kwargs['queryset'] = Animal.objects.filter(sexo='Fêmea', setor=get_user_setor(request.user))
        elif db_field.name == 'macho':
            kwargs['queryset'] = Animal.objects.filter(sexo='Macho', setor=get_user_setor(request.user))
        elif db_field.name == 'setor':
            kwargs['initial'] = get_user_setor(request.user)
            kwargs['disabled'] = True
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
# Saída
    
class SaidaAdmin(admin.ModelAdmin):
    date_hierarchy = 'data_hora_saida'
    list_display = ['id', 'animal', 'data_hora_saida', 'tipo', 'setor', 'observacao']
    list_display_links = ['id']
    list_filter = ['animal', 'data_hora_saida', 'tipo', 'setor']
    list_per_page = 10
    ordering = ['id']
    search_fields = ['animal', 'data_hora_saida', 'tipo', 'setor', 'observacao']
    show_full_result_count = True
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'animal':
            kwargs['queryset'] = Animal.objects.filter(setor=get_user_setor(request.user))
        elif db_field.name == 'setor':
            kwargs['initial'] = get_user_setor(request.user)
            kwargs['disabled'] = True
        return super().formfield_for_foreignkey(db_field, request, **kwargs)    

admin.site.register(SetorPecuaria, SetorPecuariaAdmin)
admin.site.register(Galpao, GalpaoAdmin)
admin.site.register(Sala, SalaAdmin)
admin.site.register(Baia, BaiaAdmin)
admin.site.register(Especie, EspecieAdmin)
admin.site.register(Raca, RacaAdmin)
admin.site.register(Tipo, TipoAdmin)
admin.site.register(Animal, AnimalAdmin)
admin.site.register(Suino, SuinoAdmin)
admin.site.register(BovinoCorte, BovinoCorteAdmin)
admin.site.register(BovinoLeite, BovinoLeiteAdmin)
admin.site.register(Lote, LoteAdmin)
admin.site.register(Parto, PartoAdmin)
admin.site.register(Manejo, ManejoAdmin)
admin.site.register(ManejoPecuaria, ManejoPecuariaAdmin)
admin.site.register(ProcedimentoManejo)
admin.site.register(ProdutoManejo)
admin.site.register(Produto)
admin.site.register(Procedimento)
admin.site.register(TipoProcedimento)
admin.site.register(TipoProduto)
admin.site.register(Funcionario)
admin.site.register(Cobertura, CoberturaAdmin)
admin.site.register(Saida, SaidaAdmin)
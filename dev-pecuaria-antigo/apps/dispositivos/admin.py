from django.contrib import admin
from .models import *

'''
class DispositivoAdmin(admin.ModelAdmin):
    exclude = ('componente',)

class ComponenteInline(admin.StackedInline):
    model = Componente
    extra = 0 

class AtuadorInline(admin.StackedInline):
    model = Atuador
    extra = 0

class DispositivoAdmin(admin.ModelAdmin):
    inlines = [ComponenteInline, AtuadorInline,]

admin.site.register(Dispositivo, DispositivoAdmin)
admin.site.register(Tipo_dispositivo)
admin.site.register(Manutencao)
admin.site.register(Alocacao_dispositivo)
admin.site.register(Pessoa)
admin.site.register(Componente_Tipo)
admin.site.register(Componentes_especificacoes)
admin.site.register(Servico)
admin.site.register(Manutencao_Servico)
admin.site.register(Manutencao_Produto)
admin.site.register(Setor)
admin.site.register(Setor_Unidade)
'''
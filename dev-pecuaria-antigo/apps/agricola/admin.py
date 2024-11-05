from django.contrib import admin
from .models import *

# Tabelas de área
admin.site.register(Fazenda)
admin.site.register(Areas)
admin.site.register(Talhao)

# Tabelas de plantio
admin.site.register(TipoCultura)
admin.site.register(VariedadePlanta)
admin.site.register(Cultivar)
admin.site.register(Planta)

# Tabelas de producao
admin.site.register(TipoFerramenta)
admin.site.register(Ferramenta)
admin.site.register(Servico)
admin.site.register(Producao)

# Tabelas de estoque
# ...

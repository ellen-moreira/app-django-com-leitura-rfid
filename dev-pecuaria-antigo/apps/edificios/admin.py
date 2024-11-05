from django.contrib import admin
from .models import *

class RoomAdmin(admin.ModelAdmin):
    exclude = ('room',)  # Change 'Salas' to 'room'

class RoomInline(admin.StackedInline):
    model = Room
    extra = 1
    
class UnitAdmin(admin.ModelAdmin):
    exclude = ('unit',)  # Change 'Salas' to 'room'

class UnitInline(admin.StackedInline):
    model = Unit
    extra = 1

class InstituitionAdmin(admin.ModelAdmin):
    inlines = [UnitInline]

class BuildingAdmin(admin.ModelAdmin):
    inlines = [RoomInline]


class ManageShiftAdmin(admin.ModelAdmin):
    exclude = ('shift',)  #  # Change 'Salas' to 'room'

class ManageShiftInline(admin.StackedInline):
    model = ManageShift
    extra = 1

class ShiftAdmin(admin.ModelAdmin):
    inlines = [ManageShiftInline]

class RoomAllocationAdmin(admin.ModelAdmin):
    list_display = ('building', 'number_rooms', 'data', 'start_time', 'end_time', 'name_allocation', 'grade', 'discipline')
    list_filter = ('building', 'grade', 'discipline')  # Filtros por prédio, turma e disciplina
    exclude = ['alocacao']
    search_fields = ['id','building', 'number_rooms']
    ordering = ['data']
    list_per_page = 20
    list_display_links = ('building', 'number_rooms')  # Adicionando links para detalhes
    

    
admin.site.register(Room, RoomAdmin)
admin.site.register(Building, BuildingAdmin)  # Change 'Edificio' to 'Building'
admin.site.register(RoomAllocation,RoomAllocationAdmin, verbose_name="Alocação de Sala")
admin.site.register(Corridor, verbose_name="Corredor")
admin.site.register(Floor, verbose_name="Piso")
admin.site.register(Shift,ShiftAdmin, verbose_name="Turno")
admin.site.register(DayOfWeek, verbose_name="Dia da Semana")
admin.site.register(ManageShift,ManageShiftAdmin, verbose_name="Gerenciar Turno")
admin.site.register(RoomType, verbose_name="Tipo de Sala")
admin.site.register(RoomStatus, verbose_name="Status da Sala")
admin.site.register(Unit,UnitAdmin, verbose_name="Unidade")
admin.site.register(Institution,InstituitionAdmin, verbose_name="Instituição")


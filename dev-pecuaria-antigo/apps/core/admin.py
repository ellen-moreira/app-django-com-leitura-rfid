from django.contrib import admin
from .models import *

# Produtos
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'category')

class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

class MeasureAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

class ModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

class PackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

class ItemsAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'category', 'subcategory', 'brand', 'manufacturer', 'measure', 'model', 'package')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Subcategory, SubcategoryAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Manufacturer, ManufacturerAdmin)
admin.site.register(Measure, MeasureAdmin)
admin.site.register(Model, ModelAdmin)
admin.site.register(Package, PackageAdmin)
admin.site.register(Items, ItemsAdmin)

# Instituição

class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

class InstitutionUnitAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

class SectorAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

class SubSectorAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'sector')

admin.site.register(Institution, InstitutionAdmin)
admin.site.register(InstituitionUnit, InstitutionUnitAdmin)
admin.site.register(Sector, SectorAdmin)
admin.site.register(SubSector, SubSectorAdmin)

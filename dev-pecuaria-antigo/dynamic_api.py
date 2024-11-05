# from django.apps import apps
# from rest_framework import serializers, viewsets, routers

# class BaseDynamicSerializer(serializers.ModelSerializer):
#     def to_representation(self, instance):
#         ret = super().to_representation(instance)
#         for field_name, field in self.fields.items():
#             if isinstance(field, serializers.PrimaryKeyRelatedField):
#                 related_object = getattr(instance, field_name)
#                 if related_object:
#                     related_value = str(related_object)
#                     ret[field_name] = related_value
#             elif isinstance(field, serializers.DateTimeField):
#                 field_value = getattr(instance, field_name)
#                 if field_value:
#                     field_value = field_value.strftime('%d/%m/%Y às %H:%M:%S')
#                     ret[field_name] = field_value
#             elif isinstance(field, serializers.DateField):
#                 field_value = getattr(instance, field_name)
#                 if field_value:
#                     field_value = field_value.strftime('%d/%m/%Y')
#                     ret[field_name] = field_value
#         return ret

# class DynamicAPIBuilder:
#     # Construtor da classe
#     def __init__(self, app, model, fields=None, url_field=True, related_models=None, related_field=None, depth=None, prefix=None, permission_classes=None, filters_backend=None, filterset_fields=None, ordering_fields=None):
#         self.app = f'apps.{app}' or apps.get_app_config(f'apps.{app}').name
#         self.model = model
#         self.fields = fields or [field.name for field in self.model._meta.fields]
#         self.url_field = url_field or False
#         self.related_models = related_models or []
#         self.related_field = related_field or self.model.__name__.lower()
#         self.depth = depth or 0
#         self.prefix = prefix or model.__name__.lower()
#         self.permission_classes = permission_classes or []
#         self.filters_backend = filters_backend or []
#         self.filterset_fields = filterset_fields or []
#         self.ordering_fields = ordering_fields or '__all__'

#     # Função que adiciona o campo url aos fields do serializer
#     def _add_url(self):
#         if self.url_field:
#             if 'url' not in self.fields:
#                 self.fields.insert(0, 'url')

#     # Função que adiciona as relações reversas aos fields do serializer
#     def _add_related_names(self):
#         if self.related_models:
#             related_names = [related_name._meta.get_field(self.related_field)._related_name for related_name in self.related_models] 
#             self.fields.extend(related_names)

#     # Função que cria a estrutura da API
#     def create_api(self):
#         class DynamicSerializer(BaseDynamicSerializer):
#             self._add_related_names()
#             self._add_url()
            
#             class Meta:
#                 model = self.model
#                 fields = self.fields
#                 depth = self.depth

#             print(self.fields)
#             print(self.app) # segunda forma de obter o nome do app
#             print(apps.get_app_config('app').name) # primeira forma de obter o nome do app
#             print(apps.get_containing_app_config(__file__)) # terceira forma de obter o nome do app
        
#         class DynamicViewSet(viewsets.ModelViewSet):
#             queryset = self.model.objects.all()
#             serializer_class = DynamicSerializer
#             permission_classes = self.permission_classes
#             filter_backends = self.filters_backend
#             filterset_fields = self.filterset_fields
#             ordering_fields = self.ordering_fields

#         router = routers.DefaultRouter()
#         router.register(f'{self.app}/{self.prefix}', DynamicViewSet)
#         return router
    
# # Exemplo de uso
    
# # from app.models import *
# # from django.contrib.auth.models import User
# # from components.dynamic_api import DynamicAPIBuilder
# # from rest_framework import permissions, routers, filters
# # from django_filters.rest_framework import DjangoFilterBackend
    
# # # Defina os modelos e prefixos desejados em uma lista ou dicionário
# # params = [
# #     {
# #         'app': pecuaria,
# #         'model': Animal,
# #         'url_field': False,
# #         'related_models': [LoteAnimal],
# #         'related_field': 'animal',
# #         'prefix': 'animais',
# #     },
# #     {
# #         'app': pecuaria,
# #         'model': Lote,
# #         'related_models': [LoteAnimal],
# #         'related_field': 'lote',
# #         'prefix': 'lotes',
# #     },
# #     {
# #         'app': pecuaria,
# #         'model': Parto,
# #         'related_models': [Animal],
# #         'related_field': 'parto',
# #         # 'depth': 1
# #         'prefix': 'partos',
# #     },
# #     {
# #         'app': pecuaria,
# #         'model': Manejo,
# #         'related_models': [ProcedimentoManejo, ProdutoManejo],
# #         'related_field': 'manejo',
# #         'prefix': 'manejos',
# #     },
# #     {
# #         'app': pecuaria,
# #         'model': User,
# #         'fields': ['id', 'username', 'email'],
# #         'prefix': 'usuarios',
# #         'permission_classes': [permissions.IsAdminUser],
# #         'filters_backend': [DjangoFilterBackend],
# #         'filterset_fields': ['username', 'email']
# #     }
# # ]

# # # Crie uma lista de instâncias da classe DynamicAPIBuilder
# # builders = [DynamicAPIBuilder(**mp) for mp in params]

# # # Crie um único router final
# # router = routers.DefaultRouter()

# # # Itere sobre as instâncias da classe DynamicAPIBuilder
# # for builder in builders:
# #     # Crie o router e estenda o registro com o registro do novo router
# #     router.registry.extend(builder.create_api().registry)

from apps import *
from django.db import models
from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework.settings import api_settings
from rest_framework import serializers, viewsets, routers
from collections import defaultdict
from itertools import chain

class CreateDynamicAPI:
    def __init__(
        self,
        app,
        model,
        url_field=None,
        fields=None,
        depth=None,
        related_models=None,
        related_models_fields=None,
        related_depth=None,
        queryset=None,
        # authentication_classes=None,
        # permission_classes=None,
        filter_backends=None,
        filterset_fields=None,
        search_fields=None,
        ordering_fields=None,
        ordering=None,
        prefix=None
    ):
        self.app = app
        self.model = model
        self.url_field = url_field if url_field else False
        self.fields = fields if fields else [field.name for field in self.model._meta.get_fields()]
        self.depth = depth if depth else 0
        self.related_models = related_models
        self.related_models_fields = related_models_fields if related_models_fields else []
        self.related_depth = related_depth if related_depth else 0
        self.queryset = queryset if queryset else self.model.objects.all()
        # self.authentication_classes = authentication_classes if authentication_classes else []
        # self.permission_classes = permission_classes if permission_classes else []
        self.filter_backends = filter_backends if filter_backends else []
        self.filterset_fields = filterset_fields if filterset_fields else []
        self.search_fields = search_fields if search_fields else []
        self.ordering_fields = ordering_fields if ordering_fields else []
        self.ordering = ordering if ordering else []
        self.prefix = prefix if prefix else f'{self.model._meta.verbose_name_plural.lower().replace(" ", "_")}'

    def create_dynamic_serializer(self):
        related_serializers = {}

        if self.related_models:
            for related_model, related_model_fields in zip(self.related_models, self.related_models_fields):
                class DynamicRelatedSerializer(serializers.ModelSerializer):
                    class Meta:
                        model = related_model
                        fields = related_model_fields
                        depth = self.related_depth

                for field in related_model._meta.get_fields():
                    if isinstance(field, models.ForeignKey) and field.related_model == self.model:
                        related_name = field.related_query_name()
                        related_serializers[related_name] = DynamicRelatedSerializer

        related_foreign_keys = {}

        if self.fields:
            for field in self.model._meta.get_fields():
                if isinstance(field, models.ForeignKey):
                    class DynamicForeignKeyRelatedField(serializers.ModelSerializer):
                        class Meta:
                            model = field.related_model
                            fields = [field.name for field in field.related_model._meta.get_fields() if field.name != 'id' and not isinstance(field, models.ManyToOneRel)]

                    related_foreign_keys[field.name] = DynamicForeignKeyRelatedField

        class DynamicSerializer(WritableNestedModelSerializer):
            for field_name in self.fields:
                field = self.model._meta.get_field(field_name)
                if isinstance(field, models.ManyToManyField):
                    locals()[field_name] = serializers.PrimaryKeyRelatedField(many=True, queryset=field.related_model.objects.all())

            if self.related_models:
                for related_name, related_serializer in related_serializers.items():
                    locals()[related_name] = related_serializer(many=True)
                    self.fields.append(related_name)

            if related_foreign_keys:
                for field_name, related_field in related_foreign_keys.items():
                    locals()[field_name] = related_field()
                    self.fields.append(field_name)

            if self.url_field:
                self.fields.insert(0, 'url')
                        
            class Meta:
                model = self.model
                fields = self.fields
                depth = self.depth

        return DynamicSerializer

    def create_dynamic_viewset(self):
        class DynamicViewSet(viewsets.ModelViewSet):
            queryset = self.queryset
            serializer_class = self.create_dynamic_serializer()
            # authentication_classes = self.authentication_classes
            # permission_classes = self.permission_classes
            filter_backends = self.filter_backends
            filterset_fields = self.filterset_fields
            search_fields = self.search_fields
            ordering_fields = self.ordering_fields
            ordering = self.ordering

            def get_queryset(self):
                queryset = super().get_queryset()
                filter_params = self.request.query_params.dict()
                filter_params.pop('format', None)
                filter_params.pop('search', None)
                filter_params.pop('ordering', None)
                filter_params.pop('limit', None)
                filter_params.pop('offset', None)
                filter_params.pop('page', None)
                filter_params.pop('group_by', None)  # Remover o parâmetro 'group_by'
                filter_params = {key: value for key, value in filter_params.items() if value}
                return queryset.filter(**filter_params)

            def group_by(self, data, group_fields):
                if not group_fields:
                    return data

                field = group_fields[0]
                grouped_data = defaultdict(list)

                for item in data:
                    if isinstance(item[field], list):
                        keys = item[field]
                    else:
                        keys = [item[field]]
                    
                    for key in keys:
                        grouped_data[key].append(item)

                grouped_result = []
                for key, value in grouped_data.items():
                    grouped_result.append({
                        field: key,
                        "children": self.group_by(value, group_fields[1:])
                    })

                return grouped_result

            def list(self, request, *args, **kwargs):
                response = super().list(request, *args, **kwargs)
                group_by_fields = request.query_params.get('group_by', None)
                if group_by_fields:
                    group_by_fields = group_by_fields.split(',')
                    response.data = self.group_by(response.data, group_by_fields)
                return response

        return DynamicViewSet
    
    def create_dynamic_router(self):
        router = routers.DefaultRouter()
        router.register(f'{self.app}/{self.prefix}', self.create_dynamic_viewset())
        return router
    
    def create_dynamic_api(self):
        return self.create_dynamic_router()
    
# Exemplo de uso

# from dynamic_api import CreateDynamicAPI
# from django.contrib.auth.models import User
# from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework import filters, routers
# from rest_framework_simplejwt.authentication import *

# params = [
#     {
#         'app': 'auth',
#         'model': User,
#         'url_field': True,
#         'fields': ['id', 'username', 'email', 'first_name', 'last_name', 'groups', 'user_permissions', 'is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined'],
#         'filter_backends': [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter],
#         'filterset_fields': ['id', 'username', 'email', 'is_staff', 'is_active', 'date_joined', 'last_login'],
#         'search_fields': ['id', 'username', 'email', 'is_staff', 'is_active', 'date_joined', 'last_login'],
#         'ordering_fields': ['id', 'username', 'email', 'is_staff', 'is_active', 'date_joined', 'last_login'],
#         'ordering': ['id'],
#         'prefix': 'usuarios'
#     }
# ]

# builders = [CreateDynamicAPI(**param) for param in params]

# router = routers.DefaultRouter()

# [router.registry.extend(builder.create_dynamic_api().registry) for builder in builders]

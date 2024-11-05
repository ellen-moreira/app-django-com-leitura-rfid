from api.serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, response
from django.db.models import Count

class AnimalViewSet(viewsets.ModelViewSet):
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'

    def list(self, request, *args, **kwargs):
        group_by = request.query_params.get('group_by', None)
        if group_by:
            group_by_fields = group_by.split(',')
            queryset = self.queryset.values(*group_by_fields).annotate(count=Count('id'))
            results = self._build_nested_results(queryset, group_by_fields)
            return response.Response(results)
        else:
            return super().list(request, *args, **kwargs)

    def _build_nested_results(self, queryset, group_by_fields):
        results = []
        for item in queryset:
            current_level = results
            for field in group_by_fields:
                value = item[field]
                found = False
                for entry in current_level:
                    if entry.get(field) == value:
                        current_level = entry.setdefault('children', [])
                        found = True
                        break
                if not found:
                    new_entry = {field: value, 'children': []}
                    current_level.append(new_entry)
                    current_level = new_entry['children']
            
            # Adicionar os detalhes dos animais neste nível
            animals = Animal.objects.filter(**{field: item[field] for field in group_by_fields})
            serialized_animals = self.serializer_class(animals, many=True).data
            current_level.extend(serialized_animals)
        
        return results
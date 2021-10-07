from django_filters import rest_framework as filters

from reviews.models import Title


class TitleFilter(filters.FilterSet):
    category = filters.CharFilter(field_name='category__slug')
    genre = filters.CharFilter(field_name='genre__slug')
    name = filters.CharFilter(method='name_filter')

    def name_filter(self, queryset, name, value):
        return queryset.filter(name__contains=value)

    class Meta:
        model = Title
        fields = ('category', 'genre', 'name', 'year', )

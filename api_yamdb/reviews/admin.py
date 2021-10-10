from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title

admin.site.register(Category, admin.ModelAdmin)
admin.site.register(Genre, admin.ModelAdmin)
admin.site.register(Title, admin.ModelAdmin)
admin.site.register(Review, admin.ModelAdmin)
admin.site.register(Comment, admin.ModelAdmin)

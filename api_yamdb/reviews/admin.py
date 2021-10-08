from django.contrib import admin

from .models import (
    Category,
    Genre,
    Title,
    Review,
    Comment
)

admin.site.register(Category, admin.ModelAdmin)
admin.site.register(Genre, admin.ModelAdmin)
admin.site.register(Title, admin.ModelAdmin)
admin.site.register(Review, admin.ModelAdmin)
admin.site.register(Comment, admin.ModelAdmin)

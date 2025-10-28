from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'likes_count', 'favorites_count')
    search_fields = ('title', 'author__username')
    list_filter = ('created_at',)

    def likes_count(self, obj):
        return obj.liked_by.count()
    likes_count.short_description = 'Лайков'

    def favorites_count(self, obj):
        return obj.favorited_by.count()
    favorites_count.short_description = 'В избранном'

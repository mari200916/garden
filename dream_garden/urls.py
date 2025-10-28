from django.contrib import admin
from django.urls import path, include
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('like/<int:post_id>/', views.toggle_like, name='toggle_like'),
    path('favorite/<int:post_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('favorites/', views.favorites_view, name='favorites'),
    path('create/', views.create_post, name='create_post'),  # новая страница

]

from django.conf import settings
from django.conf.urls.static import static
# Чтобы медиа-файлы отображались в DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
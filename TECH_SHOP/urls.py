from django.contrib import admin
from django.urls import path, include


#Для отображения фото
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')), #login/logout
    path('', include('main_page.urls')),# Подключаем все адреса

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #Добавить изображение

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from imports import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('imports/', include('imports.urls')),
    path('upload/', views.upload_dataset, name='upload_dataset_root'),
    path('products/', views.products_list, name='products_list_root'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

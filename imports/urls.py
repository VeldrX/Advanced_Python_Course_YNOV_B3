from django.urls import path
from . import views

urlpatterns = [
    path("upload/", views.upload_dataset, name="upload_dataset"),
    path("result/<int:dataset_id>/", views.import_result, name="import_result"),
    path("products/", views.products_list, name="products_list"),
]

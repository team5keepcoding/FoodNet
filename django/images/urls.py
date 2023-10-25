from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='images-index'),
    path('upload/', views.upload_view, name='images-upload'),
    path('image-table/', views.image_table_view, name='image-table'),
]
from django.urls import path
from .views import index, livro

urlpatterns = [
    path('', index),
    path('Livro/<int:pk>', livro, name='Livro'),
    path('del_livro/<int:pk>', livro, name='del_livro')
]
from django.urls import path
from . import views 

urlpatterns = [
    path('', views.index, name='index_url'),
    path('Livro/<int:pk>', views.livro, name='Livro'),
    path('del_livro/<int:pk>', views.del_livro, name='deletar_livro_url'),
    path('upg_livro/<int:pk>', views.upg_livro, name='atualizar_livro_url'),
    path('cad_livro', views.cadastrar_livro, name='cadastrar_livro_url'),
    path('cad_user', views.cad_user, name='cad_user_url'),
    path('entrar', views.entrar, name='entrar_url'),
    path('sair', views.sair, name='sair_url'),
    path('graf', views.graf, name='graf_url'),
]
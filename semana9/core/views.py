from django.shortcuts import render, redirect
from .models import Livro

def index(request):
    livros = Livro.objects.all()
    context = {
        'livro': livros
    }
    return render(request, 'index.html', context)

def livro(request, pk):
    livro = Livro.objects.get(id=pk)
    context = {
        'livro': livro
    }
    return render(request, 'livro.html', context)

def del_livro(request, pk):
    livro = Livro.objects.get(id=pk)
    livro.delete()
    return redirect('index_url')

def cadastrar_livro(request):
    if request.method == 'GET':
        return render(request, 'cad_livro.html')
    elif request.method == 'POST':
        titulo = request.POST.get('titulo')
        preco = request.POST.get('preco')

        livro = Livro(
            title = titulo,
            price = preco,
        )

        livro.save()
        return redirect('/')
    

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
    print(f'>>>>>>>>>>> {livro}')
    #if request.method == 'POST':
    livro.delete()
    return redirect('index')
    

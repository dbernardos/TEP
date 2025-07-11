from django.shortcuts import render, redirect
from .models import Livro
from django.contrib.auth.models import User
from django.http.response import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

import matplotlib.pyplot as plt
import io
import base64
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def graf(request):
    livros = Livro.objects.all()
    df = pd.DataFrame.from_records(livros.values())

    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df['review_score'] = pd.to_numeric(df['review_score'], errors='coerce')

    df_grouped = df.groupby('review_score')['price'].mean().reset_index()

    fig = px.bar(
        df_grouped,
        x = 'review_score',
        y = 'price',
        title = 'Preço médio por avaliação',
        labels = {'review_score': 'Avaliação', 'price': 'Preço Médio (R$)'},
        template = 'plotly_white'
    )

    plot_div = fig.to_html(full_html=False)
    context = {
        'plot_div': plot_div
    }
    return render(request, 'graf.html', context)

@login_required(login_url='entrar_url')
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

def upg_livro(request, pk):
    if request.method == 'GET':
        livro = Livro.objects.get(id=pk)
        context = {
            'livro': livro,
        }
        return render(request, 'upg_livro.html', context)
    elif request.method == 'POST':
        titulo = request.POST.get('titulo')
        preco = request.POST.get('preco')

        livro = Livro(
            title = titulo,
            price = preco,
        )

        livro.save()
        return redirect('index_url')

def cadastrar_livro(request):
    if request.user.is_authenticated:
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
            return redirect('index_url')
    else:
        return redirect('entrar_url')
    
def cad_user(request):
    if request.method == 'GET':
        return render(request, 'cad_user.html')
    else:
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()
        #return HttpResponse('Sucesso ao cadastrar')
        return redirect('entrar_url')

def entrar(request):
    if request.method == 'GET':
        return render(request, 'entrar.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return redirect('index_url')
        else:
            return HttpResponse('Falha ao tentar autenticar')
        
def sair(request):
    logout(request)
    return redirect('entrar_url')

    

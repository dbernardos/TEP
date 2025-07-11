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


import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
nltk.download('wordnet')
nltk.download('omw-1.4')

from sklearn.tree import DecisionTreeClassifier

def features(request):
    livros = Livro.objects.all()
    df = pd.DataFrame.from_records(livros.values())
    df = df.dropna()

    # lemmatizer = WordNetLemmatizer()

    # def lematizar_nltk(texto):
    #     return ' '.join([lemmatizer.lemmatize(palavra) for palavra in texto.split()])

    # # Aplicando a função nos reviews
    # reviews_lematizados = [lematizar_nltk(review) for review in df['review_text']]
    def get_tfidf(df):
        # Criando o vetorizador TF-IDF
        vectorizer = TfidfVectorizer(
            stop_words='english', # Remove palavras comuns (stopwords)
            lowercase=True,       # Converte tudo para minúsculas
            min_df=5,            # Ignora palavras que aparecem em menos de 5 documentos
            max_df=0.8,           # Ignora palavras que aparecem em mais de 50% dos docs
            max_features=1000,     # Limita ao vocabulário mais frequente
            dtype=np.float32 
        )

        # Aplicando o TF-IDF na coluna 'review'
        tfidf_matrix = vectorizer.fit_transform(df['review_text'])

        # Convertendo para um DataFrame
        return pd.DataFrame(tfidf_matrix.toarray(), columns=vectorizer.get_feature_names_out())
    
    tfidf_df = get_tfidf(df)
    
    # definir os intervalos e os rótulos
    bins = [0.99, 2.0, 3.0, 5.0]
    labels = ['negativo', 'neutro', 'positivo']

    #aplicar pd.cut
    df['classe'] = pd.cut(pd.to_numeric(df['review_score']), bins=bins, labels=labels)

    # Resetar o índice para garantir alinhamento
    tfidf_df_reset = tfidf_df.reset_index(drop=True)
    df_reset = df.reset_index(drop=True)

    # Escolha a coluna que você quer adicionar (ex: 'sentiment')
    coluna_extra = df_reset['classe']

    # Concatenar no final do tfidf_df
    tfidf_extra = pd.concat([tfidf_df_reset, coluna_extra], axis=1)

    X = tfidf_extra.drop(columns=['classe'])
    Y = tfidf_extra['classe']

    clf = DecisionTreeClassifier()
    clf.fit(X,Y)
    ultimo = get_tfidf({'review_text': ['the book is bad. it is very long and boring. i want my money back. i do not recommend it']})

    print(ultimo)


    tfidf_extra.to_csv('tfidf_resultados2.csv', index=False)
    return HttpResponse('Acabou')

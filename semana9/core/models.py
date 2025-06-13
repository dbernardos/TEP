from django.db import models

class Livro(models.Model):
    titulo = models.CharField('Títilo', max_length=100)
    genero = models.CharField('Gênero', max_length=60, null=True)
    data_publicacao = models.DateField('Dada de publicação', null=True)
    numero_paginas = models.PositiveIntegerField('Páginas', null=True)
    estoque = models.PositiveIntegerField('Quantidade', null=True)
    preco = models.DecimalField('Preço', decimal_places=2, max_digits=8)

    def __str__(self):
        return self.titulo

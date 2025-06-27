from django.db import models

class Livro(models.Model):
    title = models.CharField('Título', max_length=100)
    price = models.DecimalField('Preço', decimal_places=2, max_digits=8, null=True)
    user_id = models.CharField('ID Usuário',  max_length=100, null=True)
    profileName = models.CharField('Usuário', max_length=100, null=True)  
    review_helpfulness = models.CharField('Utilidade', max_length=10, null=True)    
    review_score = models.CharField('Avaliação', max_length=10, null=True)   
    review_time = models.CharField('Hora do review', max_length=50, null=True)  
    review_summary = models.CharField('Resumo do review', max_length=500, null=True)   
    review_text = models.CharField('Texto do review', max_length=1000, null=True)  

    def __str__(self):
        return self.title

from .models import Livro
import csv

with open('new-books-dataset-1.5k.csv', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        Livro.objects.create(
            title=row['Title'],
            price=row['Price'],
            user_id=row['User_id'],
            profileName=row['profileName'],
            review_helpfulness=row['review/helpfulness'],
            review_score=row['review/score'],
            review_time=row['review/time'],
            review_summary=row['review/summary'],
            review_text=row['review/text'],

        )
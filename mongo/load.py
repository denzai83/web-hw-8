import json
from mongoengine import connect
from models import Author, Quote

connect(host='mongodb+srv://hw8:567432@cluster0.g08jtiw.mongodb.net/hw8?retryWrites=true&w=majority')


def load_authors(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        authors_data = json.load(f)
    authors = []
    for author_data in authors_data:
        author = Author(fullname=author_data['fullname'], born_date=author_data.get('born_date'), born_location=author_data.get('born_location'), description=author_data.get('description'))
        authors.append(author)
    Author.objects.insert(authors)


def load_quotes(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        quotes_data = json.load(f)
    quotes = []
    for quote_data in quotes_data:
        author_name = quote_data.get('author')
        author = Author.objects.get(fullname=author_name) if author_name else None
        quote = Quote(author=author, quote=quote_data['quote'], tags=quote_data.get('tags'))
        quotes.append(quote)
    Quote.objects.insert(quotes)

if __name__ == '__main__':
    load_authors('./authors.json')
    load_quotes('./quotes.json')
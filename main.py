import xml.etree.ElementTree as ET
import os
import pprint

DATA_DIR = 'data'

def read_xml(file_name):
    filepath = os.path.join(DATA_DIR, file_name)
    tree = ET.parse(filepath)
    return tree.getroot()

# --------- Parsanje podatkov iz xml ---------
def parse_authors(root):
    authors = [] #seznam slovarjev
    for author in root.findall('author'):
        authors.append({
            "id": author.get("id"),
            "name": author.findtext("name"),
            "authorSlug": author.findtext("authorSlug", default="")
        })
    return authors

def parse_books(root):
    books = []
    for book in root.findall('book'):
        books.append({
            "id": book.get("id"),
            "authorId": book.findtext("authorId"),
            "title": book.findtext("title"),
            "publisher": book.findtext("publisher", default=""),
            "publishedDate": book.findtext("publishedDate", default=""),
            "pageCount": int(book.findtext("pageCount", default="0")),
            "language": book.findtext("language", default=""),
            "averageRating": float(book.findtext("averageRating", default="0"))
        })
    return books

def parse_quotes(root):
    quotes = []
    for quote in root.findall('quote'):
        quotes.append({
            "id": quote.get("id"),
            "authorId": quote.findtext("authorId"),
            "content": quote.findtext("content"),
            "tags": quote.findtext("tags", default=""),
            "length": int(quote.findtext("length", default="0")),
            "dateAdded": quote.findtext("dateAdded", default="")
        })
    return quotes

# --------- Povezovanje avtorjev s knjigami, quoti ---------
def link_authors(authors, books, quotes):
    author_lookup = {author['id']: author for author in authors}
    for book in books:
        book['author'] = author_lookup.get(book['authorId'], {})
    
    for quote in quotes:
        quote['author'] = author_lookup.get(quote['authorId'], {})


# --------- Filtriranje knjig - minimalni rating ---------
def filter_books(books, min_rating=0):
    return [book for book in books if book['averageRating'] >= min_rating]

# --------- Filtriranje quotov - minimalno stevilo znakov ---------
def filter_quotes(quotes, min_length=0):
    return [quote for quote in quotes if quote['length'] >= min_length]

# --------- MAIN ---------
def main():
    authors = parse_authors(read_xml('authors.xml'))
    books = parse_books(read_xml('books.xml'))
    quotes = parse_quotes(read_xml('quotes.xml'))

    link_authors(authors, books, quotes)

    min_rating = float(input("Show books with average rating >= :"))
    min_length = int(input('Show quotes with minimal length: '))

    filtered_books = filter_books(books, min_rating)
    filtered_quotes = filter_quotes(quotes, min_length)

    print()
    print("\n---------Filtered Books:---------")
    print()
    pprint.pprint(filtered_books)
    

    print()
    print("\n---------Filtered Quotes:---------")
    print()
    pprint.pprint(filtered_quotes)

    
    # pprint.pprint(books)
    # pprint.pprint(quotes)

    # # print, da preverim za ziher, ce vse dela ok
    # print(authors)
    # print()
    # print(books)
    # print()
    # print(quotes)

if __name__ == "__main__":
    main()



#Sam izpis, 1. poskus, ignore
# import xml.etree.ElementTree as ET
# import os

# DATA_DIR = 'data/'       

# def read_xml(file_name):
#     filepath = os.path.join(DATA_DIR, file_name)
#     tree = ET.parse(filepath)
#     root = tree.getroot()
#     return root

# def print_authors(root):
#     print("--------Authors:--------")
#     for author in root.findall('author'):
#         author_id = author.get('id')
#         name = author.findtext('name')
#         author_slug = author.find('authorSlug')
#         # author_slug_element = author_slug.text if author_slug is not None else ''
#         print(f"ID: {author_id}, Name: {name}, Slug: {author_slug.text if author_slug is not None else 'N/A'}")

# def print_quotes(root):
#     print("--------Quotes:--------")
#     for quote in root.findall('quote'):
#         quote_id = quote.get('id')
#         author_id = quote.findtext('authorId')
#         content = quote.findtext('content')
#         print(f"ID: {quote_id}, Author ID: {author_id}, Content: {content}")

# def print_books(root):
#     print("--------Books:--------")
#     for book in root.findall('book'):
#         book_id = book.get('id')
#         author_id = book.findtext('authorId')
#         title = book.findtext('title')
#         published_date = book.findtext('publishedDate', default='')
#         average_rating = book.findtext('averageRating', default='')
#         print(f"ID: {book_id}, Author ID: {author_id}, Title: {title}, Published Date: {published_date if published_date else 'N/A'}, Average Rating: {average_rating if average_rating else 'N/A'}")

# def main():
#     authors_root = read_xml('authors.xml')
#     quotes_root = read_xml('quotes.xml')
#     books_root = read_xml('books.xml')

#     print_authors(authors_root)
#     print_quotes(quotes_root)
#     print_books(books_root)

# if __name__ == "__main__":
#     main()


# main.py
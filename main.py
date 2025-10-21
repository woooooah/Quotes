import xml.etree.ElementTree as ET
import os
import pprint
import json

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


# --------- SHRANI json ---------
FILTERED_DIR = 'filtered_json'

def save_json(data, filename):
    os.makedirs(FILTERED_DIR, exist_ok=True)

    filepath = os.path.join(FILTERED_DIR, filename)

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    print(f"Saved {filename} to {FILTERED_DIR}/")

# --------- SHRANI xml ---------


    # --------- dodava indent xmlu, da je format lepsi ---------
def indent_xml(elem, level=0):
    """
    Recursively adds indentation to an XML element for pretty printing.
    """
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        for child in elem:
            indent_xml(child, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i



FILTERED_XML_DIR = 'filtered_xml'

def save_filtered_xml(data, root_tag, item_tag, filename):
    os.makedirs(FILTERED_XML_DIR, exist_ok=True)

    root = ET.Element(root_tag)

    for item in data:
        elem = ET.SubElement(root, item_tag, id=item.get('id', ''))

        for key, value in item.items():
            if key == 'id':
                continue
            if isinstance(value, dict):
                sub_elem = ET.SubElement(elem, key)
                for sub_key, sub_val in value.items():
                    child = ET.SubElement(sub_elem, sub_key)
                    child.text = str(sub_val) if sub_val is not None else ""

            else:
                child = ET.SubElement(elem, key)
                child.text = str(value)
        
        indent_xml(root)

        tree = ET.ElementTree(root)
        filepath = os.path.join(FILTERED_XML_DIR, filename)
        tree.write(filepath, encoding='utf-8', xml_declaration=True)
        print(f"Saved {filename} to {FILTERED_XML_DIR}/")


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

    save_json(filtered_books, 'filtrirano_books.json')
    save_json(filtered_quotes, 'filtrirano_quotes.json')
    print()
    print("Filtered results saved to JSON!")

    save_filtered_xml(filtered_books, root_tag='books', item_tag='book', filename='filtrirano_books.xml')
    save_filtered_xml(filtered_quotes, root_tag='quotes', item_tag='quote', filename='filtrirano_quotes.xml')


if __name__ == "__main__":
    main()

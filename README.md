# QuotesAPP

QuotesAPP je preprost konzolni program, ki:

1. Prebere podatke iz **XML datotek**
   - `authors.xml` – seznam avtorjev
   - `books.xml` – seznam knjig
   - `quotes.xml` – seznam citatov
2. Poveze podatke preko atributa `authorId`
3. Omogoca filtriranje knjig in citatov po:
   - minimalni oceni knjige
   - minimalni dolzini citata
4. Izvede izvoz filtriranih rezultatov:
   - JSON (`filtered_json/filtrirano_books.json`, `filtered_json/filtrirano_quotes.json`)
   - XML (`filtered_xml/filtrirano_books.xml`, `filtered_xml/filtrirano_quotes.xml`)

## Zagon projekta:

1. `cd quotes`
2. `python3 main.py`

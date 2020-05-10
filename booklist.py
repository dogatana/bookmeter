import json
import csv


class Book:
    def __init__(self, title, authors, image, book_id, asin):
        self.title = title
        self.authors = authors
        self.image = image
        self.book_id = book_id
        self.asin = asin

    def __str__(self):
        return f"Book({self.title}, {self.authors}, {self.asin})"

    def to_dict(self):
        return {
            "title": self.title,
            "authors": self.authors,
            "image": self.image,
            "book_id": self.book_id,
            "asin": self.asin,
        }

    def to_list(self):
        authors = ",".join([str(author) for author in self.authors])
        return [self.title, authors, self.image]


class BookList:
    def __init__(self):
        self.book_list = []

    def add(self, book):
        self.book_list.append(book)

    def len(self):
        return len(self.book_list)

    def serialize(self):
        return {
            "class": "BookList",
            "books": [book.to_dict() for book in self.book_list],
        }

    def save_to_json(self, filename):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self, f, cls=BookListJSONEncoder)

    def save_to_csv(self, filename):
        with open(filename, "w", encoding="utf_8_sig", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["title", "author(s)", "cover"])
            rows = [book.to_list() for book in self.book_list]
            writer.writerows(rows)

    def dump(self):
        for book in self.book_list:
            print(str(book))


class BookListJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, BookList):
            return o.serialize()
        return super().default(o)

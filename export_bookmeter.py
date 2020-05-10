""" export the list of books that you have read from 読書メータ """
import itertools
import time
import sys
import re
from datetime import datetime

import requests
import lxml.html

from booklist import Book, BookList


def main(base_url):
    booklist = download_books(base_url)
    print(booklist.len(), "books in total")

    date = get_date()
    save_file_as(booklist, f"bookmeter_{date}.json", booklist.save_to_json)
    save_file_as(booklist, f"bookmeter_{date}.csv", booklist.save_to_csv)


def download_books(base_url):
    booklist = BookList()
    for page in itertools.count(1):
        url = base_url
        if page != 1:
            url += f"&page={page}"
        for retry_count in itertools.count(0):
            res = requests.get(url)
            print("page:", page, ", status_code:", res.status_code)
            if res.status_code == 404:
                print("*** invalid user_id")
                exit()
            time.sleep(30)
            if res.status_code == 200:
                break
            if retry_count > 3:
                print("** retry over, exit")
                exit()

        # 公開用に削除
        # save_page(page, res.content)
        count = parse_books(booklist, res.content)
        if count == 0:
            break

    return booklist


def save_page(page_number, contents):
    filename = f"page_{page_number}.html"
    print("save to", filename)
    with open(filename, "wb") as f:
        f.write(contents)


def parse_books(book_list, contents):
    doc = lxml.html.fromstring(contents)
    count = 0
    for li_tag in doc.xpath('//li[@class="group__book"]'):
        book_list.add(parse_book(li_tag))
        count += 1
    return count


def parse_book(node):
    authors = [
        tag.text
        for tag in node.xpath(
            './div[@class="book__detail"]/ul[@class="detail__authors"]/li/a'
        )
    ]

    tag = node.xpath("./div/div/a")[0]
    book_id = tag.attrib["href"]

    cover = node.xpath('./div/div/a/img[@class="cover__image"]')[0]
    title = cover.attrib["alt"]
    image = cover.attrib["src"]
    asin = ""  # get_asin(book_id)
    return Book(title, authors, image, book_id, asin)


def get_asin(book_id):
    url = "https://bookmeter.com" + book_id
    res = requests.get(url)
    time.sleep(5)
    if res.status_code != 200:
        return "?"
    doc = lxml.html.fromstring(res.content)
    tag = doc.xpath('//div[@class="group__image"]/a')[0]
    href = tag.attrib["href"]

    result = re.search("creativeASIN=(.{10})", href)
    if result is None:
        return "?"
    return result.group(1)


def get_date():
    return datetime.today().strftime("%y%m%d")


def save_file_as(book_list, filename, save_method):
    print("save to", filename)
    save_method(filename)


def usage():
    print("usage: python export_bookmete.rpy <user_id>")
    exit()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        usage()
    user_id = sys.argv[1]
    # 読んだ本
    base_url = f"https://bookmeter.com/users/{user_id}/books/read?display_type=grid"
    # 読んでる本
    # base_url = f"https://bookmeter.com/users/{user_id}/books/reading?display_type=grid"
    # 積読本
    # base_url = f"https://bookmeter.com/users/{user_id}/books/stacked?display_type=grid"
    # 読みたい本
    # base_url = f"https://bookmeter.com/users/{user_id}/books/wish?display_type=grid"
    main(base_url)

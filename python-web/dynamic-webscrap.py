from requests_html import HTMLSession
from pymongo import MongoClient

# MongoDB setup
client = MongoClient("mongodb://localhost:27017")
mydb = client["webscrap"]
information = mydb.python

# HTMLSession setup
session = HTMLSession()
# url = "https://www.digitaltrends.com/computing/windows-12-may-not-happen-anytime-soon/"
url = input('Masukkan URL: ')

r = session.get(url)
r.html.render(sleep=1, scrolldown=3)

# Finding articles
articles = r.html.find(input('Masukkan class artikel: '))

if not articles:
    print("artikelnya gada")
else:
    for item in articles:
        # Extract title
        newsitem_h1 = item.find("h1", first=True)
        if newsitem_h1:
            title = newsitem_h1.text
            print(title)
        else:
            print("gada h1")
        newsitem_author = item.find(input('Masukkan class author: '))
        if newsitem_author:
            # link = newsitem_author.absolute_links
            name = newsitem_author[0].find("a", first=True).text
            print(name)

            # Extract content and link
            newsitem_p = item.find(input('Masukkan class paragraf: '))
            newsitem_date = item.find(input('Masukkan class tanggal: '))
            links = []
            if newsitem_p:
                for p in newsitem_p:
                    if p.absolute_links:
                        links.extend(list(p.absolute_links))

            data = {
                "title": title,
                "author": name,
                "date": newsitem_date[0].text if newsitem_date else "",
                "content": " ".join(p.text for p in newsitem_p) if newsitem_p else "",
                "link": links,
            }

            information.insert_one(data)
            print(f"data yang dimasukkan: {data}")
        else:
            print("gada paragraf")

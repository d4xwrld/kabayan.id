from requests_html import HTMLSession
from pymongo import MongoClient

# MongoDB setup
client = MongoClient('mongodb://localhost:27017')
mydb = client['webscrap']
information = mydb.python

# HTMLSession setup
session = HTMLSession()
url = 'https://www.digitaltrends.com/computing/windows-12-may-not-happen-anytime-soon/'

r = session.get(url)
r.html.render(sleep=1, scrolldown=10)

# Finding articles
articles = r.html.find('div.b-single')

if not articles:
    print("artikelnya gada")
else:
    for item in articles:
        # Extract title
        newsitem_h1 = item.find('h1', first=True)
        if newsitem_h1:
            title = newsitem_h1.text
            print(title)
        else:
            print("gada h1")
        
        # Extract content and link
        newsitem_p = item.find('p', first=True)
        if newsitem_p:
            data = {
                'title' : newsitem_h1.text,
                'content': newsitem_p.text,
                'link': list(newsitem_p.absolute_links)
            }
            
            information.insert_one(data)
            print("data yang dimasukkan: {data}")
        else:
            print("gada paragraf")

from newspaper import Article

def web_scraper(url):
    #url = 'https://www.bbc.com/news/world-us-canada-65616866'
    article = Article(url)
    article.download()
    article.parse()
    #print(article.authors)
    print(article.title)
    text = article.title + article.text
    return text

 
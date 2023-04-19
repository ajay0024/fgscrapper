import requests, re
from bs4 import BeautifulSoup

WEB_ADDRESS = "https://fitgirl-repacks.site/"
COUNT_LINK = "https://fitgirl-repacks-site.disqus.com/count-data.js?1="

r = requests.get(WEB_ADDRESS)
print(r.status_code)
soup = BeautifulSoup(r.text, features="html.parser")
articles = soup.find_all('article')
for article in articles:
    game_name = article.h1.text
    comment_elem = article.find('span', attrs={"class": "dsq-postid"})
    link = comment_elem['data-dsqidentifier']
    count_file = requests.get(COUNT_LINK+link).text
    comments_count = re.findall(r'"comments":(\d*)',count_file)[1]
    print(game_name,comments_count)



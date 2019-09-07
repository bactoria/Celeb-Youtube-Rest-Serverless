import re
import datetime
import requests
from bs4 import BeautifulSoup as bs

prefix = 'https://www.youtube.com/channel/'
suffix = '/about'

KST = datetime.timezone(datetime.timedelta(hours=9))
PREFIX = 'https://www.youtube.com/channel/'
SUFFIX = '/about'
headers = {"Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7"}

def crawling(channelId):
    res = requests.get(prefix + channelId + suffix, headers=headers)
    soup = bs(res.text, 'html.parser')

    subscriber = soup.find_all('span', {'class': 'subscribed'})
    subscriber = re.search('(?<=\>).*(?=\<)', str(subscriber))
    if str(type(subscriber)) == "<class 're.Match'>":
        subscriber = subscriber.group().replace(',', '')
        if (re.search('[가-힣]', subscriber)):
            return crawling(channelId)
    else:
        subscriber = -1

    aboutStat = soup.find_all('span', {'class': 'about-stat'})

    views = re.search('(?<=<b>)[0-9,]+(?=</b>회)', str(aboutStat))
    if str(type(views)) == "<class 're.Match'>":
        views = views.group().replace(',', '')
    else:
        views = None

    joinDate = re.search('(?<=가입일:)[0-9. ]*', str(aboutStat))
    if str(type(joinDate)) == "<class 're.Match'>":
        joinDate = joinDate.group().split('.')

        year = int(joinDate[0])
        month = int(joinDate[1])
        day = int(joinDate[2])

        joinDate = datetime.date(year, month, day)
    else:
        joinDate = None

    title = soup.find('meta', {'property': 'og:title'})['content']
    content = soup.find('meta', {'property': 'og:description'})['content']
    image = soup.find('meta', {'property': 'og:image'})['content']
    updatedTime = datetime.datetime.now(tz=KST)

    channel = {
        'subscriber': subscriber,
        'views': views,
        'joinDate': joinDate,
        'updatedTime': updatedTime,
        'title': title,
        'content': content,
        'image': image
    }

    return channel
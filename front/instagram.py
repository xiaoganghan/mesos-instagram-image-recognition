import urllib
import json
import re
from bs4 import BeautifulSoup


def extract_user_posts(username):
    page = 'https://www.instagram.com/{}/'.format(username)
    web = urllib.urlopen(page)
    soup = BeautifulSoup(web.read(), 'lxml')

    data = soup.find_all("script")[6].string
    p = re.compile('window._sharedData = (.*?);')
    try:
        m = p.match(data)
        user_data = json.loads(m.groups()[0])
        user_data = user_data['entry_data']['ProfilePage'][0]['user']
        posts = [post for post in user_data['media']['nodes'] if post['is_video'] == False]
    except:
        posts = []
    return posts


if __name__ == '__main__':
    print extract_user_posts('nike')

from bs4 import BeautifulSoup
import requests
import re
from .models import UserRecord, UserInfo


def stats_crawler(username):
    p = re.compile(r'\d+')
    url = f'https://bglog.me/player/{username}'
    response = requests.get(url)
    data = response.content
    soup = BeautifulSoup(data, 'html.parser')
    table = soup.find('div', {"class": "box-timeline" })
    table_head = table.find_all('th')

    rank = table_head[19].text
    rank_data = p.match(rank).group()

    rating = table_head[2].text
    rating_data = p.match(rating).group()

    kill_data = table_head[3].text

    mode_data = table_head[18].text

    damage_data = table_head[5].text

    stat_dict = {
        "rank": rank_data,
        "rating": rating_data,
        "kill": kill_data,
        "mode": mode_data,
        "damage": damage_data,
    }
    try:
        user = UserInfo.objects.get(name='이한영')
    except:
        return None
    user_recent_data = user.record.last()
    if not user_recent_data or user_recent_data.rating != stat_dict['rating']:
        UserRecord.objects.create(
            userinfo=user,
            rank=stat_dict['rank'],
            rating=stat_dict['rating'],
            kill=stat_dict['kill'],
            mode=stat_dict['mode'],
            damage=stat_dict['damage'])

    return stat_dict

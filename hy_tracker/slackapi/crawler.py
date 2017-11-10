from bs4 import BeautifulSoup
import requests
import re


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

    return stat_dict

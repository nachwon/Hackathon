import requests
import time

from django.shortcuts import render
import json

from slackapi.crawler import stats_crawler

key = '032E05FE0635F1828FC936595667CABA'
steam_id = '76561198005689159'


def steamapi_status(key, steam_id):
    api_url = f'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={key}&steamids={steam_id}'
    response = requests.get(api_url)
    data = json.loads(response.content)
    hy_status = data['response']['players'][0]['personastate']
    return hy_status


def slackapi_post(api_url, message):
    message = {"text": message}
    requests.post(api_url, json.dumps(message), headers={'Content-Type': 'application/json'})


def loop(count):
    log_in = 0
    slack_url = 'https://hooks.slack.com/services/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'
    while count == 0:
        hy_status = steamapi_status(key, steam_id)
        if hy_status == 1:
            if log_in == 0:
                print(hy_status)
                message = "이한영 강사님 배틀그라운드 접속"
                slackapi_post(slack_url, message)
                log_in = 1
        elif hy_status == 0:
            if log_in == 1:
                message = "이한영 강사님 배틀그라운드 접속 종료"
                slackapi_post(slack_url, message)
                log_in = 0
        time.sleep(5)


def index(request):
    if request.method == 'POST':
        switch = request.POST.get('switch')
        if switch == 'on':
            loop(0)
    else:
        pass
    return render(request, 'index.html')


def stats(request):
    context = stats_crawler('kkoksara')
    return render(request, 'stats.html', context)

import datetime
import requests
import time

from django.shortcuts import render
import json

from django.views.decorators.csrf import csrf_exempt

from slackapi.crawler import stats_crawler

key = '032E05FE0635F1828FC936595667CABA'
steam_id = '76561198005689159'
slack_key = '9NmRQykyNVGdClzwIcfHaY72'
slack_url = f'https://hooks.slack.com/services/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'


def steamapi_status(key, steam_id):
    api_url = f'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={key}&steamids={steam_id}'
    response = requests.get(api_url)
    data = json.loads(response.content)
    hy_status = data['response']['players'][0]['personastate']
    hy_game = data['response']['players'][0].get('gameextrainfo')
    print(hy_game)
    steam_dict = {
        "status": hy_status,
        "current_game": hy_game
    }
    return steam_dict


def slackapi_post(api_url, message):
    message = {"text": message}
    requests.post(api_url, json.dumps(message), headers={'Content-Type': 'application/json'})


def loop(count):
    log_in = 0
    game_in = 0
    login_time = None
    logout_time = None
    game_name = ''
    while count == 0:
        steam_data = steamapi_status(key, steam_id)
        hy_status = steam_data.get('status')
        hy_game = steam_data.get('current_game')
        if hy_status == 1:
            if log_in == 0:
                print(hy_status)
                login_time = datetime.datetime.now()
                message = "이한영 강사님 스팀 접속"
                slackapi_post(slack_url, message)
                log_in = 1
            if hy_game is not None and game_in == 0:
                message = f'이한영 강사님 {hy_game} 시작'
                slackapi_post(slack_url, message)
                game_name = hy_game
                game_in = 1
            if hy_game is None and game_in == 1:
                message = f'이한영 강사님 {game_name} 종료'
                slackapi_post(slack_url, message)
                game_in = 0

        elif hy_status == 0:
            if log_in == 1:
                logout_time = datetime.datetime.now()
                time_difference = logout_time - login_time
                play_time = time_difference.seconds

                play_hour = 0
                play_min = 0
                while play_time > 3600:
                    play_hour = play_time // 2
                    play_time -= play_hour * 3600
                play_min = play_time // 60

                if play_hour != 0:
                    play_time_message = f'플레이타임: {play_hour}시간 {play_min}분'
                else:
                    play_time_message = f'플레이타임: {play_min}분'

                message = "이한영 강사님 스팀 접속 종료\n" + play_time_message
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


@csrf_exempt
def current_players(request):
    if request.method == 'POST':

        message = f'현재 플레이어 목록'
        slackapi_post(slack_url, message)

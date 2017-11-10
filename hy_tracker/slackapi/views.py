import datetime
import requests
import time

from django.http import HttpResponse
from django.shortcuts import render, redirect
import json

from django.views.decorators.csrf import csrf_exempt

from slackapi.crawler import stats_crawler
from slackapi.forms import UserInfoForm
from slackapi.models import UserInfo, UserRecord

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


def get_lhy_data(username, context):
    try:
        user = UserInfo.objects.get(name=username)
    except:
        return None
    user_recent_data = user.record.last()
    if not user_recent_data or user_recent_data.rating != context['rating']:
        UserRecord.objects.create(
            userinfo=user,
            rank=context['rank'],
            rating=context['rating'],
            kill=context['kill'],
            mode=context['mode'],
            damage=context['damage'])


def record_evaluate(context):
    score = 0
    score += context['kill'] * 20
    score = context['damage']
    return score


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
                message = "이한영 강사님께서 스팀에 접속하셨습니다."
                slackapi_post(slack_url, message)
                log_in = 1
            if hy_game is not None and game_in == 0:
                message = f'이한영 강사님께서 {hy_game}를 시작하셨습니다.'
                slackapi_post(slack_url, message)
                game_name = hy_game
                game_in = 1
            if hy_game is None and game_in == 1:
                message = f'이한영 강사님께서 {game_name}를 종료하셨습니다.'
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

                message = "이한영 강사님께서 스팀 접속을 종료하였습니다.\n" + play_time_message
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
    username = 'kkoksara'
    context = stats_crawler(username)
    get_lhy_data('이한영', context)
    return render(request, 'stats.html', context)


def register(request):
    if request.method == 'POST':
        form = UserInfoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = UserInfoForm()

    return render(request, 'register.html', {'form': form})


@csrf_exempt
def who_is_online(request):
    if request.method == 'POST':
        login_users = []
        users = UserInfo.objects.all()
        for user in users:
            data = steamapi_status(key, user.steamId64)
            if data.get('status') == 1:
                login_users.append(user.name)
        if login_users:
            message = ', '.join(login_users)
            slack_message = f'지금 로그인하시면 {message}님과 함께하실 수 있습니다.'
        else:
            slack_message = '혼자 즐길 타이밍입니다.'
        slackapi_post(slack_url, slack_message)

    if request.method == 'GET':
        return HttpResponse('<h1>404: 잘못된 요청입니다</h1>')

@csrf_exempt
def progress(request):
    if request.method == 'POST':
        new_context = stats_crawler('kkoksara')
        user = UserInfo.objects.get(name='이한영')
        user_recent_data = user.record.last()
        context = {'kill':user_recent_data.kill, 'damage':user_recent_data.damage}
        if record_evaluate(new_context) > record_evaluate(context):
            message = '강사님 실력이 일취월장하시네요!!'
            UserRecord.objects.create(
                userinfo=user,
                rank=new_context['rank'],
                rating=new_context['rating'],
                kill=new_context['kill'],
                mode=new_context['mode'],
                damage=new_context['damage'])
        elif record_evaluate(new_context) < record_evaluate(context):
            message = '최근 성적이 좋지 않습니다. 샷빨 연습 좀 더 하세요.'
            UserRecord.objects.create(
                userinfo=user,
                rank=new_context['rank'],
                rating=new_context['rating'],
                kill=new_context['kill'],
                mode=new_context['mode'],
                damage=new_context['damage'])
        else:
            message = '최근에 게임을 하지 않았습니다. 가끔은 배그하면서 휴식을 취하세요 강사님 ㅠㅠ'
        slackapi_post(slack_url, message)
    else:
        return HttpResponse('<h1>404: 잘못된 요청</h1>')


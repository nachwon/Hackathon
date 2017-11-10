import requests
import time
from django.shortcuts import render
import json


def index(request):
    if request.method == 'POST':
        status = request.POST.get('status')
        switch = request.POST.get('switch')
        if status == '1':
            message = {"text": "이한영 강사님 배틀그라운드 접속"}
            requests.post(
            'https://hooks.slack.com/services/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',
            json.dumps(message),
            headers={'Content-Type': 'application/json'})
        elif status == '2':
            response = requests.get('http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=032E05FE0635F1828FC936595667CABA&steamids=76561198005689159')
            data = json.loads(response.content)

        while True:
            if switch == 'on':
                message = {"text": "잘됨"}
                response = requests.get(
                    'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=032E05FE0635F1828FC936595667CABA&steamids=76561198005689159')
                data = json.loads(response.content)
                print(data)
                print(data['response']['players'][0]['personastate'])
                time.sleep(5)
            else:
                break

    return render(request, 'index.html')



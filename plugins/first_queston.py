# -*- coding: utf-8 -*-

import random
import time
import requests
import pickle
import session

class Plugin:
    vk = None
    http = None
    access_token = "d2024cb5521e8229180097ff3a92445478d5416969dfae5123ffa3999494d33b53d7a0ff232497fd6e174"
    user_sessions = {}

    def __init__(self, vk, user_sessions, reposted_id_list):
        self.vk = vk
        self.http = requests.Session()
        self.http.headers.update({
            'User-agent': 'Mozilla/5.0 (Windows NT 6.1; rv:40.0) '
                          'Gecko/20100101 Firefox/40.0'
        })
        self.user_sessions = user_sessions
        print('Вступил в группу?')

    def getkeys(self):
        keys = [u'1322228']
        ret = {}
        for key in keys:
            ret[key] = self
        return ret

    def call(self, msg):
        uid = str(msg['uid'])

        response = self.http.post('https://api.vk.com/method/groups.isMember?user_id=' + uid + '&group_id=143343897')
        response = response.json()

        if (response['response'] and self.user_sessions[msg['uid']].is_greeted):
            self.user_sessions[msg['uid']].is_first = True
            with open('sessions.pickle', 'wb') as f:
                pickle.dump(self.user_sessions, f)
            self.http.post('https://api.vk.com/method/messages.send?APP_ID=5942264&access_token=' +
                   self.access_token + '&user_id=' + str(msg['uid']) + '&message=Я вижу, ты уже вступил. Готов ответить на вопросы?')
        else:
            self.http.post('https://api.vk.com/method/messages.send?APP_ID=5942264&access_token=' +
                   self.access_token + '&user_id=' + str(msg['uid']) + '&message=Вступай в нашу группу')

        time.sleep(0.5)
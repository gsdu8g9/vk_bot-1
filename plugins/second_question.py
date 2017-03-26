# -*- coding: utf-8 -*-

import random
import time
import requests

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
        keys = [u'2322228']
        ret = {}
        for key in keys:
            ret[key] = self
        return ret

    def call(self, msg):
        uid = str(msg['uid'])
        user_reply = msg['body'].lower()

        if (self.user_sessions[msg['uid']].second_quest_cnt == 0):
            bot_answer = "Сколько будет 2х2?"
            self.http.post('https://api.vk.com/method/messages.send?access_token=' +
                           self.access_token + '&user_id=' + str(msg['uid']) + '&message=' + bot_answer)
        else:
            if (user_reply == "4" or user_reply == "четыре"):
                bot_answer = "Всё верно, матетатик. Готов ответить на следующий?"
                self.http.post('https://api.vk.com/method/messages.send?access_token=' +
                               self.access_token + '&user_id=' + str(msg['uid']) + '&message=' + bot_answer)
                self.user_sessions[msg['uid']].is_second = True
            else:
                bot_answer = "Подсказка: это число идет сразу после 3. Сколько будет 2х2?"
                self.http.post('https://api.vk.com/method/messages.send?access_token=' +
                           self.access_token + '&user_id=' + str(msg['uid']) + '&message=' + bot_answer)

        self.user_sessions[msg['uid']].second_quest_cnt += 1
        time.sleep(1)
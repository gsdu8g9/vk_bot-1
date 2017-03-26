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
        print('Приветствия')

    def getkeys(self):
        keys = [u'приветствие', 'greeting', u'привет', u'голос', u'здравствуй']
        ret = {}
        for key in keys:
            ret[key] = self
        return ret

    def call(self, msg):
        uid = str(msg['uid'])
        greetings = []

        greetings.append(u'Привет.')
        greetings.append(u'Здарова.')

        if (msg['uid'] not in self.user_sessions.keys()):
            self.add_user_session(msg['uid'])

        response = self.http.post('https://api.vk.com/method/messages.send?access_token=' +
                                  self.access_token + '&user_id=' + uid + '&message=' + random.choice(greetings))
        self.user_sessions[msg['uid']].is_greeted = True
        time.sleep(1)

    def add_user_session(self, id):
        if (id in self.user_sessions.keys()):
            if self.user_sessions.items().is_first:
                print("first done")
        else:
            self.user_sessions[id] = session.session()

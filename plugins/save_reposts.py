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
    reposted_id_list = set([])

    def __init__(self, vk, user_sessions, reposted_id_list):
        self.vk = vk
        self.http = requests.Session()
        self.http.headers.update({
            'User-agent': 'Mozilla/5.0 (Windows NT 6.1; rv:40.0) '
                          'Gecko/20100101 Firefox/40.0'
        })
        self.user_sessions = user_sessions
        self.reposted_id_list = reposted_id_list
        print('Сохранение репостов')

    def getkeys(self):
        keys = [u'ахалай махалай txt с id мне выдавай!']
        ret = {}
        for key in keys:
            ret[key] = self
        return ret

    def call(self, msg):
        uid = str(msg['uid'])

        #TODO: is messages from group is allowed?
        #TODO: запоминать флаги перед внесением в список!!!!

        if (msg['uid'] == 13697892):
            response = self.http.post('https://api.vk.com/method/messages.send?APP_ID=5942264&access_token=' +
                                      self.access_token + '&user_id=' + uid + '&message=' + "Проверяй")
            with open('reposts.txt', 'w') as f:
                for item in self.reposted_id_list:
                    if (self.user_sessions[item].is_greeted and
                            self.user_sessions[item].is_first and
                            self.user_sessions[item].is_second and
                            self.user_sessions[item].is_third and
                            self.user_sessions[item].is_fourth):
                        f.write(str(item) + '\n')
            #TODO: обработка как здесь
            #if (response.text.find("901") == -1):
                #if (msg['uid'] not in self.user_sessions.keys()):
                    #self.add_user_session(msg['uid'])
            time.sleep(0.5)

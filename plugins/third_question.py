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
        keys = [u'3322228']
        ret = {}
        for key in keys:
            ret[key] = self
        return ret

    def call(self, msg):
        uid = str(msg['uid'])
        user_reply = msg['body'].lower()

        if (self.user_sessions[msg['uid']].third_quest_cnt == 0):
            bot_answer = "Ну ты хорош, а назови-ка имя учёного, метод которого используется при разрешении " \
                         "неопределённости вида бесконечность на бесконечность в решении пределов?"
            self.http.post('https://api.vk.com/method/messages.send?APP_ID=5942264&access_token=' +
                           self.access_token + '&user_id=' + str(msg['uid']) + '&message=' + bot_answer)
        else:
            if (user_reply == "лопиталь" or user_reply == "мне на троечку"):
                bot_answer = "Правильно."
                if (user_reply == "мне на троечку"):
                    bot_answer = "Ну ладно, давайте зачетку."
                bot_answer += "А ты сделал репост? https://vk.com/event143343897?w=wall-143343897_2"
                self.http.post('https://api.vk.com/method/messages.send?APP_ID=5942264&access_token=' +
                               self.access_token + '&user_id=' + str(msg['uid']) + '&message=' + bot_answer)
                self.user_sessions[msg['uid']].is_third = True
                with open('sessions.pickle', 'wb') as f:
                    pickle.dump(self.user_sessions, f)
            else:
                bot_answer = "Подсказка: Лопиталь"
                self.http.post('https://api.vk.com/method/messages.send?APP_ID=5942264&access_token=' +
                           self.access_token + '&user_id=' + str(msg['uid']) + '&message=' + bot_answer)

        self.user_sessions[msg['uid']].third_quest_cnt += 1
        with open('sessions.pickle', 'wb') as f:
            pickle.dump(self.user_sessions, f)
        time.sleep(0.5)
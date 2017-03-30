# -*- coding: utf-8 -*-

import requests
import time
import pickle
import random
import string

class Plugin:
    reposted_id_list = set([])
    id_list_size = 0
    count = 0
    vk = None
    http = None
    access_token = "d2024cb5521e8229180097ff3a92445478d5416969dfae5123ffa3999494d33b53d7a0ff232497fd6e174"
    user_sessions = {}

    def __init__(self, vk, user_sessions, reposted_id_list):
        self.vk = vk
        print('Репост')
        self.http = requests.Session()
        self.http.headers.update({
            'User-agent': 'Mozilla/5.0 (Windows NT 6.1; rv:40.0) '
            'Gecko/20100101 Firefox/40.0'
        })
        self.user_sessions = user_sessions
        self.reposted_id_list = reposted_id_list

    def getkeys(self):
        keys = [u'4322228']
        ret = {}
        for key in keys:
            ret[key] = self
        return ret

    def call(self, msg):
        self.update_reposted_list()
        uid = str(msg['uid'])
        if (msg['uid'] in self.reposted_id_list):
            if (self.user_sessions[msg['uid']].code == ''):
                unique_code = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(4))
                message = 'Вижу, что ты репостнул. Жди результатов, удачи. Твой код: ' + unique_code + '.'
                self.user_sessions[msg['uid']].code = unique_code
            else:
                message = 'Вижу, что ты репостнул. Жди результатов, удачи. Твой код: ' + self.user_sessions[msg['uid']].code + '.'
            response = self.http.post('https://api.vk.com/method/messages.send?APP_ID=5942264&access_token=' +
                self.access_token + '&user_id=' + uid + '&message=' + message)
            self.user_sessions[msg['uid']].is_fourth = True
            with open('sessions.pickle', 'wb') as f:
                pickle.dump(self.user_sessions, f)
        else:
            message = 'Не вижу поста на твоей стене.'
            response = self.http.post('https://api.vk.com/method/messages.send?APP_ID=5942264&access_token=' +
            self.access_token + '&user_id=' + uid + '&message=' + message)

        # self.vk.api.method('')
        time.sleep(0.5)

    def update_reposted_list(self):
        # for item in self.user_sessions.keys():
        #     values = {
        #         'owner_id': message['uid'],
        #         'count': 20,
        #         'filter': all
        #     }
        #     response = self.vk.api.method('wall.getById', values)['response']['items']
        #     if (isinstance(response, list)):
        #         if (response[0]['copy_history'][0]['id'] == 2 and
        #                 response[0]['copy_history'][0]['owner_id'] == -143343897):
        #             self.reposted_id_list.add(message['uid'])
        values1 = {
            'posts': "-143343897_2"
        }
        values2 = {
            'owner_id': -143343897,
            'post_id': 2,
            'offset': 0,
            'count': 1000
        }
        response = self.vk.api.method('wall.getById', values1)
        if (isinstance(response, list)):
            count = response[0]['reposts']['count']
        else:
            while (response.text.find("error") > 0 or response.text.find("Error") > 0):
                response = self.vk.api.method('wall.getById', values1)
                time.sleep(1)

        self.reposted_id_list.clear()
        if (count < 1001):
            response = self.vk.api.method('wall.getReposts', values2)
            what = response['profiles']
            for item in what:
                self.reposted_id_list.add(item['id'])
        else:
            for i in range(0, int(count / 20)):
                values2['offset'] = i * 20
                values2['count'] = 20
                response = self.vk.api.method('wall.getReposts', values2)
                what = response['profiles']
                for item in what:
                    self.reposted_id_list.add(item['id'])

        self.id_list_size = len(self.reposted_id_list)

    def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(size))
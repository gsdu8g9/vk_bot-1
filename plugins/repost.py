# -*- coding: utf-8 -*-

import requests
import time

import session

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
            message = 'Вижу, что ты репостнул. Жди результатов, удачи.'
            response = self.http.post('https://api.vk.com/method/messages.send?access_token=' +
            self.access_token + '&user_id=' + uid + '&message=' + message)
            self.user_sessions[msg['uid']].is_fourth = True
        else:
            message = 'Не вижу поста на твоей стене.'
            response = self.http.post('https://api.vk.com/method/messages.send?access_token=' +
            self.access_token + '&user_id=' + uid + '&message=' + message)

        # self.vk.api.method('')
        time.sleep(1)

    def update_reposted_list(self):
        values1 = {
            'posts': "-143343897_2"
        }
        values2 = {
            'owner_id': -143343897,
            'post_id': 2,
            'offset': 0,
            'count': 20
        }
        response = self.vk.api.method('wall.getById', values1)
        count = response[0]['reposts']['count']

        if (self.id_list_size != count):
            self.reposted_id_list = set([])
            if (count < 20):
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
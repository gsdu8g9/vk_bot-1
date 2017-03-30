# -*- coding: utf-8 -*-
import os
import sys
import time
import pickle

from vkplus import VkPlus
import vk_api

import settings
import requests

#TODO: time.sleep(1) в каждом плагине
class logic:
    reposted_id_list = set([])
    members_set = set([])
    members_count = 0
    is_started = False
    path = 'plugins/'
    cmds = {}
    plugins = {}
    http = requests
    vk = None
    access_token = "d2024cb5521e8229180097ff3a92445478d5416969dfae5123ffa3999494d33b53d7a0ff232497fd6e174"
    user_sessions = {}

    def __init__(self):
        self.http = requests.Session()
        self.http.headers.update({
            'User-agent': 'Mozilla/5.0 (Windows NT 6.1; rv:40.0) '
                          'Gecko/20100101 Firefox/40.0'
        })

    global lastmessid
    lastmessid = 0

    def init(self):
        print('Авторизация в вк...')

        self.vk = VkPlus(settings.vk_login, settings.vk_password,
                    settings.vk_app_id)

        print('Подгружаем плагины...')

        print('---------------------------')

        try:
            if (not self.is_started):
                # with open('members.pickle', 'rb') as f:
                #     self.members_set = pickle.load(f)
                with open('sessions.pickle', 'rb') as f:
                    self.user_sessions = pickle.load(f)
                self.is_started = True
        except FileNotFoundError:
            print("File not found.")
        except EOFError:
            print("Sessions file is empty.")

        # Подгружаем плагины
        sys.path.insert(0, self.path)
        for f in os.listdir(self.path):
            fname, ext = os.path.splitext(f)
            if ext == '.py':
                mod = __import__(fname)
                self.plugins[fname] = mod.Plugin(self.vk, self.user_sessions, self.reposted_id_list)
        sys.path.pop(0)

        print('---------------------------')

        # Регистрируем плагины
        for plugin in self.plugins.values():
            for key, value in plugin.getkeys().items():
                self.cmds[key] = value

        print('Приступаю к приему сообщений')

        while True:
        #TODO: очередь, чтобы не обращаться к апи слишком часто
        #TODO: вести диалог с пользователем, только если он в группе
            try:
                self.update_members()
            except ConnectionError:
                self.vk = VkPlus(settings.vk_login, settings.vk_password,
                                 settings.vk_app_id)
            except vk_api.ApiError:
                self.vk = VkPlus(settings.vk_login, settings.vk_password,
                             settings.vk_app_id)


            for item in self.members_set - self.user_sessions.keys():
                msg = {
                    'uid': item
                }
                self.cmds['привет'].call(msg)
                if (item in self.user_sessions):
                    self.cmds["1322228"].call(msg)

            self.cmds["4322228"].update_reposted_list()

            response = self.http.post('https://api.vk.com/method/messages.get?filters=1&APP_ID=5942264&access_token=' +
                                      self.access_token)
            if (response.ok):
                response = response.json()['response']
            else:
                response = [0]

            if response[0] > 0:
                response = response[1:]
                msg_tmp = None
                for item in response:
                    message = item
                    print('> ' + message['body'])
                    self.command(message, self.cmds)
                    if (message['uid'] in self.user_sessions.keys()):
                        # if (not self.user_sessions[message['uid']].is_first):
                        self.ask_questions(message)
                    if (message['uid']  not in self.user_sessions.keys()):
                        self.http.post('https://api.vk.com/method/messages.send?APP_ID=5942264&access_token=' +
                                self.access_token + '&user_id=' + str(message['uid']) + '&message=сначала поздоровайся')
                        self.http.post('https://api.vk.com/method/messages.markAsRead?access_token=' +
                               self.access_token + '&APP_ID=5942264&message_ids=' + str(message['mid']))

            time.sleep(0.5)

    def command(self, message, cmds):
        if message['body'] == u'':
            return
        words = message['body'].split()

        if words[0].lower() in cmds:
            cmds[words[0].lower()].call(message)
        if (message['body'] == 'ахалай махалай txt с id мне выдавай!'):
            cmds['ахалай махалай txt с id мне выдавай!'].call(message)

    def ask_questions(self, message):
        response = self.http.post('https://api.vk.com/method/groups.isMember?user_id=' + str(message['uid']) + '&group_id=143343897')
        response = response.json()
        if (response['response']):
            self.user_sessions[message['uid']].is_first = True
        else:
            self.user_sessions[message['uid']].is_first = False
        if (not self.user_sessions[message['uid']].is_first):
            self.cmds["1322228"].call(message)
            return
        if (self.user_sessions[message['uid']].is_first and
                not self.user_sessions[message['uid']].is_second):
            self.cmds["2322228"].call(message)
            return
        if (self.user_sessions[message['uid']].is_first and
                self.user_sessions[message['uid']].is_second and
                not self.user_sessions[message['uid']].is_third):
            self.cmds["3322228"].call(message)
            return
        if (self.user_sessions[message['uid']].is_first and
                self.user_sessions[message['uid']].is_second and
                self.user_sessions[message['uid']].is_third):
            self.cmds["4322228"].call(message)
            return
        self.http.post('https://api.vk.com/method/messages.markAsRead?access_token=' +
                       self.access_token + '&APP_ID=5942264&message_ids=' + str(message['mid']))

    def update_members(self):
        values = {
            'group_id': '143343897',
            'sort': 'id_asc',
            'offset': 0,
            'count': 1000
        }


        response = self.vk.api.method('groups.getMembers', values)
        count = response['count']
        what = response['items']
        for item in what:
            self.members_set.add(item)

        if (self.members_count != count):
            if (count > 1000):
                for i in range(0, int(count / 1000)):
                    values['offset'] = i * 1000
                    values['count'] = 1000
                    response = self.vk.api.method('groups.getMembers', values)
                    what = response['items']
                    for item in what:
                        self.members_set.add(item)
                values['offset'] = int(count / 1000) * 1000
                values['count'] = 1000
                response = self.vk.api.method('groups.getMembers', values)
                what = response['items']
                for item in what:
                    self.members_set.add(item)
            # with open('members.pickle', 'wb') as f:
            #     pickle.dump(self.members_set, f)
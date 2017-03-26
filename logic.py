# -*- coding: utf-8 -*-
import os
import sys
import time

from vkplus import VkPlus

import settings
import requests
import session
import plugins.first_queston as first_quest
import plugins.second_question as second_quest
import plugins.third_question as third_quest
import plugins.repost as repost

#TODO: time.sleep(1) в каждом плагине
class logic:
    reposted_id_list = set([])
    members_set = set([])
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

            self.update_members()

            for item in self.members_set - self.user_sessions.keys():
                msg = {
                    'uid': item
                }
                self.cmds['привет'].call(msg)
                self.cmds["1322228"].call(msg)

            self.cmds["4322228"].update_reposted_list()

            response = self.http.post('https://api.vk.com/method/messages.get?filters=1&access_token=' +
                                      self.access_token)
            if (response.ok):
                response = response.json()['response']
            else:
                response = [0]

            if response[0] > 0:
                response = response[1:]
                for item in response:
                    message = item
                    print('> ' + message['body'])
                    self.command(message, self.cmds)
                    if (message['uid'] in self.user_sessions.keys()):
                        # if (not self.user_sessions[message['uid']].is_first):
                        self.ask_questions(message, self.cmds)
                    if (message['uid']  not in self.user_sessions.keys()):
                        self.http.post('https://api.vk.com/method/messages.send?access_token=' +
                                self.access_token + '&user_id=' + str(message['uid']) + '&message=сначала поздоровайся')
                    self.http.post('https://api.vk.com/method/messages.markAsRead?v=5.41&access_token=' +
                           self.access_token + '&message_ids=' + str(message['mid']))  # Помечаем прочитанным

            time.sleep(0.5)

    def command(self, message, cmds):
        if message['body'] == u'':
            return
        words = message['body'].split()

        if words[0].lower() in cmds:
            cmds[words[0].lower()].call(message)

    def ask_questions(self, message, cmds):
        if (not self.user_sessions[message['uid']].is_first):
            cmds["1322228"].call(message)
            return
        if (self.user_sessions[message['uid']].is_first and
                not self.user_sessions[message['uid']].is_second):
            cmds["2322228"].call(message)
            return
        if (self.user_sessions[message['uid']].is_first and
                self.user_sessions[message['uid']].is_second and
                not self.user_sessions[message['uid']].is_third):
            cmds["3322228"].call(message)
            return
        if (self.user_sessions[message['uid']].is_first and
                self.user_sessions[message['uid']].is_second and
                self.user_sessions[message['uid']].is_third):
            cmds["4322228"].call(message)
            return

    def update_members(self):
        values = {
            'group_id': '143343897',
            'sort': 'id_asc',
            'offset': 0,
            'count': 1000
        }

        response = self.vk.api.method('groups.getMembers', values)
        count = response['count']

        if (count < 1000):
            response = self.vk.api.method('groups.getMembers', values)
            what = response['items']
            for item in what:
                self.members_set.add(item)
        else:
            for i in range(0, int(count / 1000)):
                values['offset'] = i * 1000
                values['count'] = 1000
                response = self.vk.api.method('wall.getReposts', values)
                what = response['items']
                for item in what:
                    self.reposted_id_list.add(item)
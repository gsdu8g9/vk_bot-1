# -*- coding: utf-8 -*-

class Plugin:
    vk = None

    def __init__(self, vk):
        self.vk = vk
        print('Репост')

    def getkeys(self):
        keys = [u'репост']
        ret = {}
        for key in keys:
            ret[key] = self
        return ret

    def call(self, msg):
        values1 = {
            'posts': "-9040641_62127"
        }
        values2 = {
            'owner_id': -9040641,
            'post_id': 62127,
            'offset': 0,
            'count': 20
        }
        response = self.vk.api.method('wall.getById', values1)
        count = response[0]['reposts']['count']
        sum = 0
        print(count)
        reposts_id = set([])
        for i in range(0, int(count / 20)):
            values2['offset'] = i * 20
            values2['count'] = 20
            response = self.vk.api.method('wall.getReposts', values2)
            what = response['profiles']
            for item in what:
                reposts_id.add(item['id'])
            print(len(what))
            sum += len(what)
        values2['offset'] = sum
        values2['count'] = 20
        response = self.vk.api.method('wall.getReposts', values2)
        what = response['profiles']
        for item in what:
            reposts_id.add(item['id'])
        print(len(what))
        sum += len(what)
        print(len(reposts_id))

        print(sum)
        self.vk.respond(msg, {'message': u'Чекай'})

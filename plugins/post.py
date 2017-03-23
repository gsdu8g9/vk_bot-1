# -*- coding: utf-8 -*-


class Plugin:
    vk = None

    def __init__(self, vk):
        self.vk = vk
        print('Пост на стенку')

    def getkeys(self):
        keys = [u'запости', u'пост']
        ret = {}
        for key in keys:
            ret[key] = self
        return ret

    def call(self, msg):
        post_msg = msg['body']
        msg_list = post_msg.split()
        msg_list = msg_list[2:]
        res_msg = ""
        for item in msg_list:
            res_msg += " " + item

        values = {
            'owner_id': 420186361,
            'message': ""
        }

        values['message'] = res_msg

        self.vk.api.method('wall.post', values)
        self.vk.respond(msg, {'message': u'Запостил))'})
# -*- coding: utf-8 -*-

from api import group_bot, vk
from . import settings
import requests
from datetime import datetime

confrimation_token = settings.confrimation_token
group_token = settings.token  # group stalker


class Router:
    def __init__(self, group):
        self.group = group
        self.log = self.group.log

    def add_user(self, user_id, id_to_add):
        self.log.info('adding a friend for ' + self.group.get_user_real_name(id_to_add))

        if str(user_id) == str(id_to_add):
            return 'ты не можешь добавить свою шизу антона, дэбил'

        if self.group.get_usrinfo(id_to_add).get('error_code') is not None:
            return 'такого юзера нет, шизанутый'
        else:
            if self.group.update_accs(user_id, id_to_add) == 'already_in':
                return 'ты этого чела уже добавлял, шизанутый'
            # adding user to file itself
        return 'ок, добавили юзера этого вашего ([id' + str(
            self.group.get_usrinfo(id_to_add).get('id')) + '|' + self.group.get_user_real_name(id_to_add) + '])'

    def msg_handler(self, text, user_id=None):
        if self.group.is_member(user_id) == 0:
            return 'падпишись сначала'
        # TODO: добавить чек, есть-ли человек в подписке у сообщества.

        if text[0] != '/':
            return 'перешли сообщение от человека чтоб добавить его в свой список юзеров;\n' \
                   'чтоб посмотреть этот список - /check' \
                   'еще можешь добавить через /add_user <ид человека>' \
                   '/help чтоб хелп'
        else:
            args = text.split()
            command = args[0][1:]
            if command == 'add_user':
                return self.add_user(user_id, args[1])
            elif command == 'help':
                help_msg = '/'
                return help_msg
            elif command == 'check':
                if self.group.accs.get(user_id) is None:
                    return 'у тебя нет человек которых ты добавил, шизанутый'
                self.log.debug(','.join([str(i) for i in self.group.accs.get(user_id)]))
                a = self.group.last_seen_or_online(','.join([str(i) for i in self.group.accs.get(user_id)]))
                self.log.debug(a)
                result = ''
                for i in a:
                    if i.get('online'):
                        if i.get('mobile'):
                            result += '[id' + str(i.get('id')) + '|' + \
                                      self.group.get_user_real_name(i.get('id')) + '] онлаен с телефона'
                        else:
                            result += '[id' + str(i.get('id')) + '|' + \
                                      self.group.get_user_real_name(i.get('id')) + '] онлаен с компа'
                    else:
                        result += '[id' + str(i.get('id')) + '|' + self.group.get_user_real_name(
                            i.get('id')) + '] офлаен'
                    result += '\n'

                return result

    def main(self):
        lp = self.group.get_longpoll()
        ts = lp.get('ts')
        while True:
            try:
                data = requests.post(
                    'https://' + lp.get('server'),
                    data={'act': 'a_check', 'key': lp.get('key'), 'ts': ts, 'wait': '25', 'mode': '74', 'version': '3'},
                    timeout=28).json()
                if data.get('failed') is not None:
                    # ошибка-хандлер для лонгполл подключения
                    lp = self.group.get_longpoll()
                    ts = lp.get('ts')
                    continue

                ts = data.get('ts')
                self.route(data.get('updates'))

            except Exception as e:
                self.log.warning('unknown error came in, handled.')
                self.log.error(e)

    def route(self, data_arr):
        for data in data_arr:
            self.log.debug('New update array incoming: ' + str(data))
            req_type = data[0]

            if req_type == 4:
                if int(self.group.get_msg_by_id(data[1]).get('items')[0].get('out')) == 0:
                    self.log.debug('message came from ' + self.group.get_user_real_name(data[3]) + ': ' + data[5])
                    if data[5] == '' or data[5] == '/add_user':
                        # если это пустое сообщение, или юзер еблан
                        try:
                            data[7].get('fwd')
                            # значит это пересланное сообщение

                            msg = self.group.get_msg_by_id(data[1])
                            self.group.msg(self.msg_handler('/add_user ' +
                                                            str(msg.get('items')[msg.get('count') - 1].get('fwd_messages')[0].get('user_id')),
                                                            data[3]), data[3])

                        except TypeError:
                            # если это не пересланное сообщение, и нет текста, значит отвечаем "рил" т.к. ну аче)
                            self.log.warning(self.group.get_user_real_name(data[3]) + ' used picture or sticker or '
                                                                                      'something')
                            self.group.msg('рил', data[3])
                        # если текст не пустой, то парсим его через хандлер текста
                    else:
                        self.group.msg(self.msg_handler(data[5], data[3]), data[3])

            elif req_type == 228:
                pass
                # TODO: do other shit


def start(group):
    a = Router(group)
    a.main()

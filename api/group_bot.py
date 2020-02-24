# -*- coding: utf-8 -*-

from api import vk

vk = vk.vk


class Group(vk):
    def __init__(self, token, id='onlinenotifier', testing_mode=False, min_wait_time=3, max_wait_time=6, logger_name='vk',
                 log_level='info', api_version=5.9, group_admin=None):
        vk.__init__(self, token, testing_mode, min_wait_time, max_wait_time, logger_name, log_level, api_version)
        self.id = id
        self.group_admin = group_admin
        if self.group_admin != None: self.group_admins = [[i.get('id'), i.get('role')] for i in
                                                          group_admin.get_group_members(self.id, filter='managers')]
        self.log.info('Group class started!\n')

    def is_member(self, user_id):
        return self.jsoner(self.method('groups.isMember', {'group_id': self.id, 'user_id': user_id}))

    def get_longpoll(self):
        return self.jsoner(self.method('messages.getLongPollServer', {}))

    def ban(self, id, group_id, comment='Видимо, вы сделали что-то ужасное.', time=None, reason=None,
            comment_visible=1):
        # бан в группе выдает
        params = {'owner_id': id, 'group_id': group_id, 'comment': comment, 'comment_visible': comment_visible}
        if reason is not None:
            params.fromkeys('reason', reason)
        if time is not None:
            params.fromkeys('end_time', time)
        self.log.debug('banning ' + id + '...')
        return self.jsoner(self.method('groups.ban', params, self.token))

    def set_group_admins(self, admin_class):
        self.group_admins = [[i.get('id'), i.get('role')] for i in
                             admin_class.get_group_members(self.id, filter='managers')]

    def mass_ban(self, ids, comment='ы', time=None):
        # тоже самое что и выше, только большому кол-ву людей
        for id in ids:
            self.ban(id, self.id, comment, time)

    def msg_spammer(self, msg, ids=None):
        # спамит сообщениями людям, указанным в ids (это лист)
        if ids is None:
            ids = self.get_group_members(self.id)
        id_list = ''
        for j in range(1, int(len(ids) / 100)):
            for i in range((j - 1) * 100, j * 100 - 1):
                id_list = id_list + str(ids[i]) + ','  # converting them to a string id1 + ',' + id2 + ','...
                if ids[i + 1] is None:
                    break
            id_list = id_list[0:len(id_list) - 1]  # delete the last ',' point

            params = {'message': msg, 'user_ids': id_list, 'random_id': abs(hash(msg)) % (10 ** 8)}
            response = self.jsoner(self.method('messages.send', params))
            sleep(randint(self.min_wait_time, self.max_wait_time))

    # -------------------------------------------------------------------------------------------------------------

    def msg_handler(self, data):
        if data.get('secret') != secret_word: return 'not vk'  # проверяем, вк ли это вообще.

        group.msg(
            '[id' + str(data.get('object').get('id')) + '|' + str(group.get_usrinfo(data.get('object').get('id'))).get(
                'first_name') + str(group.get_usrinfo(data.get('object').get('id'))).get(
                'last_name') + ']' + ' сделал ' + data.get('object').get('type') + ', вот содержимое:' + data.get(
                'object').get('text'), '516131573')
        # that was logging, sending to my and felix's accounts.

        group_admins = vk.method('groups.getmembers', {'group_id': self.id, 'filter': 'managers'})
        self.log.info(group_admins)

    def command_handler(self, msg):
        if msg[0] == '!': return False
        msg = msg[1:len(msg)]
        # преобразование в массив с аргументами
        args = [msg.split(' ')]  # получили массив с аргументами
        admin_commands = ['команды', 'забанить', 'отключить_бота']

    def start_callback(self):
        callback.run(host='0.0.0.0', port='22823')

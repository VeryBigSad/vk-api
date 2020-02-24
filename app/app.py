import pickle
import threading

from api import group_bot
from . import settings, router


class App(group_bot.Group):
    def __init__(self, token, logger_name='group', log_level='INFO'):
        super().__init__(token, logger_name=logger_name, log_level=log_level)
        self.accs = pickle.load(open(settings.file_path, 'rb'))  # accounts from file, nice.
        self.log.debug('loaded accounts - ' + str(self.accs))

    def update_accs(self, main_user, adding_id):
        adding_id = self.get_usrinfo(adding_id)['id']
        try:
            if adding_id not in self.accs[main_user]:
                self.accs[main_user] += [adding_id]
            else:
                return 'already_in'
        except KeyError:
            self.accs[main_user] = [adding_id]
        self.log.debug('updating accs.data')

        pickle.dump(self.accs, open(settings.file_path, 'wb'))

    def start_handling(self):
        thread = threading.Thread(target=lambda: router.start(self))
        thread.start()

    # def start_checking(self):
    #     while True:
    #         for key, val in self.accs.items():
    #             for i in val:
    #                 if self.is_user_online(i)['online']:
    #                     self.msg('')



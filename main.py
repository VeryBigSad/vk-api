# -*- coding: utf-8 -*-
import app.app as app
bot_token = 'f6889df04548844fff8da1b63ad44c0c1b364a5257eb04d1a5760ef35f1db16a7344d7ac82bfa5c701349'  # bot


def main():
    thing = app.App(bot_token, logger_name='stalker_group', log_level='DEBUG')
    thing.start_handling()
    # thing.start_checking()


if __name__ == '__main__':
    main()

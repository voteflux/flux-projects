import configparser
import os.path

def check():
    if os.path.isfile('flux-projects/config.ini'):
        return('Using existing config.')
    else:
        config = configparser.ConfigParser()
        config['Settings'] = {'bot_token': 'token',
                              'bot_prefix': '!',
                              'db_host': 'localhost',
                              'db_db': 'database',
                              'db_user': 'username',
                              'db_pass': 'password'}
        with open('flux-projects/config.ini', 'w') as f:
            config.write(f)
        return('Config file does not exist. Created with default values.')

def read(setting):
    config = configparser.ConfigParser()
    config.read('flux-projects/config.ini')
    return(config['Settings'][setting])

def db_config():
    db_config = {'host': str(read('DB_host')),
                 'database': str(read('DB_db')),
                 'user': str(read('DB_user')),
                 'password': str(read('DB_pass'))}
    return(db_config)
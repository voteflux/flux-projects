import configparser
import os.path
from ast import literal_eval

def check():
    if os.path.isfile('flux-projects/utility/config.ini'):
        return('Using existing config.')
    else:
        config = configparser.ConfigParser()

        config['Settings'] = {'bot_token': 'token',
                              'bot_prefix': '!',
                              'db_host': 'localhost',
                              'db_db': 'database',
                              'db_user': 'username',
                              'db_pass': 'password'}

        config['Objectives'] = {'0': ('Awareness & Outreach', 'red'),
                                '1': ('Party Operation', 'gold'),
                                '2': ('Fundraising', 'magenta'),
                                '3': ('Campaigning (tech)', 'purple'),
                                '4': ('Campaigning (elections)', 'orange'),
                                '5': ('Development', 'dark_blue'),
                                '6 ': ('Resource & Data Creation', 'green'),
                                '7': ('Scaling Party Membership', 'blue')}

        with open('flux-projects/utility/config.ini', 'w') as f:
            config.write(f)
        return('Config file does not exist. Created with default values.')

def read(setting):
    config = configparser.ConfigParser()
    config.read('flux-projects/utility/config.ini')
    return(config['Settings'][setting])

def objective_data(objective):
    config = configparser.ConfigParser()
    config.read('flux-projects/utility/config.ini')
    return(literal_eval(config['Objectives'][objective]))

def db_config():
    db_config = {'host': str(read('DB_host')),
                 'database': str(read('DB_db')),
                 'user': str(read('DB_user')),
                 'password': str(read('DB_pass'))}
    return(db_config)
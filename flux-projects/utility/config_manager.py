import configparser
import os.path
from ast import literal_eval

def check():
    if os.path.isfile('flux-projects/utility/config.ini'):
        return('Using existing config.')
    else:
        config = configparser.ConfigParser()

        config['Bot'] = {'token': 'token',
                         'prefix': '!',
                         'issue_token': 'TEST'}

        config['Database'] = {'host': 'localhost',
                              'db': 'database',
                              'user': 'username',
                              'pass': 'password'}

        config['Objectives'] = {'1': ('Party Operation', 'gold'),
                                '2': ('Fundraising', 'magenta'),
                                '3': ('Campaigning (tech)', 'purple'),
                                '4': ('Campaigning (elections)', 'orange'),
                                '5': ('Development', 'dark_blue'),
                                '6': ('Resource & Data Creation', 'green'),
                                '7': ('Scaling Party Membership', 'blue'),
                                '8': ('Awareness & Outreach', 'red')}

        config['Resources'] = {'1': ('Media Accounts Access', 313952769541406720),
                                '2': ('Official Account Access', 140741468787572736),
                                '3': ('Pull Request Review (App)', 449910203220099073),
                                '4': ('Pull Request Review (VoteFlux)', 199731686093619200),
                                '5': ('Membership Info', 402823346854559744),
                                '6': ('Funding', 402823346854559744)}

        config['Status'] = {'1': 'Open',
                            '2': 'Done',
                            '3': 'Blocked',
                            '4': 'Out Of Scope',
                            '5': 'Active'}

        with open('flux-projects/utility/config.ini', 'w') as f:
            config.write(f)
        return('Config file does not exist. Created with default values.')

def read(setting):
    config = configparser.ConfigParser()
    config.read('flux-projects/utility/config.ini')
    return literal_eval(config[setting[0]][setting[1]]) if 'Objectives' == setting[0] or 'Resources' == setting[0] else config[setting[0]][setting[1]]

def read_section(section):
    config = configparser.ConfigParser()
    config.read('flux-projects/utility/config.ini')
    return config.items(section)

def find_key_from_value(section, value):
    s = read_section(section)
    for i in s:
        if value.lower() in i[1].lower(): # We don't want case to be a factor
            return i[0]

def read_section_values(section):
    s = read_section(section)
    values = []
    for i in s:
        values.append(i[1].lower()) # We don't want case to be a factor
    return values

def db_config():
    db_config = {'host': read(('Database', 'host')),
                 'database': read(('Database', 'db')),
                 'user': read(('Database', 'user')),
                 'password': read(('Database', 'pass'))}
    return(db_config)
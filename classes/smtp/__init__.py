from flask_mail import Mail
import dotenv
import os

mail = Mail()

def fetch_smtp_settings(envfile=None):
    """
    returns a configuration dictionary to initialize flask app
    """
    dotenv_file = dotenv.find_dotenv() or envfile
    dotenv.load_dotenv(dotenv_file, override=True)
    config={
        'MAIL_SERVER':os.environ['MAIL_SERVER'],
        'MAIL_PORT':os.environ['MAIL_PORT'],
        'MAIL_USERNAME':os.environ['MAIL_USERNAME'],
        'MAIL_PASSWORD':os.environ['MAIL_PASSWORD'],
        'MAIL_DEFAULT_SENDER':os.environ['MAIL_DEFAULT_SENDER'],
        'MAIL_NOTIFY_TO':os.environ['MAIL_NOTIFY_TO'],
        'MAIL_USE_TLS':os.environ['MAIL_USE_TLS'].lower() == 'true',
        'MAIL_USE_SSL':os.environ['MAIL_USE_SSL'].lower() == 'true',
        'MAIL_NOTIFICATION_ON':os.environ['MAIL_NOTIFICATION_ON'].lower() == 'true',
        }
    return config

def set_smtp_settings(envfile=None, **config_dict):
    dotenv_file = dotenv.find_dotenv() or envfile
    dotenv.load_dotenv(dotenv_file,override=True)
    # os.environ.update(config_dict) # current environment altered
    for k,v in config_dict.items():
        # if v.lower() == 'true': v=True
        # if v.lower() == 'false': v=False
        dotenv.set_key(str(dotenv_file), str(k), str(v))

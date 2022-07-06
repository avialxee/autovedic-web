from . import mail
from flask_mail import Message
from flask import current_app

def test_msg(sender_email, to_list_email):
    print(current_app.config['MAIL_SERVER'])
    msg = Message('test mail',
                    sender=sender_email,
                        recipients=to_list_email)
    return mail.send(msg)
from . import mail
from flask_mail import Message

def test_msg(sender_email, to_list_email):
    msg = Message('test mail',
                    sender=sender_email,
                        recipients=to_list_email)
    return mail.send(msg)
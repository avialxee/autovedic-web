from flask import current_app
from . import mail
from flask_mail import Message

def send_mail_newcontact(sender_email, to_list_email, HTML=None):
    msg = Message('Autovedic - Contact Us Form',
                    sender=sender_email,
                        recipients=to_list_email, )
    msg.body= "New Contact Added"
    
    if HTML:
        HTML=HTML.replace('<table', '<table style="font-family: Arial, Helvetica, sans-serif;border-collapse: collapse;width: 100%;"')
        HTML=HTML.replace('<td', '<td style="border: 1px solid #ddd;padding: 8px;"')
        HTML=HTML.replace('<tr', '<tr style="background-color: #f2f2f2;"')
        HTML=HTML.replace('<th', '<th style="padding-top: 12px;padding-bottom: 12px;text-align: left;background-color: #0009;color: white;"')
        
        msg.html=HTML
    return mail.send(msg)
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Email, Content, Mail


def send_mail(from_email, to_email, subject, content):
    sg = SendGridAPIClient()
    content = Content('text/html', content)
    mail = Mail(Email(from_email), subject, Email(to_email), content)
    return sg.client.mail.send.post(request_body=mail.get())
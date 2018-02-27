from django.conf import settings
from django.core.management.base import BaseCommand

from api.models import User

import sendgrid
import os
from sendgrid.helpers.mail import *


class Command(BaseCommand):
    def handle(self, *args, **options):
        sg = sendgrid.SendGridAPIClient(apikey=settings.SENDGRID_API_KEY)

        email = Email("contact@angstromctf.com", "ångstromCTF Team")
        mail = Mail(email, input("Subject: "), None, Content("text/html", input("Content (HTML): ")))

        for user in User.objects.all():
            mail.personalizations[0].add_bcc(Email(user.email))

        response = sg.client.mail.send.post(request_body=mail.get())
        print(response.status_code)


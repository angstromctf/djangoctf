from django import settings
from django.core.management.base import BaseCommand

from api.models import User

import sendgrid
import os
from sendgrid.helpers.mail import *


class Command(BaseCommand):
    def handle(self, *args, **options):
        sg = SendGridAPIClient(apikey=settings.SENDGRID_API_KEY)

        mail = Mail()
        mail.set_from(Email("contact@angstromctf.com", "ångstromCTF Team"))

        mail.set_subject(input("Subject: "))

        personalization = Personalization()
        for user in User.objects.all():
            personalization.add_to(Email(user.email, user.get_full_name()))
        mail.add_personalization(personalization)

        mail.add_content(Content("text/html", input("Content (HTML): ")))

        response = sg.client.mail.send.post(request_body=mail)
        print(response.status_code)
        print(response.headers)
        print(response.body)

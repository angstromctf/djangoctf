from django.conf import settings
from django.core.management.base import BaseCommand

import sendgrid
import os
from sendgrid.helpers.mail import *

from api.models import User

subject = """angstromCTF 2018"""


class Command(BaseCommand):
    def handle(self, *args, **options):
        sg = sendgrid.SendGridAPIClient(apikey=settings.SENDGRID_API_KEY)

        email = Email("team@angstromctf.com", "angstromCTF Team")

        subj = input("Subject: ")
        cont = input("Content (HTML): ")

        for user in User.objects.all():
            try:
                mail = Mail(email, subj, Email(user.email, user.get_full_name()), Content("text/html", cont))
                response = sg.client.mail.send.post(request_body=mail.get())
            except exc:
                print(exc)

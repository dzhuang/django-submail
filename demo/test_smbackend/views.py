# -*- coding: utf-8 -*-

from __future__ import division

__copyright__ = """
Copyright (c) 2015-2016 Dong Zhuang (dzhuang.scut@gmail.com)
"""

__license__ = """
The MIT License (MIT)

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the 
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to permit
persons to whom the Software is furnished to do so, subject to the 
following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF 
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, 
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from django.shortcuts import render
from django.conf import settings
from django import http
from django.core.urlresolvers import reverse

RECIPIENT_LIST = getattr(settings, "RECIPIENT_LIST",
                        ["hello@example.com", "dongzhuang@foo.com"])

REPLY_TO = getattr(settings, "REPLY_TO", "dongzhuang@bar.com")

def analysis_result(result):
    """
    Analysis the result sent back from submail
    """
    success_count = 0
    success_message = []
    error_count = 0
    error_message = []
    for item in result:
        if item["status"] == "success":
            success_count += 1
            success_message.append(item['return'])
        else:
            error_count += 1
            error_message.append(item['msg'])
    return {
        "success_count": success_count,
        "success_message": success_message,
        "error_count": error_count,
        "error_message": error_message
    }


def home(request):  # noqa
    """
    Home page
    """
    html = (
        """
        <html>
        <body>
            <h3>Django Submail backend test</h3>
            <p>Please configure your settings.py and views.py first</p>
            <ul>
                <li>Using send_mail method: <a href="%s">link</a></li>
                <li>Using EmailMessage class: <a href="%s">link</a></li>
                <li>Using EmailMultiAlternatives class:
                    <a href="%s">link</a></li>
                <li>Using non-default APP: <a href="%s">link</a></li>
            </ul>
        </body>
        </html>
        """ % (
            reverse("sendmail"),
            reverse("sendmailmessage"),
            reverse("sendmultialternative"),
            reverse("send_email_non_default_app")
            )
        )
    return http.HttpResponse(html)


def send_email(request):
    """
    using the send_email method
    """
    from django.core.mail import send_mail

    result = send_mail(
        "Your Testing Subject",
        "This is a pure text email body, visit "
        "https://github.com/dzhuang/django-submail for more information.",
        settings.DEFAULT_FROM_EMAIL,
        RECIPIENT_LIST,
    )

    return render(request,
                  "result.html",
                  {"title": "Using the send_email method",
                   "result": analysis_result(result)})


def send_email_message(request):
    """
    using the EmailMessage class
    """
    from django.core.mail import EmailMessage

    mail = EmailMessage(
        subject="Your Testing Subject",
        body="This is a pure text email body, visit "
        "https://github.com/dzhuang/django-submail for more information.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=RECIPIENT_LIST,
        headers={"Reply-To": REPLY_TO},
    )

    result = mail.send()
    return render(request, "result.html",
                  {"title": "Using the EmailMessage class",
                   "result": analysis_result(result)})


def send_multialternative(request):
    """
    using the EmailMultiAlternatives class
    """
    from django.core.mail import EmailMultiAlternatives

    mail = EmailMultiAlternatives(
        subject="Your Testing Subject",
        body="This is a pure text email body.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=RECIPIENT_LIST,
        headers={"Reply-To": REPLY_TO},
    )
    mail.attach_alternative(
        "<p>This is an HTML email body, visit "
        "<a href='https://github.com/dzhuang/django-submail'>"
        "Github repository </a> for more information.</p>",
        "text/html")

    result = mail.send()

    return render(request, "result.html",
                  {"title": "Using the EmailMultiAlternatives class",
                   "result": analysis_result(result)})


def send_email_non_default_app(request):
    """
    using non default_app:
    You should specify the appid (using SUBMAIL_APP_ID key) and
    appkey (using SUBMAIL_APP_KEY) in headers.
    """
    from django.core.mail import EmailMessage

    mail = EmailMessage(
        subject="Your Testing Subject",
        body="This is a pure text email body, visit "
        "https://github.com/dzhuang/django-submail for more information.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=RECIPIENT_LIST,
        headers={
            "Reply-To": REPLY_TO,
            "SUBMAIL_APP_ID": settings.ANOTHER_SUBMAIL_APP_ID,
            "SUBMAIL_APP_KEY": settings.ANOTHER_SUBMAIL_APP_KEY},
    )

    result = mail.send()
    return render(request, "result.html",
                  {"title": "Using non-default APP",
                   "result": analysis_result(result)})

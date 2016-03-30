from django.conf.urls import url
from django.contrib import admin
from test_smbackend import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home),
    url(r'^send_mail/$', views.send_email, name="sendmail"),
    url(r'^send_email_message/$', views.send_email_message, name="sendmailmessage"),
    url(r'^send_multialternative/$', views.send_multialternative, name="sendmultialternative"),
    url(r'^send_email_non_default_app/$', views.send_email_non_default_app, name="send_email_non_default_app"),
    
]

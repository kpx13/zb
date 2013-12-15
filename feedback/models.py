# -*- coding: utf-8 -*-
from django.db import models
from pytils import dt
from django import forms
from django.template import Context, Template
from django.conf import settings
from django.core.mail import send_mail
from livesettings import config_value

def sendmail(subject, body):
    mail_subject = ''.join(subject)
    send_mail(mail_subject, body, settings.DEFAULT_FROM_EMAIL,
        [config_value('MyApp', 'EMAIL')])

class Feedback(models.Model):
    name  = models.CharField(u'Ваше имя',     max_length=255)
    email = models.EmailField(u'Ваш email', max_length=255)
    type  = models.CharField(u'Откуда',  max_length=255, blank=True)
    request_date = models.DateTimeField(u'дата заявки', auto_now_add=True)
                    
    class Meta:
        verbose_name = u'подписчик'
        verbose_name_plural = u'подписчики'
        ordering = ['-request_date']

    def __unicode__(self):
        return u'№ %s от %s' % (self.id, dt.ru_strftime(u"%d %B %Y", self.request_date))
    
    def send(self):
        subject=u'Новая подписка с сайта',
        body_templ="""
    {{ f.type }}
    
    Имя: {{ f.name }}
    Email: {{ f.email }}
    Дата: {{ f.request_date }}
"""
        ctx = Context({
            'f': self
        })
        body = Template(body_templ).render(ctx)
        sendmail(subject, body)
# -*- coding: utf-8 -*-

from django.core.context_processors import csrf
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages
 
from pages.models import Page
from textblock.models import TextBlock

import config
from livesettings import config_value
from django.conf import settings
from feedback.forms import FeedbackForm

import requests
import json
import urllib
import hashlib


def jc_send(name, email, group='clients_e-training'):
    m = hashlib.md5()
    user_id = 'fschool'
    user_rps_key = 'JV7Sgl#lv=d#kuQc5?[s=B}|2;v5)|L%4+tV6ZwJ'
    data = {'rid[0]': group, 'lead_name': name, 'lead_email': email}
    par = '::'.join([urllib.urlencode(data), user_id, user_rps_key])
    m.update(par)
    data['hash'] = m.hexdigest()
    r = requests.post("http://fschool.justclick.ru/api/AddLeadToGroup", data=data)
    

def get_common_context(request):
    c = {}
    c['request_url'] = request.path
    c['is_debug'] = settings.DEBUG
    c['menu'] = Page.get_menu()
    c.update(csrf(request))
    return c

def page(request, page_name):
    c = get_common_context(request)
    p = Page.get_by_slug(page_name)
    if p:
        c.update({'p': p})
        return render_to_response('page.html', c, context_instance=RequestContext(request))
    else:
        raise Http404()

def home(request):
    c = get_common_context(request)
    c['request_url'] = 'home'
    c['text_1'] = TextBlock.get_by_id(1)
    c['text_2'] = TextBlock.get_by_id(2)
    c['text_3'] = TextBlock.get_by_id(3)
    c['text_4'] = TextBlock.get_by_id(4)
    c['text_5'] = TextBlock.get_by_id(5)
    
    form = FeedbackForm()
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.type = u'Заявка на обучение'
            f.save()
            c['form_send'] = True
            jc_send(f.name.encode('utf-8'), f.email.encode('utf-8'))
            f.send()
    c['form'] = form
    return render_to_response('home.html', c, context_instance=RequestContext(request))

def audiobook(request):
    c = get_common_context(request)
    c['text_6'] = TextBlock.get_by_id(6)
    
    form = FeedbackForm()
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.type = u'Получение аудиокниги'
            f.save()
            c['form_send'] = True
            jc_send(f.name.encode('utf-8'), f.email.encode('utf-8'))
            f.send()
    c['form'] = form
    return render_to_response('audiobook.html', c, context_instance=RequestContext(request))

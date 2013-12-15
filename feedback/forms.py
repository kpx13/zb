# encoding: utf-8

from django.forms import ModelForm
from models import Feedback



class FeedbackForm(ModelForm):
    
    class Meta:
        model = Feedback
        exclude = ('request_date', 'type')
    

    

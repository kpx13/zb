# -*- coding: utf-8 -*-
from django.db import models
from ckeditor.fields import RichTextField
import pytils

class Page(models.Model):
    title = models.CharField(max_length=256, verbose_name=u'заголовок')
    content = RichTextField(blank=True, verbose_name=u'контент')
    order = models.IntegerField(blank=True, null=True, verbose_name = u'порядковый номер в меню')
    slug = models.SlugField(max_length=256, verbose_name=u'url страницы', unique=True, blank=True, help_text=u'Заполнять не нужно')
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug=pytils.translit.slugify(self.title)
        super(Page, self).save(*args, **kwargs)
        if not self.order:
            self.order = self.id
            self.save()
    
    @staticmethod
    def get_by_slug(page_name):
        try:
            return Page.objects.get(slug=page_name)
        except:
            return None
        
    @staticmethod
    def get_menu():
        try:
            return [{'slug': p.slug, 'title': p.title}  for p in Page.objects.filter(order__gte=1)]
        except:
            return None
        
    class Meta:
        verbose_name = u'статическая страница'
        verbose_name_plural = u'статические страницы'
        ordering=['order']
        
    def __unicode__(self):
        return self.slug

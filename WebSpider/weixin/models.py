# -*- coding: utf-8 -*-
__author__ = 'Administrator'


from django import forms
from django.db import models
import datetime
from django.contrib import admin
from django.forms.widgets import Widget



class DownloadUrlWidget(Widget):

    def render(self, name, value, attrs=None):
        output='<a href="/%s">%s</a>' % (value, value)
        return output

class WeiXinForm(forms.Form):
    Htmlurl=forms.CharField(max_length=2048,label='文章地址')
    UserId=forms.CharField(max_length=100,label='UserId')
    LabelId=forms.CharField(max_length=100,label='LabelId')

class WeiXin(models.Model):
    Htmlurl=models.CharField(max_length=2048,null=False,verbose_name='地址')
    UserId=models.CharField(max_length=100,null=False,verbose_name='UserId')
    LabelId=models.CharField(max_length=100,null=False,verbose_name='LabelId')
    created=models.DateTimeField(default=datetime.datetime.now,verbose_name='创建时间')

    class Meta:
        ordering=['created']
        verbose_name='微信'
    def __unicode__(self):
        return self.Title


class WeiXinAdmin(admin.ModelAdmin):
    # fields = ['Title','Htmlurl','created']
    list_display=('UserId','created','Htmlurl')
    # def Downloadurl_url(self,obj):
    #     return u'<a href="../../../%s">%s</a>' %(obj.Downloadurl,u'下载')
    # Downloadurl_url.allow_tags = True
    # Downloadurl_url.short_description = u"下载"

    def formfield_for_dbfield(self, db_field, **kwargs):
        # if db_field.name=='Downloadurl':
        #     kwargs['widget']=DownloadUrlWidget
        #     try:
        #         del kwargs['request']
        #     except KeyError:
        #         pass
        #     return  db_field.formfield(**kwargs)
        return super(WeiXinAdmin,self).formfield_for_dbfield(db_field,**kwargs)


admin.site.register(WeiXin,WeiXinAdmin)


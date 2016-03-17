# -*- coding: utf-8 -*-
__author__ = 'Administrator'


from django.http import HttpResponse
from models import WeiXin,WeiXinForm
from django.shortcuts import render_to_response,RequestContext,HttpResponseRedirect
from spider import spider


def home(request):
    if request.method=='POST':
        form=WeiXinForm(request.POST)
        if form.is_valid():
            weixin=WeiXin()
            weixin.Htmlurl=form.cleaned_data['Htmlurl']
            spider(weixin)
            # weixin.save()
            return HttpResponse(u'爬取成功！')
        else:
            return HttpResponse(u'爬取失败请联系管理员！')
    else:
        form=WeiXinForm(request.GET)
        # return render_to_response('weixin.html',{'form':form},context_instance=RequestContext(request))
        if form.is_valid():
            weixin=WeiXin()
            weixin.Htmlurl=form.cleaned_data['Htmlurl']
            weixin.UserId=form.cleaned_data['UserId']
            weixin.LabelId=form.cleaned_data['LabelId']
            spider(weixin)
            weixin.save()
            return HttpResponse(u'爬取成功！')
        else:
            return HttpResponse(u'爬取失败请联系管理员！')


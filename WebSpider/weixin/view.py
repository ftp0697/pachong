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
            weixin.save()
            return HttpResponseRedirect(weixin.Downloadurl)
        else:
            return HttpResponse(u'爬取失败请联系管理员！')
    else:
        form=WeiXinForm()
        return render_to_response('weixin.html',{'form':form},context_instance=RequestContext(request))

# -*- coding:utf-8 -*-
import urllib
import urllib2
import re
import os
import Zfile
import shutil

# 创建新目录
def mkdir(path):
    path = path.strip()
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        print u"偷偷新建了名字叫做", path, u'的文件夹'
        # 创建目录操作函数
        os.makedirs(path)
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print u"名为", path, '的文件夹已经创建成功'
        return False


# 保存HTML页面
def saveHtml(content, name):
    fileName = name + "/" + name + ".txt"
    f = open(fileName, "w+")
    print u"正在偷偷保存她的个人信息为", fileName
    f.write(content.encode('utf-8'))


# 保存多张图片
def saveImgs(images, name):
    number = 1
    print u"发现", name, u"共有", len(images), u"张照片"
    for imageURL in images:
        splitPath = imageURL.split('.')
        fTail = splitPath.pop()
        if len(fTail) > 3:
            fTail = "jpg"
        fileName = name + "/" + str(number) + "." + fTail
        saveImg(str(imageURL), fileName)
        number += 1

# 传入图片地址，文件名，保存单张图片
def saveImg(imageURL, fileName):
    u = urllib.urlopen(imageURL)
    data = u.read()
    f = open(fileName, 'wb')
    f.write(data)
    print u"正在悄悄保存她的一张图片为", fileName
    f.close()

def spider(weixin):
    url=weixin.Htmlurl
    # url = '''http://mp.weixin.qq.com/s?__biz=MzA4MzUwNzExMg==&mid=204458088&idx=1&sn=3e72b6b064232240aab4bc9ef445906d&scene=1&srcid=09113ERW3oEqdtsufsLYReMn&key=dffc561732c22651bd637924993cc98b75333cf022692f52bdf57d84d329163241da8609c9f08bf7c88ff0cf6f5a055e&ascene=1&uin=MTc1Njg2MDIyMQ%3D%3D&devicetype=webwx&version=70000001&pass_ticket=r5bIjsrbkVWvxNarrNxcFDsUgl%2BzdL0uD0KUEm8IxzYjFtsctIn%2Bnr5RMc14mXWc'''
    try:
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; rv:37.0) Gecko/20100101 Firefox/37.0'
        headers = {'User-Agent': user_agent}
        request = urllib2.Request(url, headers=headers)
        response = urllib2.urlopen(request)
        # print response.read()
        html = response.read().decode("utf-8")
        # print html
        myItems = re.findall('<h2 class="rich_media_title" id="activity-name">(.*?)</h2>', html, re.S)
        title = myItems[0].replace("\r\n", " ").strip()
        path=title
        mkdir(path)
        content=re.findall('<div class="rich_media_content " id="js_content">(.*?)</div>', html, re.S)
        saveHtml(content[0].strip(),title)
        myItems = re.findall('<img.*?data-src="(.*?)".*?/>', content[0], re.S)
        saveImgs(myItems,path)
        download=u'static/' + path + u'.zip'
        Zfile.careate(download,path)#生成压缩包
        shutil.rmtree(path)#删除目录
        weixin.Title=title
        weixin.Downloadurl=download

    except urllib2.URLError, e:
        if hasattr(e, "code"):
            print e.code
        if hasattr(e, "reason"):
            print e.reason
    return weixin
# -*- coding:utf-8 -*-
import urllib
import urllib2
import re
import os
import logging
from urllib import urlencode
import Zfile
import shutil
import bos_conf
import uuid
import json
import base64
from baidubce.services.bos.bos_client import BosClient

bucket_name = 'didiweixuetestpublic'
logging.basicConfig(level=logging.DEBUG)
__logger = logging.getLogger(__name__)

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
    imgUrl = {}
    bos_client = BosClient(bos_conf.config)
    if not bos_client.does_bucket_exist(bucket_name):
        __logger.debug("未查询到bucket：%s ", bucket_name)
        exit()
    # print u"发现", name, u"共有", len(images), u"张照片"
    for imageURL in images:
        splitPath = imageURL.split('.')
        fTail = splitPath.pop()
        if len(fTail) > 3:
            fTail = "jpg"
        fileName = name+"/" + str(number) + "." + fTail
        saveImg(str(imageURL), fileName, bos_client)
        imgUrl[imageURL] = bucket_name+".bj.bcebos.com/"+fileName
        number += 1
    return imgUrl

# 传入图片地址，文件名，保存单张图片
def saveImg(imageURL, fileName,bos_client):

    u = urllib.urlopen(imageURL)
    data = u.read()
    bos_client.put_object_from_string(bucket_name, fileName, data)

    # f = open(fileName, 'wb')
    # f.write(data)
    # print u"正在悄悄保存她的一张图片为", fileName
    # f.close()

def spider(weixin):
    url=base64.b64decode(weixin.Htmlurl)
    UserId=weixin.UserId
    LabelId=weixin.LabelId
    # url = '''http://mp.weixin.qq.com/s?__biz=MzA4ODUzNjAxOA==&mid=420208152&idx=5&sn=5fc225209d3dbd5d8f74b405510d7b9a&scene=2&srcid=0314ZkCVNaMETykzam3Mi2Ys&from=timeline&isappinstalled=0#wechat_redirect'''
    try:
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; rv:37.0) Gecko/20100101 Firefox/37.0'
        headers = {'User-Agent': user_agent}
        request = urllib2.Request(url, headers=headers)
        response = urllib2.urlopen(request)
        # print response.read()
        html = response.read().decode("utf-8")
        # print html
        title = re.findall('var msg_title = "(.*?)";', html, re.S)
        # title = myItems[0].replace("\r\n", " ").strip()
        AuthorName = re.findall('var nickname = "(.*?)";', html, re.S)
        # if len(myItems1)!=0:
        #    AuthorName=myItems1[0].replace("\r\n", " ").strip()
        Thumb = re.findall('var msg_cdn_url = "(.*?)";', html, re.S)
        # path=title
        # mkdir(path)
        content=re.findall('<div class="rich_media_content " id="js_content">(.*?)</div>', html, re.S)
        htmlcontent=content[0].strip()
        myItems2 = re.findall('<img.*?src="(.*?)".*?/>', content[0], re.S)
        imgUrl=saveImgs(myItems2,str(uuid.uuid1()))
        for imageURL in myItems2:
            htmlcontent=htmlcontent.replace(imageURL,"http://"+imgUrl[imageURL])
        # saveHtml(htmlcontent,title)
        htmlcontent=htmlcontent.replace("data-src","src")
        if len(Thumb)!=0:
            imgUrl=saveImgs(Thumb,str(uuid.uuid1()))
            Thumb=imgUrl[Thumb[0]]
        postDict={
            'uploaderId':UserId,
            "Thumb":Thumb,
            "AuthorName":AuthorName.encode('utf-8'),
            "AuthorId":title.encode('utf-8'),
            "HtmlBody":htmlcontent,
            "LabelId":LabelId
        }
        encodedjson = json.dumps(postDict)
        # postData = urllib.urlencode(postDict)
        request = urllib2.Request("http://localhost:10451/api/UGCNewsLinkApi/ReceiveNewsBody", encodedjson)
        request.add_header('Content-Type', "application/json")
        response = urllib2.urlopen(request)
        html = response.read().decode("utf-8")
        print html
        # download=u'static/' + path + u'.zip'
        # Zfile.careate(download,path)#生成压缩包
        # shutil.rmtree(path)#删除目录
        # weixin.Title=title
        # weixin.Downloadurl=download

    except urllib2.URLError, e:
        if hasattr(e, "code"):
            print e.code
        if hasattr(e, "reason"):
            print e.reason
    return weixin
# -*- coding: utf-8 -*-

#导入接口文件包，给接口负值
import urllib
import urllib2

#get接口
url = 'https://tron.network/api/v2/node/nodemap'

def get_str():#（定义函数）

    #d定义请求数据，且对数据进行复制
    data = {}
    #data['address'] = 'TS8fyGssAxgBttmezCis9o3zz3jir5ysp9'
    #data['name'] = 'bochang123'

    #对数据进行编码
    data = urllib.urlencode(data)

    #将数据与URL进行链接
    request = url+'?'+data

    requestResponse = urllib2.urlopen(request)


    #打开请求，获取对象
    ResponseStr =  requestResponse.read()


    #打印数据
    ResponseStr = ResponseStr.decode("unicode_escape")

    return ResponseStr

if __name__ == "__main__":
   # i=0#(循环)
    #while i<5:
        a = get_str()
       # i += 1
        #print a
        print a





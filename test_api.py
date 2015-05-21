# -*- encoding:utf-8 -*-
import requests
import sys,os
import json

if __name__ == "__main__":
    data = {"feedback":"这应用太他妈好用了","email":"dasdf@fds.com","phone":"12345"}
    url = "http://shuailong.me:5000/api/feedback"
    #print requests.post(url, data=json.dumps(data)).text

    data1 = {"feedback":"这应用太他妈好用了","email":"dasdf@fds.com","phone":"12345"}
    data1 = {"name":"吴朝晖","email":"fads","phone":"123445","title":"教授","location":"曹东105","research":"纳米材料的应用"}
    url1 = "http://shuailong.me:5000/api/correct_teacher"
    print requests.post(url1, data=json.dumps(data1)).text



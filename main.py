import datetime
import json
import requests

from WeChatPush import WechatMessagePush

def get_info():
    url = "http://hslhapp.hhws168.com/common/v1/jsonDownload/"
    headers = {
        "Host": "hslhapp.hhws168.com",
        "Token":"3a90beddb879790a606bcb1141e325d9",
        "Content-Encoding": "gzip",
        "Versioncode":"1.2.8",
        "Channel":"alphago",
        "Content-Type":"application/json;charset=utf-8",
        "Content-Length":"166",
        "Connection": "Keep-Alive",
        "Accept-Encoding":"gzip",
        "User-Agent":"okhttp/3.8.0"
    }

    date = "2022-11-04"
    # date = str(datetime.date.today())

    body = {"option0": "alphaGo",
            "option1": "server",
            "option2": "minuteLargeDdePulseQulet",
            "option3": "stockData",
            "option4": str(date),
            "option5": "9999",
            "truncation": "cut20191111"
    }
    responses = requests.post(url = url,data = json.dumps(body),headers = headers)
    return responses

def get_info1():
    url = "http://hslhapp.hhws168.com/common/v1/jsonDownload/"
    headers = {
        "Host": "hslhapp.hhws168.com",
        "Token":"3a90beddb879790a606bcb1141e325d9",
        "Content-Encoding": "gzip",
        "Versioncode":"1.2.8",
        "Channel":"alphago",
        "Content-Type":"application/json;charset=utf-8",
        "Content-Length":"156",
        "Connection": "Keep-Alive",
        "Accept-Encoding":"gzip",
        "User-Agent":"okhttp/3.8.0"
    }
    date = "2022-11-04"
   #date = str(datetime.date.today())
    body = {"option0": "alphaGo",
        "option1": "server",
        "option2": "timeDivingGold",
        "option3": "stockData",
        "option4": str(date),
        "option5": "9999",
        "truncation": "cut20191111"
    }
    responses = requests.post(url = url,data = json.dumps(body),headers = headers)
    return responses

def get_info2():
    url = "http://hslhapp.hhws168.com/common/v1/jsonDownload/"
    headers = {
        "Host": "hslhapp.hhws168.com",
        "Token":"3a90beddb879790a606bcb1141e325d9",
        "Content-Encoding": "gzip",
        "Versioncode":"1.2.8",
        "Channel":"alphago",
        "Content-Type":"application/json;charset=utf-8",
        "Content-Length":"156",
        "Connection": "Keep-Alive",
        "Accept-Encoding":"gzip",
        "User-Agent":"okhttp/3.8.0"
    }
    date = "2022-11-04"
   # date = str(datetime.date.today())
    body = {"option0": "alphaGo",
        "option1": "server",
        "option2": "minuteUpShadow",
        "option3": "stockData",
        "option4": str(date),
        "option5": "9999",
        "truncation": "cut20191111"
    }
    responses = requests.post(url = url,data = json.dumps(body),headers = headers)
    return responses

def get_info3():
    url = "http://hslhapp.hhws168.com/common/v1/jsonDownload/"
    headers = {
        "Host": "hslhapp.hhws168.com",
        "Token":"3a90beddb879790a606bcb1141e325d9",
        "Content-Encoding": "gzip",
        "Versioncode":"1.2.8",
        "Channel":"alphago",
        "Content-Type":"application/json;charset=utf-8",
        "Content-Length":"158",
        "Connection": "Keep-Alive",
        "Accept-Encoding":"gzip",
        "User-Agent":"okhttp/3.8.0"
    }
    date = "2022-11-04"
 # date = str(datetime.date.today())
    body = {"option0": "alphaGo",
        "option1": "server",
        "option2": "minutePulseQulet",
        "option3": "stockData",
        "option4": str(date),
        "option5": "9999",
        "truncation": "cut20191111"
    }
    responses = requests.post(url = url,data = json.dumps(body),headers = headers)
    return responses


def parse_info(res):
    json1 = json.loads(res.text)
    dict1 = dict(json1)
    list1 = dict1.get("data")
    str1 = ''.join(list1)
    list2 = json.loads(str1)
    # for i in range(len(list2)):
    #     print(list2[i])
    dict_result = {}
    list3 = list()
    for _ in list2:
        for k, v in _.items():
            if k == 'code' or k == 'name' or k == 'getTime' or k == 'firstGetTime':
                dict_result[k] = v
        # print(dict_result)
        if dict_result['getTime'] != dict_result['firstGetTime']:
            list3.append(dict_result.copy())

    return list3

    # for i in range(len(list3)):
    #     print(list3[i])

def save_list(filepath,c_list):

    c_list = json.dumps(c_list)
    '''将c_list存入文件
    '''
    a = open(filepath, "w", encoding='UTF-8')
    a.write(c_list)
    a.close()

def read_list(filepath):
    '''读取data_source_list文件
    '''
    b = open(filepath, "r", encoding='UTF-8')
    out = b.read()
    out = json.loads(out)
    b.close()
    return out

def push_info(filepath,list_result,template_id):
    appid = "wx112f057de987d19e"
    screct = "0c9af8144a9f98b2ece14e8a0918778d"
    #template_id = "Vos7ef7UiEXRXL6AfLsA83zbOD9Ehkd9nQ79OMLKuYg"

    last_list = read_list(filepath)
    push_list = list()

    print("list_result")
    for i in range(len(list_result)):
       print(list_result[i])

    print("last_list")
    for i in range(len(last_list)):
        print(last_list[i])

    if len(list_result) != len(last_list):
        # 数据数量不一致，直接推送
        for i in range(len(list_result)):
            WechatMessagePush(appid, screct, template_id).send_wechat_temple_msg(list_result[i])
        print("数据数量不一致，直接推送")

        for i in range(len(list_result)):
           print(list_result[i])
    else:
        # 数据数量一致，判断更新推送
        for i in range(len(list_result)):
            if list_result[i] != last_list[i]:
                push_list.append(list_result[i].copy())

        print("数据数量一致，判断更新推送")

        print("push_list")
        for i in range(len(push_list)):
           print(push_list[i])

        if len(push_list):
            for i in range(len(push_list)):
                WechatMessagePush(appid, screct, template_id).send_wechat_temple_msg(push_list[i])
        else:
            print("没有数据更新,不推送")

    save_list(filepath,list_result)

if __name__ == '__main__':
    filepath = "./data_source_list.txt"
    filepath1 = "./data_source_list_1.txt"
    filepath2 = "./data_source_list_2.txt"
    filepath3 = "./data_source_list_3.txt"
    res = get_info()
    res1 = get_info1()
    res2 = get_info2()
    res3 = get_info3()
    list_result = parse_info(res)
    list_result1 = parse_info(res1)
    list_result2 = parse_info(res2)
    list_result3 = parse_info(res3)
    template_id="LwjaQf2BqPDKtoatVisuxQLKcorVC3zeLYcwQespDsY"
    #template_id1="6EMjOCJZKHTF7fZA6QylsNcIlDiObfKw67Ddvj2Zm7Q"
    #template_id2="Vos7ef7UiEXRXL6AfLsA83zbOD9Ehkd9nQ79OMLKuYg"
    #template_id3="ikOqvUyQjFbDD7kqW1as22YScnOAvm8aRirGl-GW2wc"
    push_info(filepath,list_result,template_id)
    #push_info(filepath1,list_result1,template_id1)
    #push_info(filepath2,list_result2,template_id2)
    #push_info(filepath3,list_result3,template_id3)

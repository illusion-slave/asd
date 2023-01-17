import datetime
import json
import requests

def get_info(ContentLength,option2):
    url = "http://hslhapp.hhws168.com/common/v1/jsonDownload/"
    headers = {
        "Host": "hslhapp.hhws168.com",
        "Token":"3a90beddb879790a606bcb1141e325d9",
        "Content-Encoding": "gzip",
        "Versioncode":"1.2.8",
        "Channel":"alphago",
        "Content-Type":"application/json;charset=utf-8",
        "Content-Length":ContentLength,
        "Connection": "Keep-Alive",
        "Accept-Encoding":"gzip",
        "User-Agent":"okhttp/3.8.0"
    }
 
    # date = "2022-11-01"
    date = str(datetime.date.today())
 
    body = {"option0": "alphaGo",
            "option1": "server",
            "option2": option2,
            "option3": "stockData",
            "option4": str(date),
            "option5": "9999",
            "truncation": "cut20191111"
    }
    responses = requests.post(url = url,data = json.dumps(body),headers = headers)
    return responses
 
def parse_info(res):
    # 请求数据成功
    list_judge = list()
    list_result = list()
    if res.status_code == 200:
        json1 = json.loads(res.text)
        dict1 = dict(json1)
        list1 = dict1.get("data")
        if len(list1):
            str1 = ''.join(list1)
            list2 = json.loads(str1)
            # for i in range(len(list2)):
            #     print(list2[i])
            dict_result = {}

            for _ in list2:
                for k, v in _.items():
                    if k == 'name' or k == 'date':
                        dict_result[k] = v
                list_judge.append(dict_result.copy())

                for k, v in _.items():
                    if k == 'code' or k == 'name' or k == 'date' or k == 'firstGetTime':
                        dict_result[k] = v
                list_result.append(dict_result.copy())
        else:
            print("data is null")
    else:
        print("requset failed!")

    return list_judge,list_result

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
 
def push_info(filepath, list_judege, list_result, web_hook):
    last_list = read_list(filepath)
    push_list = list()

    if len(list_judege):
        print("上次数据：")
        for i in range(len(last_list)):
            print(last_list[i])

        print("本次数据：")
        for i in range(len(list_result)):
            print(list_result[i])

        for i in range(len(list_result)):
            if list_judege[i] not in last_list:
                push_list.append(list_result[i].copy())

        print("需推送数据：")
        if len(push_list):
            for i in range(len(push_list)):
                print(push_list[i])
                push_report(push_list[i], web_hook)
        else:
            print("push_list empty!!!没有数据更新")

        save_list(filepath, list_result)

    else:
        print("list_result empty!!!")

    print("\n")


 
 
def push_report(push_dict, web_hook):
    header = {
        "Content-Type": "application/json;charset=UTF-8"
    }

    message_body = {
        "msgtype": "text",
        "text": {
            "content":
                " •  code：" + push_dict['code'] +
                "                      "
                " •  name：" + push_dict['name'] +
                "                      "
                "https://m.10jqka.com.cn/stockpage/hs_" + push_dict['code'] +
                "                      "
                " •  firstGetTime：" + push_dict['firstGetTime']
        },
        "at": {
            "atMobiles": [],
            "isAtAll": False
        }
    }

    send_data = json.dumps(message_body)  # 将字典类型数据转化为json格式
    ChatBot = requests.post(url=web_hook, data=send_data, headers=header)
    opener = ChatBot.json()
    if opener["errmsg"] == "ok":
        print(u"%s 通知消息发送成功！" % opener)
    else:
        print(u"通知消息发送失败，原因：{}".format(opener))
 
if __name__ == '__main__':
    filepath = "./data_source_list.txt"
    filepath1 = "./data_source_list_1.txt"
    filepath2 = "./data_source_list_2.txt"
    filepath3 = "./data_source_list_3.txt"
    webhook = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=f38433df-3a2a-46d3-bd45-8d31bf8adc94"
    webhook1 = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=8eed9b02-38de-4d20-939c-278214128005"
    webhook2 = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=9b6a9289-c683-4f42-9a77-04c4384cf19e"
    webhook3 = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=0810ff88-06be-46dc-9d67-07e1d894ad95"

    print("大单回调")
    res = get_info("166","minuteLargeDdePulseQulet")
    list_judge,list_result = parse_info(res)
    push_info(filepath, list_judge, list_result, webhook)

    print("潜水捞金")
    res1 = get_info("156","timeDivingGold")
    list_judge1,list_result1 = parse_info(res1)
    push_info(filepath1, list_judge1,list_result1, webhook1)

    print("尾盘上引")
    res2 = get_info("156","minuteUpShadow")
    list_judge2,list_result2 = parse_info(res2)
    push_info(filepath2, list_judge2, list_result2, webhook2)

    print("强势回调")
    res3 = get_info("158","minutePulseQulet")
    list_judge3,list_result3 = parse_info(res3)
    push_info(filepath3, list_judge3, list_result3, webhook3)

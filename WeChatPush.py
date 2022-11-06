import json
import requests

class WechatMessagePush:
    def __init__(self, appid, appsecret, temple_id):
        self.appid = appid
        self.appsecret = appsecret
        self.temple_id = temple_id
        self.token = self.get_Wechat_access_token()

    def get_Wechat_access_token(self):
        '''
        获取微信的access_token： 获取调用接口凭证
        :return:
        '''
        url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={self.appid}&secret={self.appsecret}"
        response = requests.get(url)
        res = response.json()
        if "access_token" in res:
            token = res["access_token"]
            return token
    def send_wechat_temple_msg(self, push_dict):
        '''
        发送微信公众号的模板消息'''
        url = f"https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={self.token}"
        touser_list=['o0gfI6HUFSZjpwYC9ZjbSS8Z43Jw','o0gfI6JKkTYAi6GUl7MJpPnL-QfY']
        for open_id in touser_list:
            body = {
                "touser": open_id,
                "template_id": self.temple_id,
                "url": "http://www.baidu.com",
                "data": {
                    "code": {"value": push_dict['code']},
                    "name": {"value": push_dict['name']},
                    "getTime": {"value": push_dict['getTime']},
                    "firstGetTime": {"value": push_dict['firstGetTime']}
                }

            }
            headers = {"Content-type": "application/json"}
            data = json.JSONEncoder().encode(body)
            res = requests.post(url=url, data=data, headers=headers)
        # print(res)

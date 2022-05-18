#低保版,魔改各路大佬的,已完成每日签到,开宝箱和分享3000币,每日3000币起,测试约为3000-8000币
# 变量名ksjsbCookie 多个用&分割，需要完整cookies，青龙单容器快手完整cookies只能放63个。建议启用60个,否则会报错

import json
import os
import time
import urllib.parse
import urllib.request

env_dist = os.environ
# 获取环境变量
_Cookie = env_dist.get("ksjsbCookie")
# 分割环境变量
Cookies = _Cookie.split("&")
# 协议头


Agent = "Mozilla/5.0 (Linux; Android 11; Redmi K20 Pro Premium Edition Build/RKQ1.200826.002; wv) AppleWebKit/537.36 " \
        "(KHTML, like Gecko) Version/4.0 Chrome/90.0.4430.226 KsWebView/1.8.90.488 (rel;r) Mobile Safari/537.36 " \
        "Yoda/2.8.3-rc1 ksNebula/10.3.41.3359 OS_PRO_BIT/64 MAX_PHY_MEM/7500 AZPREFIX/yz ICFO/0 StatusHT/34 " \
        "TitleHT/44 NetType/WIFI ISLP/0 ISDM/0 ISLB/0 locale/zh-cn evaSupported/false CT/0 "


# 获取账号信息


def getInformation(can_cookie):
    url = "https://nebula.kuaishou.com/rest/n/nebula/activity/earn/overview/basicInfo"
    headers = {'User-Agent': Agent, 'Accept': '*/*', 'Accept-Language': ' zh-CN,zh;q=0.9', 'Cookie': can_cookie}
    request = urllib.request.Request(url=url, headers=headers)
    response = urllib.request.urlopen(request)
    str_result = response.read().decode('UTF-8')
    arr_json = json.loads(str_result)
    arr_result = {
        'code': -1
    }
    try:
        arr_result = {
            'code': arr_json['result'],
            'data': {
                'nickname': str(arr_json['data']['userData']['nickname']),
                'cah': str(arr_json['data']['totalCash']),
                'coin': str(arr_json['data']['totalCoin'])
            }
        }
    except TypeError as reason:
        print("获取信息出错啦" + str(reason) + str_result)

    return arr_result


# 开宝箱
def openBox(can_cookie, name):
    url = "https://nebula.kuaishou.com/rest/n/nebula/box/explore?isOpen=true&isReadyOfAdPlay=true"
    headers = {'User-Agent': Agent, 'Accept': '*/*', 'Accept-Language': ' zh-CN,zh;q=0.9', 'Cookie': can_cookie}
    request = urllib.request.Request(url=url, headers=headers)
    response = urllib.request.urlopen(request)
    str_result = response.read().decode('UTF-8')
    arr_json01 = json.loads(str_result, strict=False)
    show = arr_json01['data']['show']
    try:
        if show:
            if arr_json01['data']['commonAwardPopup'] is not None:
                print("账号[" + name + "]开宝箱获得" + str(arr_json01['data']['commonAwardPopup']['awardAmount']) + "金币")
            else:
                if arr_json01['data']['openTime'] == -1:
                    print("账号[" + name + "]今日开宝箱次数已用完")
                else:
                    print("账号[" + name + "]开宝箱冷却时间还有" + str(int(arr_json01['data']['openTime'] / 1000)) + "秒")
        else:
            print("账号[" + name + "]账号获取开宝箱失败:疑似cookies格式不完整")
    except TypeError as reason:
        print("开宝箱出错啦" + str(reason) + str_result)


# 查询签到
def querySign(can_cookie,name):
    url = "https://nebula.kuaishou.com/rest/n/nebula/sign/queryPopup"
    headers = {'User-Agent': Agent, 'Accept': '*/*', 'Accept-Language': ' zh-CN,zh;q=0.9', 'Cookie': can_cookie}
    request = urllib.request.Request(url=url, headers=headers)
    response = urllib.request.urlopen(request)
    str_result = response.read().decode('UTF-8')
    json_arr = json.loads(str_result)
    result_code = json_arr['data']['nebulaSignInPopup']['todaySigned']
    try:
        if result_code:
            print("账号[" + name + "]今日已签到" + json_arr['data']['nebulaSignInPopup']['subTitle'] + "," + json_arr['data']['nebulaSignInPopup']['title'])
        else:
            sign(can_cookie,name)
    except TypeError as reason:
        print("查询签到出错啦" + str(reason) + str_result)


# 签到
def sign(can_cookie,name):
    url = "https://nebula.kuaishou.com/rest/n/nebula/sign/sign?source=activity"
    headers = {'User-Agent': Agent, 'Accept': '*/*', 'Accept-Language': ' zh-CN,zh;q=0.9', 'Cookie': can_cookie}
    request = urllib.request.Request(url=url, headers=headers)
    response = urllib.request.urlopen(request)
    str_result = response.read().decode('UTF-8')
    json_arr = json.loads(str_result)
    result_code = json_arr['result']
    try:
        if result_code==1:
            print("账号[" + name + "]签到成功:" + str(json_arr['data']['toast']))
        else:
            print("账号[" + name + "]签到成功:" + json_arr['error_msg'])
    except TypeError as reason:
        print("查询签到出错啦" + str(reason) + str_result)


# 准备分享得金币任务
def setShare(can_cookie, name):
    url = "https://nebula.kuaishou.com/rest/n/nebula/account/withdraw/setShare"
    headers = {'User-Agent': Agent, 'Accept': '*/*', 'Accept-Language': ' zh-CN,zh;q=0.9', 'Cookie': can_cookie}
    data_can = ""
    data = urllib.parse.urlencode(data_can).encode('utf-8')
    request = urllib.request.Request(url=url, data=data, headers=headers)
    response = urllib.request.urlopen(request)
    str_result = response.read().decode('UTF-8')
    json_arr = json.loads(str_result)
    try:
        if json_arr['result'] == 1:
            print("账号[" + name + "]" + "准备分享任务成功,正在执行分享...")
            url = "https://nebula.kuaishou.com/rest/n/nebula/daily/report?taskId=122"
            request = urllib.request.Request(url=url, headers=headers)
            response = urllib.request.urlopen(request)
            str_result = response.read().decode('UTF-8')
            json_arr = json.loads(str_result)
            if json_arr['result'] == 1:
                print("账号[" + name + "]" + "分享任务成功:" + json_arr['data']['msg'] + str(json_arr['data']['amount']))
            else:
                print("账号[" + name + "]" + "分享任务执行失败:疑似今日已分享." + json_arr['error_msg'])
        else:
            print("账号[" + name + "]" + "准备分享任务失败:" + json_arr['error_msg'])
    except TypeError as reason:
        print("账号[" + name + "]执行任务出错啦" + str(reason) + str_result)


# 依次执行任务
def taskStat():
    i = 0
    for cookie in Cookies:
        i = i + 1
        print("========开始序号[" + str(i) + "]任务========")
        cookie = cookie.replace("@", "")
        json_str = getInformation(cookie)
        code = json_str['code']
        if code == 1:
            name = json_str['data']['nickname']
            # 查询签到
            querySign(cookie, name)
            # 分享任务
            setShare(cookie, name)
            # 开宝箱
            openBox(cookie, name)
        else:
            print("========序号[" + i + "]获取信息失败,请检查cookies是否正确========")

        time.sleep(1)



num = len(Cookies)

if num > 0:
    print("共找到" + str(num) + "个快手变量,开始执行任务...")
    taskStat()
else:
    print("未共找到任务快手变量,请检查您的变量名是否为ksjsbCookie,且多个账号用&分割")

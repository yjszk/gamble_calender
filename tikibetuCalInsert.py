from datetime import datetime
import json
from pprint import pprint
from insertGoogleCal import *
import configparser
import sys


def auth_cal_id(envName):
    config = configparser.ConfigParser()
    config.read('setting.ini')
    calId = config.get(envName, 'calId')
    return calId


def selectGamble(envName):
    if envName == "kyotei":
        shubetuStr = "競艇"
        colorId = "1"
    if envName == "keirin":
        shubetuStr = "競輪"
        colorId = "2"
    if envName == "keiba":
        shubetuStr = "競馬"
        colorId = "3"
    if envName == "autorace":
        shubetuStr = "オートレース"
        colorId = "4"
    if envName == "keiba_jra":
        shubetuStr = "中央競馬"
        colorId = "5"
    return shubetuStr, colorId


def jikanToDatetime(jikan, kaisaiDay):
    rawStr = f'{nowYear}{kaisaiDay}'
    if jikan == 'midnight':
        returnStr = 'ミッドナイト'
        rawDateStart = f'{rawStr} 20:00'
        rawDateEnd = f'{rawStr} 23:30'
        startTime = datetime.strptime(rawDateStart, '%Y%m/%d %H:%M')
        endTime = datetime.strptime(rawDateEnd, '%Y%m/%d %H:%M')
    if jikan == 'nighter':
        rawDateStart = f'{rawStr} 15:00'
        rawDateEnd = f'{rawStr} 20:50'
        startTime = datetime.strptime(rawDateStart, '%Y%m/%d %H:%M')
        endTime = datetime.strptime(rawDateEnd, '%Y%m/%d %H:%M')
        returnStr = 'ナイター'
    if jikan == 'morning':
        returnStr = 'モーニング'
        rawDateStart = f'{rawStr} 09:00'
        rawDateEnd = f'{rawStr} 15:00'
        startTime = datetime.strptime(rawDateStart, '%Y%m/%d %H:%M')
        endTime = datetime.strptime(rawDateEnd, '%Y%m/%d %H:%M')
    if jikan == 'summer':
        returnStr = 'サマータイム'
        rawDateStart = f'{rawStr} 12:30'
        rawDateEnd = f'{rawStr} 18:30'
        startTime = datetime.strptime(rawDateStart, '%Y%m/%d %H:%M')
        endTime = datetime.strptime(rawDateEnd, '%Y%m/%d %H:%M')
    return returnStr, startTime, endTime


def judgeKubun(kubun):
    if kubun == "kanto":
        return '関東', kubun
    if kubun == "tyuokoti":
        return '中央高地', kubun
    if kubun == "hokkaido":
        return '北海道', kubun
    if kubun == "tohoku":
        return '東北', kubun
    if kubun == "hokuriku":
        return "北陸", "tokai"
    if kubun == "tokai":
        return '東海', kubun
    if kubun == "kinki":
        return '近畿', kubun
    if kubun == "tyugoku":
        return '中国', kubun
    if kubun == "sikoku":
        return '四国', kubun
    if kubun == "kyushu":
        return '九州', kubun


nowYear = sys.argv[1]
nowMouth = sys.argv[2]
envName = sys.argv[3]
tikiKubun, kubunName = judgeKubun(sys.argv[4])
calendarId = auth_cal_id(sys.argv[4])
shubetuStr, colorId = selectGamble(envName)

loadJson = json.load(open(f'{nowYear}{nowMouth}{envName}.json'))

for i in loadJson.items():
    for j in i[1]:
        if j.get('tiki') == tikiKubun:
            classs = ""
            if j.get('class') != None:
                classs = j['class']
            if j.get('class') == None:
                classs = ""
            if j.get('jikan') != None:
                jyo = j['jyo']
                jikan, startTime, endTime = jikanToDatetime(
                    j['jikan'], i[0])
                insStr = f'{jyo}{classs}{jikan}{startTime}{endTime}'
                print(insStr)
                insertGoogleCal(f'{jyo}{shubetuStr}',
                                startTime, endTime, colorId, calendarId)
            else:
                jyo = j['jyo']
                startTime = datetime.strptime(
                    f'{nowYear}{i[0]} 12:00', '%Y%m/%d %H:%M')
                endTime = datetime.strptime(
                    f'{nowYear}{i[0]} 17:00', '%Y%m/%d %H:%M')
                jikan = "日中"
                insStr = f'{jyo}{jikan}{startTime}{endTime}'
                print(insStr)
                insertGoogleCal(f'{jyo}{shubetuStr}',
                                startTime, endTime, colorId, calendarId)

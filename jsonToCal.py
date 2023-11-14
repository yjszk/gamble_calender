from datetime import datetime
import json
from pprint import pprint
from insertGoogleCal import *
import configparser
import sys
import asyncio
import time


def asyncInsert(dict, kaisaiday):
    print(dict, kaisaiday)
    classs = ""
    if dict.get('class') != None:
        classs = dict['class']
    if dict.get('class') == None:
        classs = ""
    if dict.get('jikan') != None:
        jyo = j['jyo']
        jikan, startTime, endTime = jikanToDatetime(dict['jikan'], kaisaiday)
        insStr = f'{jyo}{classs}{jikan}{startTime}{endTime}'
        # print(insStr)j
        insertGoogleCal(f'{jyo}{shubetuStr}',
                        startTime, endTime, colorId, calendarId)
    else:
        jyo = dict['jyo']
        startTime = datetime.strptime(
            f'{nowYear}{kaisaiday} 12:00', '%Y%m/%d %H:%M')
        endTime = datetime.strptime(
            f'{nowYear}{kaisaiday} 17:00', '%Y%m/%d %H:%M')
        jikan = "日中"
        insStr = f'{jyo}{jikan}{startTime}{endTime}'
        print(insStr)
        insertGoogleCal(f'{jyo}{shubetuStr}',
                        startTime, endTime, colorId, calendarId)


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


envName = sys.argv[1]
nowYear = sys.argv[2]
nowMouth = sys.argv[3]
calendarId = auth_cal_id(envName)
shubetuStr, colorId = selectGamble(envName)
loadJson = json.load(open(f'{nowYear}{nowMouth}{envName}.json'))

for i in loadJson.items():
    for j in i[1]:
        asyncInsert(j, i[0])

import datetime
import re
import googleapiclient.discovery
import google.auth
import configparser
from pprint import pprint
from datetime import datetime as dt
import sys

shubetu = sys.argv[1]
executeDate = sys.argv[2]
dYear = executeDate[0:4]
dMouth = executeDate[4:6]
dDay = executeDate[6:8]
try:
    dryRun = sys.argv[3]
    dryRunFlag = False
except:
    dryRunFlag = True


def auth_cal_id(envName):
    config = configparser.ConfigParser()
    config.read('setting.ini')
    calId = config.get(envName, 'calId')
    return calId


def strToDatetime(str):
    rawStr = re.search(r'[0-9][0-9][0-9][0-9]-[0-9][0-9]', str).group()
    ifLs = rawStr.split('-')
    return ifLs


def delYotei(eventId):
    result = service.events().delete(calendarId=calendar_id, eventId=eventId).execute()
    return result


# ①Google APIの準備をする
SCOPES = ['https://www.googleapis.com/auth/calendar']
calendar_id = auth_cal_id(shubetu)
# Googleの認証情報をファイルから読み込む
gapi_creds = google.auth.load_credentials_from_file(
    'key.json', SCOPES)[0]
# APIと対話するためのResourceオブジェクトを構築する
service = googleapiclient.discovery.build(
    'calendar', 'v3', credentials=gapi_creds)


# 削除する機関の頭を決定する
now = datetime.datetime(int(dYear), int(dMouth), int(dDay)).isoformat() + 'Z'
event_list = service.events().list(
    calendarId=calendar_id, timeMin=now,
    maxResults=10000, singleEvents=True,
    orderBy='startTime').execute()
countLs = []
for flag, i in enumerate(event_list['items']):
    print(f'{flag+1} 件目の処理')
    countLs.append(i)
    rawDate = i['start']['dateTime']
    print(rawDate)
    ifLs = strToDatetime(rawDate)
    if dryRunFlag:
        print("No Dry Run")
        delYotei(i['id'])
print(f'処理件数:{len(countLs)}')

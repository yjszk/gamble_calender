from util import *


def dayParser(mouth, day):
    return f'{mouth}/{day}'


def getNarTmpDict(url, kaisaiMouth):
    soup = urlToBs4(url)
    table = soup.find('table', {'class': "schedule"})
    calTable = table.find_all("tr")
    tabledHeader1 = 0
    tabledHeader2 = 1
    rowHeader = 0
    tmpDict = {}
    for rf, row in enumerate(calTable):
        if rf != tabledHeader1:
            if rf != tabledHeader2:
                row = row.find_all("td")
                tmpLs = []
                for flag, i in enumerate(row):
                    if flag == rowHeader:
                        jyo = i.get_text()
                        print(jyo)
                    if flag != rowHeader:
                        if i.get_text().strip() == '●':
                            tmpLs.append('D'+dayParser(kaisaiMouth, flag))
                        if i.get_text().strip() == '☆':
                            tmpLs.append('N'+dayParser(kaisaiMouth, flag))
                        if i.get_text().strip() == 'Ｄ':
                            tmpLs.append('D'+dayParser(kaisaiMouth, flag))
                tmpDict[jyo] = tmpLs
    pprint(tmpDict)
    return tmpDict


def dayBaseKeyJsonGet(tmpDict):
    # AIが作った
    new_dict = {}
    for place, dates in tmpDict.items():
        print(place, dates)
        tiki, ken = insertTikiAndKen(place)
        for dt in dates:
            if dt not in new_dict:
                new_dict[dt] = []
            if 'D' in dt:
                new_dict[dt].append(
                    {'jyo': place, 'ken': ken, 'tiki': tiki})
            if 'N' in dt:
                new_dict[dt].append(
                    {'jyo': place, 'ken': ken, 'tiki': tiki})
            if 'J' in dt:
                new_dict[dt].append(
                    {'jyo': place, 'ken': ken, 'tiki': tiki})
    pprint(new_dict)
    return new_dict


def dayKeyFlagRemove(original_dict):
    # jikanキーに適切な値を挿入
    for key in original_dict:
        if key[0] == 'N':
            for jk in original_dict[key]:
                jk['jikan'] = "nighter"
        elif key[0] == 'D':
            for jk in original_dict[key]:
                pass
        elif key[0] == 'J':
            for jk in original_dict[key]:
                jk['class'] = "jusho"
    # 先頭の文字列を取り除いた新しい辞書を作成
    new_dict = {}
    for key, value in original_dict.items():
        new_key = key[1:]  # キーの先頭の文字列を取り除く
        if new_key in new_dict:
            new_dict[new_key] += value  # 既にキーがある場合は統合する
        else:
            new_dict[new_key] = value
    pprint(new_dict)
    return new_dict

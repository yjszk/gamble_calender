from util import *
from narUtil import *
import sys

print(sys.argv)
kaisaiMouth = sys.argv[1]
kaisaiYear = sys.argv[2]
shubetuFlag = sys.argv[3]
print(kaisaiMouth, kaisaiYear, shubetuFlag)

if shubetuFlag == "keiba_jra":
    jsonRawKeiba = netkeibaJraGetCalPt2(
        f'https://race.netkeiba.com/top/calendar.html?year={kaisaiYear}&month={kaisaiMouth}', kaisaiMouth)
    jsonDump(jsonRawKeiba, f'{kaisaiYear}{kaisaiMouth}keiba_jra.json')

if shubetuFlag == "keiba":
    jsonRawKeiba = getNarTmpDict(
        f'https://www.keiba.go.jp/KeibaWeb/MonthlyConveneInfo/MonthlyConveneInfoTop?k_year={kaisaiYear}&k_month={kaisaiMouth}', kaisaiMouth)
    jsonKeyBaseKeiba = dayBaseKeyJsonGet(jsonRawKeiba)
    jsonKeyBaseKeiba = dayKeyFlagRemove(jsonKeyBaseKeiba)
    jsonDump(jsonKeyBaseKeiba, f'{kaisaiYear}{kaisaiMouth}keiba.json')

if shubetuFlag == "keirin":
    keirinJson = netkeirinSc(
        f'https://keirin.netkeiba.com/race/race_calendar/?kaisai_year={kaisaiYear}&kaisai_month={kaisaiMouth}')
    jsonDump(keirinJson, f'{kaisaiYear}{kaisaiMouth}keirin.json')

if shubetuFlag == "autorace":
    autoRaceBaseurl = "https://www.oddspark.com/autorace/KaisaiRaceList.do?raceDy="
    autoRaceLs = MouthUrlParser(
        autoRaceBaseurl, autoRaceGetCal, kaisaiMouth, kaisaiYear)
    jsonDump(autoRaceLs, f'{kaisaiYear}{kaisaiMouth}autorace.json')

if shubetuFlag == "kyotei":
    kyoteiBaseUrl = "https://www.boatrace.jp/owpc/pc/race/index?hd="
    kyoteiLs = MouthUrlParser(
        kyoteiBaseUrl, kyoteiGetCal, kaisaiMouth, kaisaiYear)
    jsonDump(kyoteiLs, f'{kaisaiYear}{kaisaiMouth}kyotei.json')

if shubetuFlag == "all":
    jsonRawKeiba = netkeibaGetCal(
        f'https://nar.netkeiba.com/top/calendar.html?year={kaisaiYear}&month={kaisaiMouth}', kaisaiMouth)
    jsonDump(jsonRawKeiba, 'keiba.json')
    keirinJson = netkeirinSc(
        f'https://keirin.netkeiba.com/race/race_calendar/?kaisai_year={kaisaiYear}&kaisai_month={kaisaiMouth}')
    jsonDump(keirinJson, 'keirin.json')
    autoRaceBaseurl = "https://www.oddspark.com/autorace/KaisaiRaceList.do?raceDy="
    autoRaceLs = MouthUrlParser(
        autoRaceBaseurl, autoRaceGetCal, kaisaiMouth, kaisaiYear)
    jsonDump(autoRaceLs, 'autorace.json')
    kyoteiBaseUrl = "https://www.boatrace.jp/owpc/pc/race/index?hd="
    kyoteiLs = MouthUrlParser(
        kyoteiBaseUrl, kyoteiGetCal, kaisaiMouth, kaisaiYear)
    jsonDump(kyoteiLs, 'kyotei.json')

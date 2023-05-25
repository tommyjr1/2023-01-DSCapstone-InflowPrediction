import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
import datetime as dt
from glob import glob
import os


def parse(item, date, time):
    datetime = dt.datetime(date.year, date.month, date.day, time, 0, 0)
    try:
        damnm = item.find("damnm").get_text()
        dvlpqyacmtlacmslt = item.find("dvlpqyacmtlacmslt").get_text()
        dvlpqyacmtlplan = item.find("dvlpqyacmtlplan").get_text()
        dvlpqyacmtlversus = item.find("dvlpqyacmtlversus").get_text()
        dvlpqyfyerplan = item.find("dvlpqyfyerplan").get_text()
        dvlpqyfyerversus = item.find("dvlpqyfyerversus").get_text()
        inflowqy = item.find("inflowqy").get_text()
        lastlowlevel = item.find("lastlowlevel").get_text()
        lastrsvwtqy = item.find("lastrsvwtqy").get_text()
        nowlowlevel = item.find("nowlowlevel").get_text()
        nowrsvwtqy = item.find("nowrsvwtqy").get_text()
        nyearlowlevel = item.find("nyearlowlevel").get_text()
        nyearrsvwtqy = item.find("nyearrsvwtqy").get_text()
        oyaacurf = item.find("oyaacurf").get_text()
        prcptqy = item.find("prcptqy").get_text()
        pyacurf = item.find("pyacurf").get_text()
        rsvwtrt = item.find("rsvwtrt").get_text()
        suge = item.find("suge").get_text()
        totdcwtrqy = item.find("totdcwtrqy").get_text()
        totdcwtrqyjo = item.find("totdcwtrqyjo").get_text()
        vyacurf = item.find("vyacurf").get_text()
        zerosevenhourprcptqy = item.find("zerosevenhourprcptqy").get_text()
        return {
            "댐이름": damnm,
            "시간": datetime,
            "발전량(실적)": dvlpqyacmtlacmslt,
            "발전량(계획)": dvlpqyacmtlplan,
            "발전량(계획대비)": dvlpqyacmtlversus,
            "연간발전계획": dvlpqyfyerplan,
            "연간계획대비": dvlpqyfyerversus,
            "전일유입량": inflowqy,
            "저수위(전년)": lastlowlevel,
            "저수량(전년)": lastrsvwtqy,
            "저수위(현재)": nowlowlevel,
            "저수량(현재)": nowrsvwtqy,
            "저수위(예년)": nyearlowlevel,
            "저수량(예년)": nyearrsvwtqy,
            "예년누계강우량": oyaacurf,
            "강우량전일": prcptqy,
            "금년누계강우량": pyacurf,
            "현재저수율": rsvwtrt,
            "수계": suge,
            "전일방류량(본댐)": totdcwtrqy,
            "전일방류량(조정지)": totdcwtrqyjo,
            "전년누계강우량": vyacurf,
            "강우량금일": zerosevenhourprcptqy
        }
    except AttributeError as e:
        return {
            "댐이름": None,
            "시간": None,
            "발전량(실적)": None,
            "발전량(계획)": None,
            "발전량(계획대비)": None,
            "연간발전계획": None,
            "연간계획대비": None,
            "전일유입량": None,
            "저수위(전년)": None,
            "저수량(전년)": None,
            "저수위(현재)": None,
            "저수량(현재)": None,
            "저수위(예년)": None,
            "저수량(예년)": None,
            "예년누계강우량": None,
            "강우량전일": None,
            "금년누계강우량": None,
            "현재저수율": None,
            "수계": None,
            "전일방류량(본댐)": None,
            "전일방류량(조정지)": None,
            "전년누계강우량": None,
            "강우량금일": None
        }


def collect(startY, startM, startD, endY, endM, endD, serviceKey, url):
    # 시작할 날짜
    date = dt.datetime(startY, startM, startD)
    # 끝날 날짜
    while (date < dt.datetime(endY, endM, endD)):
        row = []
        vdate = date
        tdate = date-dt.timedelta(days=1)
        ldate = date-dt.timedelta(days=365)

        for i in range(1, 25):
            str_i = str(i).zfill(2)
            params = {'serviceKey': serviceKey, 'tdate': tdate.strftime("%Y-%m-%d"),
                      'ldate': ldate.strftime("%Y-%m-%d"), 'vdate': vdate.strftime("%Y-%m-%d"),
                      'vtime': str_i, 'numOfRows': '21'}

            response = requests.get(url, params=params)
            soup = bs(response.text, 'lxml-xml')

            items = soup.find_all('item')
            for item in items:
                row.append(parse(item, vdate, i-1))
        df2 = pd.DataFrame(row)
        df2 = df2[df2["댐이름"] == "합천"]
        df2.to_csv("./합천다목적댐/합천다목적댐_" +
                   vdate.strftime("%Y-%m-%d")+".csv", index=False)
        date = date+dt.timedelta(days=1)


def concat(startY, endY):
    file_names = glob("../data/합천다목적댐_전체원본/*.csv")

    total = pd.DataFrame()
    for file_name in file_names:
        temp = pd.read_csv(file_name, encoding='utf-8', low_memory=False)
        temp = temp[temp["댐이름"] == "합천"]
        total = pd.concat([total, temp], ignore_index=True)

    total.dropna(subset=['시간'], how='any', axis=0, inplace=True)
    total.drop(['댐이름', '수계', 'Unnamed: 0'], axis=1, inplace=True)
    total['당일유입량'] = total['전일유입량'][24:].reset_index()['전일유입량']
    total = total.iloc[:-24,]
    total['시간'] = pd.to_datetime(total['시간'])
    total = total.set_index(keys='시간')
    total.sort_index(inplace=True)
    total = total[total.index.year >= startY]

    for feature in total.columns[1:]:
        total[feature] = total[feature].astype(
            str).str.replace(',', '').astype(float)

    total = total.resample(rule='H').mean()
    total = total.interpolate(method='linear')
    total.ffill(inplace=True)
    total.bfill(inplace=True)
    total['홍수기'] = 0
    for year in range(2000, 2024):
        start_date = dt.datetime(year, 6, 21)  # 시작 날짜 (6월 21일)
        end_date = dt.datetime(year, 9, 21, 0, 0, 0)  # 종료 날짜 (9월 20일)

        total.loc[(total.index.to_pydatetime() >= start_date) & (
            total.index.to_pydatetime() < end_date), '홍수기'] = 1
    total.to_csv(f"../data/합천다목적댐_전체.csv")

    total_daily = total.resample(rule='D').mean()
    total_daily.to_csv(f"../data/합천다목적댐_전체_일별.csv")

import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
import datetime as dt
from utils.damlib import collect, concat


url = 'http://opendata.kwater.or.kr/openapi-data/service/pubd/dam/multipurPoseDam/list'
serviceKey = "링크에서 운영계정으로 신청하고, 받은 encoding 키"


if __name__ == '__main__':
    startY = 2000
    endY = dt.datetime.today().year
    endM = dt.datetime.today().month
    endD = dt.datetime.today().day
    # collect(startY, 1, 1, endY, endM, endD, serviceKey, url)
    concat(startY, endY)

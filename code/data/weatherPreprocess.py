import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
import datetime as dt
from utils.weatherlib import concat

if __name__ == '__main__':
    startY = 2000
    endY = dt.datetime.today().year
    concat(startY, endY)

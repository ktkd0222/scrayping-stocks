import os
import time
import random
import requests

TARGET_URL = 'https://kabuoji3.com/stock/file.php'
#TARGET_BRANDS = [4755, 4506, 6047, 9201, 9202]
TARGET_BRANDS = [4307]
START_YEAR = 2016
END_YEAR = 2021
TARGET_YEARS  = list(range(START_YEAR, END_YEAR + 1))
IS_DEBUG = False
DATA_DIR = './datas'
UA = r'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1'

header = {'User-Agent': UA}
print(os.getcwd())

for brand in TARGET_BRANDS:
    # make output dirs
    os.makedirs(os.path.join(DATA_DIR, str(brand)), exist_ok=True)
    for year in TARGET_YEARS:
        print(f'get brand is {brand} / year is {year}')
        data = {'code': brand, 'year': year, 'csv': ''}
        response = requests.post(TARGET_URL, data=data, headers=header)
        #print(response.text)
        output_file = os.path.join(os.path.join(DATA_DIR, str(brand)), f'{brand}_{year}.csv')
        with open(output_file, mode='wb') as f:
            f.write(response.text.encode('shift-jis'))
        print(f'download and output stock data is finished. url:{TARGET_URL} brand:{brand} / year:{year}')
        if IS_DEBUG:
            wait_time = 0.5
        else:
            wait_time = random.randint(5,10) + random.random()
        print(f'wait time is {wait_time}s')
        time.sleep(wait_time)
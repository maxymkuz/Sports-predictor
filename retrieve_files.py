from kaggle.api.kaggle_api_extended import KaggleApi

api = KaggleApi()
api.authenticate()

api.dataset_download_files('hugomathien/soccer')

import csv
import requests

CSV_URL = 'https://raw.githubusercontent.com/vijinho/epl_mysql_db/master/csv/E0-2016.csv'

with requests.Session() as s:
    download = s.get(CSV_URL)
    decoded_content = download.content.decode('utf-8')

    cr = csv.reader(decoded_content.splitlines(), delimiter=',')
    my_list = list(cr)
    # Вивід на екран
    i = 0
    for row in my_list:
        print(row)
        i += 1
        if i >= 15:
            break

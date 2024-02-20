import pandas as pd
import requests
from bs4 import BeautifulSoup
from pathlib import Path
import datetime
import os

# TODO 新公式、もしかして自動化できるかも？
# GitHubではtimezoneがUTC指定。
# now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))
now = datetime.datetime.now()
today_str = now.strftime("%Y%m%d")
const_dir = 'out/jpn_detective/'
Path(const_dir).mkdir(parents=True, exist_ok=True)

# 6日分はさかのぼれそう。毎日実行しても動くようにはなっている
for dr in range(0,6):
    today_str = str((now + datetime.timedelta(days=-dr)).strftime("%Y%m%d"))
    print(today_str)
    for sn in range(1,4):
        url = 'https://www.redstoneonline.jp/rank?t=2&s=WORLD0'+str(sn)+'&c=&d='
        print(url)
        response = requests.get(url)
        response.raise_for_status()
        html_ranking = response.text
        print(html_ranking)
        mat = []  # 保存先の行列
        soup = BeautifulSoup(html_ranking, 'html.parser')
        # FIXME 構造みて判断する
        table = soup.find('table')
        # table = soup.find('table', {'data-v-d31fa134': ''})
        print(table)
        # theadの解析
        r = [] 
        thead = table.find('thead') 
        ths = thead.tr.find_all('th')
        for th in ths: 
            r.append(th.text)

        mat.append(r) 

        # tbodyの解析
        tbody = table.find('tbody')
        trs = tbody.find_all('tr')
        for tr in trs:
            r = []
            for td in tr.find_all('td'): 
                r.append(td.text) 
            mat.append(r)

        # 出力
        # for r in mat:
        #     print(','.join(r))  # カンマ（,）で列を結合して表示

        t_server = str(today_str) + '_' + str(sn)

        with open(const_dir + t_server + ".csv", "w", encoding='utf-8') as f:
            for r in mat:
                f.write(','.join(r))
                f.write('\n')

        # ファイル量多くなるとGitHubから怒られるので1年以上前のファイルは削除
        # gitのcommitlog辿れば過去のデータ手に入るしいいよね理論
        last_year_str = str((now + datetime.timedelta(days=-367)).strftime("%Y%m%d"))
        tl_server = str(last_year_str) + '_' + str(sn)
        last_year_file = const_dir  + tl_server + ".csv"
        print("delete:" + str(last_year_file))
        if os.path.exists(last_year_file):
            os.remove(last_year_file)

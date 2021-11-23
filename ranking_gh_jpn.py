import pandas as pd
import requests
from bs4 import BeautifulSoup
from pathlib import Path
import datetime
import os
import time

now = datetime.datetime.now()
today_str = now.strftime("%Y%m%d")
const_dir = 'out/jpn_gh/'
Path(const_dir).mkdir(parents=True, exist_ok=True)
server_num = [1,3,5]
server_name = ["n", "strasserad", "b", "vaultish","w","bridgehead"]
job_num = [5,1,3]

for sn in server_num:
    print("server:" + str(server_name[sn]))
    for jn in job_num:
        print("gh-rank:" + str(jn))
        mat = []
        r = []

        url = 'https://members.redsonline.jp/game_info/community/ranking/guild.asp?act=search&world=' +str(sn) +'&guildhallrank=' +str(jn)
        if jn == 5:
            url = 'https://members.redsonline.jp/game_info/community/ranking/guild.asp'
            # 3鯖分のGH5が重複生成されないように対処
            # TODO 金鯖ある期間これで動くか？
            if sn != 1:
                continue
        response = requests.get(url)
        html_ranking = response.content
        soup = BeautifulSoup(html_ranking, 'html.parser', from_encoding="shift-jis")
        table = soup.find('table', class_='guild')

        trs = table.find_all('tr')
        cnt = 0
        for tr in trs:
            r = []
            for td in tr.find_all('td'):
                r.append(td.text)
                # 最初の2行は必ず空なので弾く
            if cnt < 1: 
                cnt = cnt+1
                continue
            mat.append(r)

        # 出力
        # for r in mat:
        #     print(','.join(r))  # カンマ（,）で列を結合して表示

        t_server = str(today_str) + '_' + str(server_name[sn]) + '_' + str(jn)

        with open(const_dir + t_server + ".csv", "w", encoding='utf-8') as f:
            for r in mat:
                f.write(','.join(r))
                f.write('\n')

        # ファイル量多くなるとGitHubから怒られるので1年以上前のファイルは削除
        # gitのcommitlog辿れば過去のデータ手に入るしいいよね理論
        last_year_str = str((now + datetime.timedelta(days=-367)).strftime("%Y%m%d"))
        tl_server = str(last_year_str) + '_' + str(server_name[sn]) + '_' + str(jn)
        last_year_file = const_dir  + tl_server + ".csv"
        print("delete:" + str(last_year_file))
        if os.path.exists(last_year_file):
            os.remove(last_year_file)
time.sleep(5.0)

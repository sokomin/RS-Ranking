import pandas as pd
import requests
from bs4 import BeautifulSoup
from pathlib import Path
import datetime
import os

now = datetime.datetime.now()
today_str = now.strftime("%Y%m%d")
Path('out/jpn_lv/').mkdir(parents=True, exist_ok=True)
headers_dic = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"}

server_num = [1,3,5]
server_name = ["n", "strasserad", "b", "vaultish","w","bridgehead"]

# job_num = [0,1,2,3,4,5,6,7,8,9,10,20,22]
job_num = [9] #デバッグ用、普段はコメントアウト

for jn in job_num:
    print("job number:" + str(jn))
    for sn in server_num:
        print("server:" + str(server_name[sn]))
        mat = []  # 保存先の行列
        r = []  # 保存先の行

        for pg in range(1,11):
            url = 'https://members.redsonline.jp/game_info/community/ranking/ranking.asp?page='+ str(pg) +'&world=' +str(sn) +'&job=' +str(jn) +'&Page_Size=100'
            response = requests.get(url, headers=headers_dic)
            # print(response.raise_for_status())
            html_ranking = response.content
            soup = BeautifulSoup(html_ranking, 'html.parser', from_encoding="shift-jis")
            table = soup.find('table', class_='personal')

            trs = table.find_all('tr')
            cnt = 0
            for tr in trs:
                r = []
                for td in tr.find_all('td'):
                    r.append(td.text)
                    # 最初の3行は必ず空なので弾く
                if cnt < 2: 
                    cnt = cnt+1
                    continue
                mat.append(r)

        # 出力テスト
        # for r in mat:
        #     print(','.join(r))  # カンマ（,）で列を結合して表示

        t_server = str(today_str) + '_' + str(server_name[sn]) + '_' + str(jn)

        with open('out/jpn_lv/' + t_server + ".csv", "w", encoding='utf-8') as f:
            for r in mat:
                f.write(','.join(r))
                f.write('\n')

        # ファイル量多くなるとGitHubから怒られるので1年以上前のファイルは削除
        # gitのcommitlog辿れば過去のデータ手に入るしいいよね理論
        last_year_str = str((now + datetime.timedelta(days=-367)).strftime("%Y%m%d"))
        tl_server = str(last_year_str) + '_' + str(server_name[sn]) + '_' + str(jn)
        last_year_file = 'out/jpn_lv/'  + tl_server + ".csv"
        print("delete:" + str(last_year_file))
        if os.path.exists(last_year_file):
            os.remove(last_year_file)

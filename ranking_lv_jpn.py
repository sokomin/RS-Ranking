import pandas as pd
import requests
from bs4 import BeautifulSoup
from pathlib import Path
import datetime
import os
import time

now = datetime.datetime.now()
today_str = now.strftime("%Y%m%d")
Path('out/jpn_lv/').mkdir(parents=True, exist_ok=True)
# どれかが必要だけど、わからん。proxy必要だったら詰む
headers_dic = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", 
    "Accept-Encoding": "gzip, deflate, br", 
    "Accept-Language": "ja-JP,ja;q=0.9,en-UM;q=0.8,en;q=0.7,en-US;q=0.6,zh-TW;q=0.5,zh;q=0.4", 
    "Host": "httpbin.org", 
    "Sec-Ch-Ua": "' Not A;Brand';v='99', 'Chromium';v='96', 'Google Chrome';v='96'", 
    "Sec-Ch-Ua-Platform": "'Windows'", 
    "Sec-Fetch-Dest": "document", 
    "Sec-Fetch-Mode": "navigate", 
    "Sec-Fetch-Site": "none", 
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
}
headers_dic = {}

server_num = [1,3,5,7]
server_name = ["n", "strasserad", "b", "vaultish","w","bridgehead","g","gold"]

job_num = [0,1,2,3,4,5,6,7,8,9,10,20,22,24]
# job_num = [9] #デバッグ用、普段はコメントアウト

for jn in job_num:
    print("job number:" + str(jn))
    for sn in server_num:
        print("server:" + str(server_name[sn]))
        mat = []  # 保存先の行列
        r = []  # 保存先の行
        # ファイルの存在チェック（何度も取得しないように）
        t_server = str(today_str) + '_' + str(server_name[sn]) + '_' + str(jn)
        out_file_name = 'out/jpn_lv/' + t_server + '.csv'
        if os.path.exists(out_file_name):
            print("File exist...")
            continue

        for pg in range(1,11):
            surl = sn
            if sn == 7:
                surl = 25
            url = 'https://members.redsonline.jp/game_info/community/ranking/ranking.asp?page='+ str(pg) +'&world=' +str(surl) +'&job=' +str(jn) +'&Page_Size=100'
            response = requests.get(url, headers=headers_dic)
            # response.encoding = response.apparent_encoding  # 文字化け回避用
            response.encoding="shift-jis"
            # response.encoding="utf-8"
            # response.apparent_encoding="shift-jis"
            # print(response.raise_for_status())
            html_ranking = response.text
            # soup = BeautifulSoup(html_ranking, 'html.parser', from_encoding="shift-jis")
            soup = BeautifulSoup(html_ranking, 'html.parser')
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

        with open(out_file_name, "w", encoding='utf-8') as f:
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
time.sleep(5.0)
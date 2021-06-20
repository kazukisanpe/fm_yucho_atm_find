from bs4 import BeautifulSoup    # importする
import sys
import requests
import re
import time

#実行処理時間計測開始
start = time.time()
#引数を取得
args = sys.argv
search_pref = args[1]
#search_pref = "東京都府中"
kyouto_flg = 0
if search_pref == "京都府" or search_pref == "京都":
    kyouto_flg = 1

# Webページを取得して解析する
load_url = "https://tamatora.36nyan.com/?p=6347#i-9"
html = requests.get(load_url)
soup = BeautifulSoup(html.text, "html.parser")

elems = soup.find_all(href=re.compile("https://map.japanpost.jp/smt/search/inf/")) 

#表示する
print(search_pref + "のゆうちょATMのある店舗を表示")
cnt = 0
for elem in elems:
    if search_pref in elem.contents[0]:
        #"京都府"を検索した際に"東京都府中"の地名も混ざってしまうため
        if elem.contents[0][0:3] != "京都府" and kyouto_flg == 1:
            continue
        #店舗数インデックス
        cnt = cnt + 1
        #住所に載ってるリンクの遷移ページより店名を取得
        html_2 = requests.get(elem.attrs['href'])
        soup_2 = BeautifulSoup(html_2.text, "html.parser")
        elems_2 = soup_2.select_one("[class='icon-heading03']")
        #店舗名が取得できたかできていないか
        if elems_2 != None:
            #店名を出力
            print(str(cnt) + ":" + elems_2.contents[0])
            #お店の住所を表示
            print("住所：" + elem.contents[0])

        else:
            #改行
            print("\n")
            #取得失敗(店舗情報削除)
            print("\"" + elem.contents[0]+ "\"" + "のファミリーマートは現在存在していないか情報がありません")
            #改行
            print("\n")
        
if cnt == 0:
    print("店舗が存在しません")
#計測処理時間を出力
elapsed_time = time.time() - start
#print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")
print ("実行結果:{:.2f}".format(elapsed_time) + "[sec]")
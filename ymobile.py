"""
概要
MyYmobileからスクレイピングして、通信容量の残量を抜き出してくるスクリプトです。
雑な実装ですが、一応役に立つ人がいるかもしれないので残しておきます。
必要ライブラリはrequestsとBeautifulSoup4だったと思います。
PhoneNumberとpasswordを入れたら動くと思います。
お好きなものと組み合わせてお使いください。
参考記事
- https://qiita.com/p_q/items/b7c951988b5ea6c866d3
- https://takeanote.blog.jp/archives/1078569625.html
"""
import requests				# HTTP通信ライブラリ
from bs4 import BeautifulSoup as bs


def get_info(PhoneNumber, password):
    def login():
        s = requests.Session()
        r = s.get('https://my.ymobile.jp/muc/d/webLink/doSend/MWBWL0130')
        soup = bs(r.text,'html.parser')
        ticket = soup.find('input',type='hidden').get('value')
        payload = {
            'telnum': PhoneNumber,
            'password': password,
            'ticket':ticket
        }
        s.post('https://id.my.ymobile.jp/sbid_auth/type1/2.0/login.php', data=payload)
        return s

    def get_data(s):
        r = s.get('https://my.ymobile.jp/muc/d/webLink/doSend/MRERE0000')
        soup = bs(r.text,'html.parser')
        auth_token = soup.find_all('input')
        payload = {
            'mfiv': auth_token[0].get('value'),
            'mfym': auth_token[1].get('value'),
        }
        req = s.post('https://re61.my.ymobile.jp/resfe/top/', data=payload)
        data = bs(req.text,'html.parser')
        return data


    data = get_data(login())

    #print(data)

    print("\n\n\n")
    ds=data.find(class_="list-toggle-content js-toggle-content m-top-20").find_all("table")
    #print(ds[0].find("tbody").find("td").text.replace("		","").replace("\n",""))
    #print(ds[1].find("tbody").find_all("tr")[1].find("td").text.replace("		","").replace("\n",""))
    #print(ds[2].find("tbody").find("tr").find("td").text.replace("	","").replace("\n",""))
    #print(ds[3].find("tbody").find("tr").find("td").text.replace("		","").replace("\n",""))
    return {
        "kurikoshi":float(ds[0].find("tbody").find("td").text.replace("		","").replace("\n","").replace("GB","")),
        "kihon":float(ds[1].find("tbody").find_all("tr")[1].find("td").text.replace("		","").replace("\n","").replace("GB","")),
        "yuryou":float(ds[2].find("tbody").find("tr").find("td").text.replace("	","").replace("\n","").replace("GB","")),
        "used":float(ds[3].find("tbody").find("tr").find("td").text.replace("		","").replace("\n","").replace("GB",""))
    }

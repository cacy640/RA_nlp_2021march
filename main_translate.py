import pandas as pd
import execjs
import time
import requests
import json
from concurrent.futures import ThreadPoolExecutor
proxyUser = '627161197791563776'
proxyPass = 'dpd2UuiK'
proxyHost = "http-dynamic.xiaoxiangdaili.com"
proxyPort = "10030"
proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
    "host": proxyHost,
    "port": proxyPort,
    "user": proxyUser,
    "pass": proxyPass,
}

proxies = {
    "http": proxyMeta,
    "https": proxyMeta,
}
class Py4Js():

    def __init__(self):
        self.ctx = execjs.compile("""
        function TL(a) {
        var k = "";
        var b = 406644;
        var b1 = 3293161072;

        var jd = ".";
        var $b = "+-a^+6";
        var Zb = "+-3^+b+-f";

        for (var e = [], f = 0, g = 0; g < a.length; g++) {
            var m = a.charCodeAt(g);
            128 > m ? e[f++] = m : (2048 > m ? e[f++] = m >> 6 | 192 : (55296 == (m & 64512) && g + 1 < a.length && 56320 == (a.charCodeAt(g + 1) & 64512) ? (m = 65536 + ((m & 1023) << 10) + (a.charCodeAt(++g) & 1023),
            e[f++] = m >> 18 | 240,
            e[f++] = m >> 12 & 63 | 128) : e[f++] = m >> 12 | 224,
            e[f++] = m >> 6 & 63 | 128),
            e[f++] = m & 63 | 128)
        }
        a = b;
        for (f = 0; f < e.length; f++) a += e[f],
        a = RL(a, $b);
        a = RL(a, Zb);
        a ^= b1 || 0;
        0 > a && (a = (a & 2147483647) + 2147483648);
        a %= 1E6;
        return a.toString() + jd + (a ^ b)
    };

    function RL(a, b) {
        var t = "a";
        var Yb = "+";
        for (var c = 0; c < b.length - 2; c += 3) {
            var d = b.charAt(c + 2),
            d = d >= t ? d.charCodeAt(0) - 87 : Number(d),
            d = b.charAt(c + 1) == Yb ? a >>> d: a << d;
            a = b.charAt(c) == Yb ? a + d & 4294967295 : a ^ d
        }
        return a
    }
    """)

    def getTk(self, text):
        return self.ctx.call("TL", text)
def  buildUrl(text, tk):
    baseUrl = 'https://translate.google.cn/translate_a/single?client=webapp&sl=auto&tl=en&hl=en&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=sos&dt=ss&dt=t&source=bh&ssel=0&tsel=0&xid=45662847&kc=1&'
    ########## https://translate.google.cn/translate_a/single?client=webapp&sl=auto&tl=ja&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=sos&dt=ss&dt=t&source=bh&ssel=0&tsel=0&xid=45662847&kc=1&tk=267041.175848
    baseUrl += 'tk=' + str(tk)
    # baseUrl+='&q='+text
    return baseUrl

def translate( text):

    url = buildUrl(text, js.getTk(text))
    res = ''
    data = {
        'q': text
    }
    try:
        done = 0
        c1 = 0
        c2 = 0
        while done == 0:
            if c1 == 5:
                return 'error'
            try:
                #r = requests.post(url, timeout=1, data=data)
                r = requests.post(url, timeout=3 ,data=data,proxies=proxies)
                if r.status_code == 200:
                    done = 1
                else:
                    c1 = 1 + c1
                    print(r.status_code)
            except:
                c2 += 1
        result = json.loads(r.text)
        res = ''
        for i in result[0]:
            if i[0] == None:
                continue
            res = res + str(i[0])
    except Exception as e:
        res = 'error'
        print(url)
        print("翻译" + text + "失败")
        print("错误信息:")
        print(e)
    finally:
        if len(res)<10:
            a=1
        return res
def gettext(stxt):
    pass
def trans1(item):
    buff = []
    num,stxt=item
    txts=stxt.split('.')
    result=''
    txt = txts[0]
    for index,source in enumerate(txts[1:]):
        if len(txt+'.'+source)<3000:
            txt=txt+'.'+source
            if source==txts[-1]:
                buff.append(txt)
        else:
            buff.append(txt)
            txt=source
    for bu in buff:
        ttxt = translate(bu)
        result+=ttxt

    newbody.append([num,result])
    print([num,result])
def trans2(item):
    index,stxt=item
    ttxt=translate(stxt)
    print(ttxt)
    newtitle.append([index,ttxt])
if __name__ == '__main__':

    results=[]
    buffsou=[]
    js = Py4Js()
    df=pd.read_csv('1.csv',encoding='utf8')
    newtitle=[]
    newbody=[]

    folha_de_sp_title=df['folha_de_sp_title'].tolist()
    folha_de_sp_body=df['folha_de_sp_body'].tolist()
    items=[]
    for index ,body in enumerate(folha_de_sp_title):
        print(index ,body)
        items.append([index,body])
    with ThreadPoolExecutor(8) as ex:
        ex.map(trans2,items)
    items = []
    for index ,body in enumerate(folha_de_sp_body):
        print(index ,body)
        items.append([index,body])
    with ThreadPoolExecutor(6) as ex:
        ex.map(trans1,items)

    new1=pd.DataFrame(newtitle)
    new2=pd.DataFrame(newbody)
    new1.to_excel('title1.xlsx',index=None)
    new2.to_excel('body1.xlsx', index=None)

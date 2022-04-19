from .httpclient import HttpClient
from bs4 import BeautifulSoup as bs
import base64
import json

req = HttpClient()

raw_domain = "https://rapid-cloud.ru:443"
domain = base64.b64encode(raw_domain.encode()).decode().replace("\n", "").replace("=", ".")


def gettoken(key):
    '''
    function to generate token
    '''
    
    r=req.get("https://www.google.com/recaptcha/api.js?render="+key,headers={'cacheTime':'0'})
    s=r.text.replace("/* PLEASE DO NOT COPY AND PASTE THIS CODE. */","")
    s=s.split(";")
    vtoken = s[10].replace("po.src=","").split("/")[-2]

    r=req.get("https://www.google.com/recaptcha/api2/anchor?ar=1&hl=en&size=invisible&cb=cs3&k="+key+"&co="+domain+"&v="+vtoken)
    
    soup = bs(r.content, "html.parser")
    recap_token = [i['value'] for i in soup.select("#recaptcha-token")][0]
    
    data = {
        "v" : vtoken,
        "k" : key,
        "c" : recap_token,
        "co" : domain,
        "sa" : "",
        "reason" :"q"
    }
    
    headers ={'cacheTime':'0'}
    
    j = json.loads(
        req.post("https://www.google.com/recaptcha/api2/reload?k="+key,data=data,headers=headers).text.replace(")]}'",'')
    )
    
    return j[1]

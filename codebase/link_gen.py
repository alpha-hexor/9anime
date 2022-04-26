from .httpclient import HttpClient
from bs4 import BeautifulSoup as bs
from .captcha import *
from .m3u8 import *
import sys

req = HttpClient()
#some global shit
main_url = "https://9anime.se"

def ask_sub_dub():
    """
    ask for sub or dub
    """
    x = input(("[S]ubbed or [D]ubbed: ")).lower()
    if x == "s":
        return "sub"
    else:
        return "dub"

def get_rapid_link(ep_id):
    '''
    functin to get rabbid link url
    '''
    x={}
    r=req.get(f"{main_url}/ajax/episode/servers?episodeId={ep_id}",headers={"X-Requested-With":"XMLHttpRequest"})
    soup = bs(r.json().get("html"),"html.parser")
    x["sub"] = [i.select(".item")[0]["data-id"] for i in soup.select(".servers-sub")][0]
    try:
        x["dub"] = [i.select(".item")[0]["data-id"] for i in soup.select(".servers-dub")][0]
    except:
        x["dub"] = ""
    server_id = x[ask_sub_dub()]
    
    if server_id == "":
        sys.exit()
    
    #get the link
    r=req.get(
        f"{main_url}/ajax/episode/sources?id={server_id}",
        headers={"X-Requested-With":"XMLHttpRequest"}
    )
    
    link = r.json().get("link")
    
    return link

def get_final_links(link):
    '''
    function to get final links
    '''
 
    
    #https://rapid.net/embed-4/cGAGPSIA8PFI?z= --> cGAGPSIA8PFI
    
    rapid_id = link.split("/")[-1].split("?")[0]
    
    r=req.get(
        
        link,
        
        headers={
            'referer' : main_url
        }
    )
    
    soup = bs(r.content,'html.parser')
    num = [i.text for i in soup.find_all("script")][-3].replace("var","")
    x=str(num).split(",")
    key=x[0].split("= ")[-1].replace("'","")
    times=x[1].split("= ")[-1].replace("'","")
    
    token = gettoken(key)
    
    x = req.get(f"https://rapid-cloud.ru/ajax/embed-6/getSources?id={rapid_id}&_token={token}&_number={times}",headers={'X-Requested-With': 'XMLHttpRequest'}).json()
    

    '''
    subtitle part
    '''
    languages = [x["tracks"][i]["label"] for i in range(len(x["tracks"])-1)]        
    subtitles = [x["tracks"][i]["file"] for i in range(len(x["tracks"])-1)]
    
    subs = [list(sublist) for sublist in zip(languages,subtitles)]
    '''
    final link part
    '''
    final_link = x["sources"][0]["file"]
    
    
    qualities,links = get_m3u8_quality(final_link)
    q=[list(qlist) for qlist in zip(qualities,links)]    
    
    return subs,q  
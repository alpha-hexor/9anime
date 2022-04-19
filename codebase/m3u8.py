from .httpclient import HttpClient
import regex
req = HttpClient()
#regex 
start_regex = regex.compile(r"#EXT-X-STREAM-INF(:.*?)?\n+(.+)")
res_regex = regex.compile(r"RESOLUTION=\d+x(\d+)")




def get_m3u8_quality(link):
    
    links = []
    qualities = []
    
    partial_link = link[:link.rfind('/')+1]
    
    r=req.get(link)
    
    
    for i in start_regex.finditer(r.text):
        res_line,l = i.groups()
        
        #construct the quality 
        qualities.append(str(res_regex.search(res_line).group(1))+"p")
        
        #construct link
        links.append(partial_link+l.strip())
    
    return qualities,links

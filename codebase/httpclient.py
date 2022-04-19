import httpx

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"

#create a httpclient class
class HttpClient:
    def __init__(self,headers=user_agent):
        self.session = httpx.Client(headers={'User-Agent':user_agent})
    
    def get(self,url,headers={}):
        return self.session.get(url,headers=headers)
    
    def post(self,url,data,headers={}):
        return self.session.post(url,data=data,headers=headers)
    

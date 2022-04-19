from .httpclient import HttpClient
from bs4 import BeautifulSoup as bs


req = HttpClient()

#some global shit
main_url = "https://9anime.se"

def search_anime(query):
    '''
    function to search anime
    '''
    query = query.replace(" ","+")
    search_url = f"{main_url}/search?keyword={query}"
    r=req.get(search_url)
    soup = bs(r.text,"html.parser")
    
    #anime id
    anime_id = [i["href"].split("-")[-1] for i in soup.select(".dynamic-name")]
    
    #anime name
    anime_name = [ i["data-jname"] for i in soup.select(".dynamic-name")]
    
    
    return anime_id,anime_name


def episode_id(anime_id):
    '''
    function to return episode ids
    '''
    url = f"https://9anime.se/ajax/episode/list/{anime_id}"
    r=req.get(url,headers={"X-Requested-With":"XMLHttpRequest"})
    soup = bs(r.json().get("html"),"html.parser")
    
    e_ids = [i["data-id"] for i in soup.select(".ep-item")]
    return e_ids
    
    
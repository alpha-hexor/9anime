from termcolor import colored
import random
import sys
import os
from codebase.search import *
from codebase.link_gen import *
from codebase.httpclient import *

req = HttpClient()

#create download directory
if not os.path.exists('downloads'):
    os.mkdir('downloads')
    
#clear screen function
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

#write a function to print colored text
def colored_print(message):
    colors = ['red','green','blue','yellow','magenta','cyan']
    color = random.choice(colors)
    print(colored(message,color,attrs=["bold"]))

#funciton to ask subtitles
def ask_sub(subs):
    clear()
    colored_print("[*]Availabe subtitles:")
    for x , i in enumerate(subs):
        colored_print(f"[{x+1}] {i[0]}")
        
    choice = int(input("[*]Enter subtitle number: "))
    return subs[choice-1][1]

#function to ask quality
def ask_q(q):
    colored_print("[*]Available qualities:")
    for x , i in enumerate(q):
        colored_print(f"[{x+1}] {i[0]}")
    
    c= int(input("[*]Enter quality number: "))
    return q[c-1][1]
        
    
#function to stream episode
def stream_episode(name,e_id,ep_num,last_ep):
    clear()
    link = get_rapid_link(e_id)
    subs,q = get_final_links(link)
    
    s=ask_sub(subs)
    clear()
    colored_print(f"[*]Streaming {name}: episode :{ep_num}")
    link = ask_q(q)
    
    os.system(f'mpv --sub-file="{s}" "{link}"' if len(s)>0 else f'mpv "{link}"' )
    
    if (int(ep_num) + 1 <= int(last_ep)):
        opt = input(("[*]Want to start next episode[y/n]: "))
        
        if (opt == "n"):
            sys.exit()
            
        ep_id = int(e_id) + 1
        ep_num = int(ep_num) + 1
        
        stream_episode(name,str(ep_id),str(ep_num),last_ep)
    
#function to download episode
def download_episode(path,name,e_id,ep_num,last_ep):
    clear()
    link = get_rapid_link(e_id)
    subs,q = get_final_links(link)
    
    s=ask_sub(subs)
    clear()
    colored_print(f"[*]Downloading {name}: episode :{ep_num}")
    link = ask_q(q)
    
    os.system(f'ffmpeg -loglevel error -stats -i "{link}" -c copy "{path}/{name}.mp4"')
    
    colored_print("[*]Downloading subtitles")
    r=req.get(s)
    with open(f'{path}/{name}.srt', 'wb') as f:
        f.write(r.content)
    f.close()

    if (int(ep_num) + 1 <= int(last_ep)):
        opt = input(("[*]Want to start next episode[y/n]: "))
        
        if (opt == "n"):
            sys.exit()
            
        ep_id = int(e_id) + 1
        ep_num = int(ep_num) + 1
        
        download_episode(path,name,str(ep_id),str(ep_num),last_ep)
        
    
 
def main():
    query = input("[*]Enter anime name: ")
    anime_id,anime_name =search_anime(query)
    
    for x ,i in enumerate(anime_name):
        colored_print(f"[{x+1}] {i}")
        
    choice = int(input("[*]Enter anime number: "))
    anime_to_watch = anime_id[choice-1]
    e_ids = episode_id(anime_to_watch)
    colored_print(f"[*]Available episodes [{len(e_ids)}]")
    ep_num = int(input("[*]Enter episdoe number: "))
    
    if int(ep_num) <= len(e_ids):
        e_id = e_ids[ep_num-1]
        colored_print('[S]tream Episode')
        colored_print('[D]ownload Episode')
        x = input("[*]Enter your choice: ")
        
        if x == 'd' or x == 'D':
            path = "downloads\\" + anime_name[choice-1].replace(" ","_")
            if not os.path.exists(path):
                os.makedirs(path)
            download_episode(path,anime_name[choice-1],e_id,ep_num,len(e_ids))
            
        else:
            stream_episode(anime_name[choice-1],e_id,ep_num,len(e_ids))    
        
    
    
main()

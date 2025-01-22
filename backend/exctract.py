import re

def extrack_session_id(text):
    id_s=re.search('sessions\/(.+)\/contexts',text).group(1)
    
    return id_s
    

def dict_to_string(dic:dict):
    s=""
    c=1
    for k,v in dic.items():
        if(c):s+=f'{v} {k}'
        else :s+=f'and {v} {k}'
        c=0
    return s


def list_to_str(lis):
    s=''
    c=1
    for v in lis:
        if c:
            s+=f'{v}'
        else: s+=f'and {v}'
        c=0
    return s
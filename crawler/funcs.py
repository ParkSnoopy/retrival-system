import os

from sty import fg
from options import (
    NAME, 
    INCLUDES, 
    MIN_MSG_LEN, 
    SAVE_FTYPE,
    ENCODING, 
)



def _print(rgb, msg, end="\n", _fill=True):
    print( color(rgb, msg)+( (" "*(MIN_MSG_LEN-len(msg))) if _fill else "" ) , end=end)
    
def color(rgb, msg, _tail=True):
    if _tail:
        return fg(*rgb) + msg + fg.rs
    return fg(*rgb) + msg

def color_by_status(msg, status, _tail=True):
    colormap = {
        0: (255,100,100), 
        1: (255,255,100), 
        2: (100,255,100), 
        3: (100,255,255), 
    }
    if _tail:
        return fg(*colormap[status]) + msg + fg.rs
    return fg(*colormap[status]) + msg

def windows_valid(filename:str, force_return:str=None, _return_NAME=True) -> str:
    if NAME and _return_NAME:
        return NAME
    filename = filename.replace('https', '')
    filename = filename.replace('http', '')
    for char in '/\\:*?"<>|':
        filename = filename.replace(char, '.')
    for include in INCLUDES:
        filename = filename.replace(include, '')
    filename = filename.strip('.').strip()[:80]
    return filename

def concat_all_urls(path, _export=True):
    # path ex) './out/spss mediation'
    memory = set()
    filenames = ( filename for filename in os.listdir(path) if ( filename.endswith(SAVE_FTYPE) and filename != 'urls'+SAVE_FTYPE ) )
    for filename in filenames:
        # print(f"Concat {filename}")
        memory.update( url.strip('\n') for url in open( os.path.join(path, filename), 'r', encoding=ENCODING ) )
    # print(f"  {memory=}")
    if not _export:
        return memory
    with open( os.path.join(path, 'urls'+SAVE_FTYPE), 'w', encoding=ENCODING ) as file:
        file.write(
            '\n'.join(memory)
        )

































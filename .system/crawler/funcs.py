import os

from sty import fg

from options import (
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
        2: (100,255,255), 
        3: (100,255,100), 
    }
    if _tail:
        return fg(*colormap[status]) + msg + fg.rs
    return fg(*colormap[status]) + msg

def windows_valid(filename:str, force_return:str=None) -> str:
    filename = filename.replace('https', '')
    filename = filename.replace('http', '')
    for char in '/\\:*?"<>|':
        filename = filename.replace(char, '.')
    for include, and_or in INCLUDES.items():
        filename = filename.replace(include, '')
    filename = filename.strip('.').strip()[:80]
    return filename

def output_path(rooturl:str, currurl:str, root_dir:str) -> str:
    rooturl = ".".join(rooturl.split(".")[-2:])
    if rooturl in currurl:
        target_dir = currurl.split(rooturl)[-1].split("?")[0]
        
        target_dir = target_dir.split('/')
        path, filename = root_dir + '/'.join(target_dir[:2]), '.'.join(target_dir[2:])
        
        if not os.path.exists( path ):
            try:
                os.mkdir( root_dir + '/' + target_dir[0] )
            except FileExistsError:
                pass
            try:
                os.mkdir( path )
            except FileExistsError:
                pass
        
        if filename.endswith('.html'):
            filename = filename[:-5] + SAVE_FTYPE
        else:
            raise ValueError()
        
        if os.path.exists( path + '/' + filename ):
            raise ValueError()
        
        return path + '/' + filename
    
    raise ValueError("currurl not child of rooturl")

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

def drop_duplicates(filepath) -> int:
    memory = set()
    memory.update( url.strip('\n') for url in open( filepath, 'r', encoding=ENCODING ) )
    with open( filepath, 'w', encoding=ENCODING ) as file:
        file.write(
            '\n'.join(memory)
        )
    return len(memory)






























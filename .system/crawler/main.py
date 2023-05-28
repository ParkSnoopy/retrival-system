# -*- coding: utf-8 -*-
"""
Created on Sun May 28 17:42:24 2023

@author: sunwo
"""

from manager import Manager

from options import (
    URL_FILE, 
    TARGET_DEPTH, 
    WORKERS, 
    BROWSERLESS, 
)
from funcs import _print



if __name__ == '__main__':
    
    manager = Manager(
        max_workers=WORKERS, 
        browserless=BROWSERLESS, 
    )
    
    try:
        manager.set_initial_task(URL_FILE, target_depth=TARGET_DEPTH)
        manager.run()
        
    except KeyboardInterrupt:
        _print((200,50,50), "\n\n  System    :: Keyboard Interrupted\n")
        manager.done()
    
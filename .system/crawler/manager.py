# -*- coding: utf-8 -*-
"""
Created on Thu May 11 15:18:54 2023

@author: admin
"""

from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.webdriver import WebDriver

from threading import Thread
from time import sleep

import os; os.system("")

from options import (
    URL_FILE, 
    SAVE_FTYPE, 
    SAVE_TO, 
    ENCODING, 
    WORK_REST_IN_SEC, 
)

from worker import Worker
from funcs import windows_valid, _print, color_by_status, color, concat_all_urls



class Manager:
    
    def __init__(self, max_workers, browserless):
        self.max_workers = max_workers
        self.browserless = browserless
        
        self.workers = []
        self.threads = []
        
        self._init_options()
        self._ready_workers()
        
        self.tasks_file = None
        self.output_file = None
    
    def _init_options(self):
        self.chromeoptions = ChromeOptions()
        if self.browserless:
            self.chromeoptions.add_argument("--no-sandbox")
            self.chromeoptions.add_argument("--headless")
            self.chromeoptions.add_argument("--log-level=1")
    
    def _ready_workers(self):
        for _ in range(self.max_workers):
            self.workers.append(
                Worker(
                    manager=self, 
                    pk=1+len(self.workers), 
                    options=self.chromeoptions, 
                )
            )
    
    def _ready_threads(self):
        for i, worker in enumerate(self.workers):
            _print((100, 100, 100), f"  Thread {i+1:02d} ready")
            self.threads.append(
                Thread(
                    target=worker.work, 
                    args=(), 
                )
            )
    
    def _start_threads(self):
        for i, thread in enumerate(self.threads):
            _print((200, 200,   0), f"  Thread {i+1:02d} is now online!")
            thread.start()
    
    @staticmethod
    def mkdir(path):
        try:
            os.mkdir(path)
        except FileExistsError:
            pass
    
    def set_initial_task(self, url, target_depth):
        
        self.path = SAVE_TO
        
        self.mkdir(SAVE_TO)
        self.mkdir(self.path)
        self.mkdir(self.path+"/endpoint")
        
        self.tasks_len = sum( 1 for _ in open( URL_FILE, 'r', encoding=ENCODING ) )
        self.tasks_file = open( URL_FILE, 'r', encoding=ENCODING )
        
        self.target_depth = target_depth
        self.dones_len = 0
        self.results_len = 0
        self.idle = True
    
    def get_url(self) -> (bool, str):
        print("", end="\r")
        if not self.tasks_file.closed:
            url = self.tasks_file.readline().strip('\n')
            if url:
                self.dones_len += 1
                return True, url
        return False, ""
    
    def update(self, results:list[str]):
        if results:
            self.output_file.write("\n".join(results))
            self.output_file.write("\n")
        self.results_len += len(results)
    
    def save(self, results:list[WebDriver], from_url):
        if results:
            filename = self.path+'/endpoint/'+windows_valid(from_url, _return_NAME=False)+SAVE_FTYPE
            with open( filename, 'w', encoding=ENCODING ) as output_file:
                output_file.write(" >> FROM >> " + from_url + "\n\n\n\n")
                for result in results:
                    if result.text.strip():
                        output_file.write(result.text)
                        output_file.write("\n")
        self.results_len += len(results)
    
    def ready_next_run(self):        
        _print((100, 100, 250), "\n  Manager   :: All current task done!\n")
        _print((150, 150, 150), "  Manager   :: Continue to next tasks...")
        if self.tasks_file: self.tasks_file.close()
        self.tasks_file = open( self.path+f'/{self.curr_depth}'+SAVE_FTYPE, 'r', encoding=ENCODING )
        self.tasks_len = self.results_len
        self.dones_len = 0
        self.results_len = 0
    
    def should_work(self):
        return ( not self.idle ) or self.crawling
    
    def check_working_status(self):
        i = 0
        worker_has_task = True
        while worker_has_task or not self.results_len:
            i += 1;
            if not i % 4: i -= 4; 
            
            sleep(WORK_REST_IN_SEC)
            
            worker_task_status = tuple( worker.status() for worker in self.workers )
            status_str = "|".join( color_by_status(f" {worker.pk:02d} ", worker_task_status[i], _tail=True) for i, worker in enumerate(self.workers) )
            _print((64, 192, 64), f"  Manager   :: Depth {self.curr_depth} :: Task allocated {self.dones_len} out of {self.tasks_len} :: Worker status {status_str} "+color((0, 255, 0), f":: Found {self.results_len}", _tail=False)+" "+("."*(i))+"   ", end='\r', _fill=False)
            
            worker_has_task = any( worker_task_status )
        
        while not all( worker.is_idle() for worker in self.workers ):
            sleep(WORK_REST_IN_SEC)
        
    def crawl_for_urls(self):
        self.crawling = False
       
        if self.target_depth <= 0:
            self.target_depth = 1
        
        for self.curr_depth in range(1, 1+self.target_depth):
            if self.output_file: self.output_file.close()
            self.output_file = open( self.path+f'/{self.curr_depth}'+SAVE_FTYPE, 'w', encoding=ENCODING )
            self.check_working_status()
            self.ready_next_run()
        
        self.tasks_file.close()
        self.output_file.close()
        _print((152,251,152), "  Manager   :: Concatenate all urls into single file...")
        concat_all_urls(self.path)
    
    def crawl_for_contents(self):
        self.crawling = True
        _print((100, 255, 255), "\n  Manager   :: Start Crawling...")
        
        _print((152,251,152), "\n  Manager   :: Loading concatenated file as tasks file...", end="\n\n")
        
        filepath = os.path.join( self.path, 'urls'+SAVE_FTYPE )
        
        self.tasks_len = sum( 1 for _ in open( filepath, 'r', encoding=ENCODING ) )
        self.tasks_file = open( filepath, 'r', encoding=ENCODING )
        
        self.check_working_status()
    
    def run(self):
        self.idle = False
        self.crawling = False
        
        self._ready_threads()
        self._start_threads()
        
        self.crawl_for_urls()
        
        self.output_file = open( self.path+'/endpoint/.ignore', 'w', encoding=ENCODING )
        
        self.crawl_for_contents()
        
        self.done()
        
    def done(self):
        _print((100,100,255), "\n\n  Manager   :: All done!", end="\n")
        self.idle = True
        self.crawling = False
        
        while self.threads:
            self.threads.pop().join()
        _print((255,255,  0), "  Manager   :: Released working threads...")
        
        _print((100,100,255), "  Manager   :: Closing task file...")
        try: self.tasks_file.close()
        except: pass
        _print((100,100,255), "  Manager   :: Saving output file...")
        try: self.output_file.close()
        except: pass
        _print((100,100,255), "  Manager   :: All file operations done!")
        





    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import Service, WebDriver
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from urllib3.exceptions import ProtocolError, MaxRetryError

from time import sleep

from options import (
    EXCLUDES, 
    INCLUDES, 
    MAIN_RESULT_CONTAINER, 
    StaleElemRefExc_MAX_ATTEMPT, 
    SAVE_TARGET, 
    WORK_REST_IN_SEC, 
    CHROMEDRIVER_PATH, 
    LOADING_TIMEOUT_IN_SEC, 
    IMPLICITLY_WAIT_IN_SEC, 
    SHOW_URL_LEN, 
)

from funcs import _print

from typing import Optional



chrome_service = Service(executable_path=CHROMEDRIVER_PATH, )

class Worker:
    def __init__(self, manager, pk, options):
        self.manager = manager
        self.pk = pk
        
        self._init_driver(options)
        
        self.idle = True
        self.loaded = False
        self.has_task = False
        self.uploading = False
        
    def _init_driver(self, options):
        self.driver = Chrome(options=options, service=chrome_service)
        self.driver.set_page_load_timeout(LOADING_TIMEOUT_IN_SEC)
        self.driver.implicitly_wait(IMPLICITLY_WAIT_IN_SEC)
        
    def is_idle(self):
        return self.idle
    def is_loaded(self):
        return self.loaded
    def does_have_task(self):
        return self.has_task
    
    def status(self):
        if not self.has_task:
            return 0
        if not self.loaded:
            return 1
        if not self.uploading:
            return 2
        # if self.has_task and self.loaded and self.uploading:
        return 3
    
    def request(self, url):
        self.idle = False
        self.loaded = False
        
        try:
            self.driver.get(url)
        
        except TimeoutException:
            _print((255, 100, 100), f"  Worker {self.pk:02d} :: Request to '{url}' has reached timeout. Discard url.")
            return False
        
        except WebDriverException:
            _print((255, 100, 100), f"  Worker {self.pk:02d} :: Could not resolve DNS name of '{url}'")
            return False
        
        self.loaded = True
        return True
        
    def done(self):
        self.idle = True
        self.loaded = False
        self.has_task = False
        self.uploading = False
        
    def upload_urls(self):
        results: list[str] = self.get_cleaned_urls()
        self.uploading = True
        self.manager.update(results)
        
    def upload_contents(self, from_url):
        results: list[WebDriver] = self.get_cleaned_contents()
        self.uploading = True
        self.manager.save(results, from_url)
        
    def upload(self, from_url):
        if not self.manager.crawling:
            self.upload_urls()
        else:
            self.upload_contents(from_url)
    
    @staticmethod
    def _filter_element(element) -> bool:
        href = element.get_attribute('href')
        if not href:
            return False
        if any( ( exclude in href ) for exclude in EXCLUDES ):
            return False
        if not all( ( include in href ) for include in INCLUDES ):
            return False
        return True
    
    def get_cleaned_urls(self) -> list:
        container_id: Optional[str] = MAIN_RESULT_CONTAINER
        
        for i in range(StaleElemRefExc_MAX_ATTEMPT):
            try:
                if container_id:
                    try:
                        results_container = WebDriverWait( self.driver, timeout=IMPLICITLY_WAIT_IN_SEC ) \
                            .until(
                                EC.visibility_of_element_located(
                                    ( By.ID, container_id )
                                )
                            )
                    except TimeoutException:
                        _print((255,100,100), f"  Worker {self.pk:02d} :: Timeout :: Element not located, return body element. ")
                        results_container = self.driver
                else:
                    results_container = self.driver
                
                deeper_links = [
                    element.get_attribute('href')
                    for element in results_container.find_elements(By.TAG_NAME, 'a')
                    if self._filter_element( element )
                ]
                return deeper_links
            
            except StaleElementReferenceException:
                _print((150, 150,   0), f"  Worker {self.pk:02d} :: StaleElementReferenceException. Attempt {i+1}...")
                continue
        
        _print((200,  50,  50), f"  Worker {self.pk:02d} :: StaleElemRef fail attempt maxed. Discard current URL.  // ")
        return []
    
    def get_cleaned_contents(self) -> list[WebDriver]:
        for i in range(StaleElemRefExc_MAX_ATTEMPT):
            try:
                try:
                    
                    _: WebDriver = WebDriverWait( self.driver, timeout=IMPLICITLY_WAIT_IN_SEC ) \
                       .until( 
                           EC.visibility_of_element_located(
                               ( SAVE_TARGET['by'], SAVE_TARGET['value'] )
                           )
                       )
                    results = self.driver.find_elements( SAVE_TARGET['by'], SAVE_TARGET['value'] )
                except TimeoutException:
                    _print((255,100,100), f"  Worker {self.pk:02d} :: Timeout :: Element not located, return body element. ")
                    results = self.driver.find_elements( By.TAG_NAME, 'body' )
                
                return results
            
            except StaleElementReferenceException:
                _print((150, 150,   0), f"  Worker {self.pk:02d} :: StaleElementReferenceException. Attempt {i+1}...")
                continue
        
        _print((200,  50,  50), f"  Worker {self.pk:02d} :: StaleElemRef fail attempt maxed. Discard current URL.  // ")
        return []
    
    def get_url(self):
        try:
            return self.manager.get_url()
        except ValueError:
            sleep(WORK_REST_IN_SEC)
    
    def work(self):
        try:
            while self.manager.should_work():
                sleep(WORK_REST_IN_SEC)
                
                got, url = self.get_url()
                if got:
                    self.has_task = True
                    if len(url) < SHOW_URL_LEN: 
                        _print((  0, 200, 150), f"  Worker {self.pk:02d} :: request '{url}'")
                    else:
                        _print((  0, 200, 150), f"  Worker {self.pk:02d} :: request '{url[:SHOW_URL_LEN]} ", end="", _fill=False)
                        _print((  0, 250, 100), "...(more)...", end="", _fill=False)
                        _print((  0, 200, 150), "'", _fill=False)
                    
                    if self.request(url):
                        self.upload(from_url=url)
                    
                    self.done()
                
                else:
                    # print(f"  Worker {self.pk:02d} :: err::url_fetch_from_manager_failed")
                    self.has_task = False
                
        except ProtocolError:
            _print((255,100,100), f"  Worker {self.pk:02d} :: ProtocolError :: Network connection forcibly closed!")
        
        except MaxRetryError:
            _print((255,100,100), f"  Worker {self.pk:02d} :: MaxRetryError :: Browser is closed!")



























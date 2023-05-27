from selenium.webdriver.common.by import By
import tomli

with open("./options.toml", "rb") as toml:
    options = tomli.load(toml)

URL_FILE = options['main_config']['user']['target']['file']

NAME = options['main_config']['user']['save_to_filename']

BROWSERLESS = options['main_config']['admin']['browserless']

LOADING_TIMEOUT_IN_SEC = options['worker_setting']['loading_timeout_in_sec']
IMPLICITLY_WAIT_IN_SEC = options['worker_setting']['implicitly_wait_in_sec']

CHROMEDRIVER_PATH = options['universal']['chromedriver_path']

TARGET_DEPTH = options['main_config']['admin']['target_depth']

WORKERS = options['worker_setting']['workers']
WORK_REST_IN_SEC = options['universal']['working_tick'] / 1000

MIN_MSG_LEN = options['universal']['base_min_msg_len'] + (4*WORKERS)
SHOW_URL_LEN = options['universal']['max_show_url_len'] + (3*WORKERS)

MAIN_RESULT_CONTAINER = options['main_config']['user']['main_container']

EXCLUDES = options['main_config']['user']['excludes']
INCLUDES = options['main_config']['user']['includes']

SAVE_TARGET = {
    'by': By.TAG_NAME,  # FIXED as TAG_NAME for security reason
    'value': options['main_config']['admin']['endpoint_save_target']['value'], 
}

SAVE_TO = options['main_config']['admin']['save_to']
SAVE_FTYPE = options['main_config']['admin']['save_filetype']
ENCODING = options['main_config']['admin']['save_encoding']

StaleElemRefExc_MAX_ATTEMPT = options['worker_setting']['slateelem_max_attempt']

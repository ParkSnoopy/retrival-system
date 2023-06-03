# -*- coding: utf-8 -*-

# gunicorn.conf.py



# Access log - records incoming HTTP requests
accesslog = "/var/log/gunicorn.access.log"

# Error log - records Gunicorn server goings-on
errorlog = "/var/log/gunicorn.error.log"

# Whether to send Django output to the error log 
capture_output = True

# How verbose the Gunicorn error logs should be 
loglevel = "debug"



# Connection timeout limit ( max 300 )
timeout = 60
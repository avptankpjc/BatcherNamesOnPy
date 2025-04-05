
import logging
from logging.handlers import RotatingFileHandler
import os


log_folder = "logs"

if not os.path.exists(log_folder):
    os.makedirs(log_folder) 
    
log_path = os.path.join(log_folder, "regis.log")


#Config Handler Rotative
log_handler = RotatingFileHandler(
    log_path,
    maxBytes=1_000_000, #1MB
    backupCount=3
)

formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s"
)

log_handler.setFormatter(formatter)


#Create the Log

logger = logging.getLogger("BatcherNameLogger")
logger.setLevel(logging.DEBUG)
logger.addHandler(log_handler)


###Optional set logs in console####
#console_handler = logging.StreamHandler()
#console_handler.setFormatter(formatter)
#logger.addHandler(console_handler)









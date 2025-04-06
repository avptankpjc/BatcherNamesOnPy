
import logging
from logging.handlers import RotatingFileHandler
import os
from pathlib import Path


user_docs = str(Path(os.getenv('USERPROFILE')) / "Documents")
log_folder = os.path.join(user_docs, "BatcherNameOnPy", "logs")


#Create the Directory
try:
    os.makedirs(log_folder, exist_ok=True)
    
except PermissionError:
    print(f"Permission denied to create the log directory at {log_folder}")
    log_folder = user_docs
    os.makedirs(log_folder, exist_ok=True)
    

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









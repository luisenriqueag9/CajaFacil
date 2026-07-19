import logging
import sys
from app.core.config import settings

def setup_logger(name: str = "caja_facil") -> logging.Logger:
    """
    Configures and returns a standardized logger for the CajaFácil application.
    """
    logger = logging.getLogger(name)
    
    # Avoid duplicate handlers if already setup
    if logger.handlers:
        return logger
        
    logger.setLevel(settings.LOG_LEVEL.upper())
    
    # Stream Handler for console logs
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(settings.LOG_LEVEL.upper())
    
    # Clean structured console format
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s] [%(filename)s:%(lineno)d]: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Disable propagation to avoid duplication with root loggers if needed
    logger.propagate = False
    
    return logger

# Global application logger
logger = setup_logger()

import logging

SOCKET_VERSION = '230613'

# List for files:
SOCKET_SERVER_LOGS = 'logs/socket_server.log'
#SOCKET_SERVER_LOGS = '/dev/fd/1' #Debug
#SOCKET_SERVER_LOGS = '/dev/fd/2' #Error (Modificar el level en el setup_logger)

# Logging
log_format = logging.Formatter('%(asctime)-15s: %(name)s - %(levelname)s - %(message)s')
logging.basicConfig()
def setup_logger(name, log_file, level=logging.DEBUG):
    logger = logging.getLogger(name)
    """To setup as many loggers as you want"""

    handler = logging.FileHandler(log_file)        
    handler.setFormatter(log_format)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

logging = setup_logger('SocketServer', SOCKET_SERVER_LOGS)

# Socket listener
HOST = '0.0.0.0'
PORT = 11022

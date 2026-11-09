import logging
from logging.handlers import RotatingFileHandler,TimedRotatingFileHandler

if __name__ =='__main__':
    print('log levels :')
    print(f'DEBUG:{logging.DEBUG}')
    print(f'INFO:{logging.INFO}')
    print(f'WARN:{logging.WARN}')
    print(f'ERROR:{logging.ERROR}')
    print(f'CRITCAL:{logging.CRITICAL}')
    print(f'Default level:{logging.getLevelName(logging.getLogger().level)}')
    print(f'DEfault logger:{logging.getLogger()}')
    logger: logger=logging.getLogger(__name__)
    logger.setLevel(logging.WARNING)
    """logging.basicConfig(
        filename='confing.log',
        format='%(asctime)s|%(name)s|%(levelname)s|%(message)s',
        datefmt='%d-%m-%y %H:%H:%M:%S'
    )"""
    logger_formatter=logging.Formatter(
    fmt='%(asctime)s|%(name)s|%(levelname)s|%(message)s', 
    datefmt='%d-%m-%Y %H:%M:%S'
     )

    #console=logging.StreamHandler
    """file_rotate=RotatingFileHandler(
        filename='rotate size.log',
        maxBytes=100,
        backupCount=7
    )"""

    file_rotate=TimedRotatingFileHandler(
        filename='time_log.log',
        when='s',
        interval=10,
        backupCount=10
    )
    #file_logs=logging.FileHandler('app.log')
    #file_logs.setFormatter(logger_formatter)
    console=logging.StreamHandler()
    console.setFormatter(logger_formatter)
    #logging.error('Root MSG')
    logger.addHandler(file_rotate)

    logger.info('INFO Message')
    logger.warning('INFO Message')
    logger.error('Error Message')


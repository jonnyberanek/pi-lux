import logging
VERBOSE = 5

FORMAT = '%(asctime)s %(levelname)-7s %(name)-16s %(message)s'

root_logger = logging.getLogger()
get_logger = logging.getLogger

def init_logging(level=VERBOSE):
  handler = logging.StreamHandler()
  handler.setFormatter(logging.Formatter(FORMAT))
  
  if level >= logging.DEBUG:
    handler.addFilter(filter_ws) 
  
  logging.basicConfig(level=level, format=FORMAT, handlers=[handler])

class MyFilter(logging.Filter):
  def filter(self, record):
      return record.levelname in ('WARNING', 'ERROR', 'CRITICAL')

def filter_ws(record: logging.LogRecord) -> bool:
  return not record.name.startswith('websockets') or record.levelno > logging.DEBUG or 'bytes' in record.getMessage() 

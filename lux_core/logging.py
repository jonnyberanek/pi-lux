import logging
VERBOSE = 5

FORMAT = '%(asctime)s %(levelname)-7s %(name)-16s %(message)s'

root_logger = logging.getLogger()
get_logger = logging.getLogger

def init_logging(level=VERBOSE):
  logging.addLevelName(VERBOSE, "VERBOSE")
  logging.basicConfig(level=level, format=FORMAT)

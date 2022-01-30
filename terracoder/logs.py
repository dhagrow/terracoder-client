import sys
from logging import *

import colorlog

LOG_COLORS = {
    'DEBUG'   : 'reset',
    'INFO'    : 'white',
    'WARNING' : 'yellow',
    'ERROR'   : 'red',
    'CRITICAL': 'bold_red,bg_black',
    }

get = getLogger
log = get(__name__)

def init(debug_level=0, log_exceptions=True):
    """Initializes simple logging defaults."""
    root_log = get()

    # init only once
    if root_log.handlers: return

    fmt = '%(levelname).1s %(asctime)s . %(message)s'
    formatter = colorlog.ColoredFormatter('%(log_color)s' + fmt,
        log_colors=LOG_COLORS)

    handler = StreamHandler()
    handler.setFormatter(formatter)

    root_log.addHandler(handler)
    root_log.setLevel(DEBUG if debug_level > 0 else INFO)

    get('charset_normalizer').setLevel(WARNING)

    if log_exceptions:
        sys.excepthook = handle_exception

def handle_exception(etype, evalue, etb):
    if issubclass(etype, KeyboardInterrupt):
        sys.__excepthook__(etype, evalue, etb)
        return
    log.error('unhandled exception', exc_info=(etype, evalue, etb))

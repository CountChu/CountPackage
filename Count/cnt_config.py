#
# FILENAME.
#       cnt_config.py - Count Config Python Module.
#
# FUNCTIONAL DESCRIPTION.
#       The module provides functions to access config files.
#
# NOTICE.
#       Author: visualge@gmail.com (CountChu)
#       Created on 2024/10/11
#       Updated on 2024/10/11
#

import sys
import os 
import yaml
from pathlib import Path

br = breakpoint

class Config:
    def __init__(self, d):
        self._d = d
        for key, value in d.items():
            setattr(self, key, value)

    def __str__(self):
        return '%s' % self._d

def load_app_config(fn):
    config_p = Path(fn) 
    if config_p.parent == Path('.'):
        app_p = Path(os.path.abspath(sys.argv[0])).parent 
        config_p = app_p / fn 

    cfg = load(config_p)
    return cfg
 
def load(fn, default=None):
    if os.path.exists(fn):
        f = open(fn, 'r', encoding='utf-8')
        out = yaml.load(f, Loader=yaml.CLoader)
        f.close()

    else:
        assert default != None
        out = default

    out['__dir__'] = os.path.dirname(fn)

    return out         

def save(data, fn):
    print(f'Saving {fn}')
    
    f = open(fn, 'w', encoding='utf-8')
    yaml.dump(data, f, default_flow_style=False, encoding='utf-8', allow_unicode=True)
    f.close()
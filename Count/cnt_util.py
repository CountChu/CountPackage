#
# FILENAME.
#       cnt_util.py - Count Utility Python Module.
#
# FUNCTIONAL DESCRIPTION.
#       The module provides utility functions of Count.
#
# NOTICE.
#       Author: visualge@gmail.com (CountChu)
#       Created on 2024/4/9
#       Updated on 2024/4/30
#

import sys
import os
import yaml
import json
from datetime import datetime

import pdb
br = pdb.set_trace

class Config:
    def __init__(self, d):
        self._d = d
        for key, value in d.items():
            setattr(self, key, value)

    def __str__(self):
        return '%s' % self._d

def load_json(fn):
    f = open(fn, encoding='utf-8')
    out = json.load(f)
    f.close()

    return out

#
# ensure_ascii = True means generate ascii to express utf-8, e.g., "\u8c46\u8150\u65b0\u958b\u59cb"
#

def save_json(data, fn, ensure_ascii=False):
    f = open(fn, 'w', encoding='utf-8')
    json.dump(data, f, ensure_ascii=ensure_ascii, indent=4) 
    f.close()
 
def load_yaml(fn, default=None):
    if os.path.exists(fn):
        f = open(fn, 'r', encoding='utf-8')
        out = yaml.load(f, Loader=yaml.CLoader)
        f.close()

    else:
        assert default != None
        out = default

    out['__dir__'] = os.path.dirname(fn)

    return out         

def save_yaml(data, fn):
    print(f'Saving {fn}')
    
    f = open(fn, 'w', encoding='utf-8')
    yaml.dump(data, f, default_flow_style=False, encoding='utf-8', allow_unicode=True)
    f.close()


def get_today_str():
    today_str = datetime.today().strftime('%Y-%m-%d')
    return today_str    

def get_now_str():
    now = datetime.now()
    out = datetime.strftime(now, '%Y-%m-%d %H:%M:%S')
    return out

def get_time_str(ts):
    ts = ts // 1000
    ts_dt = datetime.fromtimestamp(ts)
    time_str = ts_dt.strftime("%Y-%m-%d %H:%M")
    return time_str

def get_time_str_2(ts):
    ts = ts // 1000
    ts_dt = datetime.fromtimestamp(ts)
    time_str = ts_dt.strftime("%Y-%m-%d %H:%M:%S")
    return time_str 

def check_file_exist(fn):
    if not os.path.exists(fn):
        print('Error. The file does not exist.')
        print(fn)
        sys.exit(1)

def check_dir_exist(dn):
    if not os.path.exists(dn):
        print('Error. The directory does not exist.')
        print(dn)
        sys.exit(1)  

def check_dir_exist_and_make(dn):
    if not os.path.exists(dn):
        print('Building %s' % dn)
        os.makedirs(dn)

def get_latest_file_time(root_dir):
    latest_time = 0
    latest_file = None

    file_path = root_dir 
    file_time = os.path.getmtime(file_path)

    if file_time > latest_time:
        latest_time = file_time
        latest_file = file_path    

    #print(root_dir)
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            file_time = os.path.getmtime(file_path)
            #print(file_path)
            #print(datetime.fromtimestamp(file_time).strftime('%Y-%m-%d %H:%M:%S'))

            if file_time > latest_time:
                latest_time = file_time
                latest_file = file_path

        for dirname in dirnames:
            file_path = os.path.join(dirpath, dirname)
            file_time = os.path.getmtime(file_path)

            if file_time > latest_time:
                latest_time = file_time
                latest_file = file_path            

    return latest_file, latest_time 

def fill_string_with_width(input_string, width, fill_char=' '):
    # Calculate the number of characters needed to fill the string
    fill_count = width - len(input_string.encode('gbk'))

    # Fill the string with the specified character
    filled_string = input_string + fill_char * fill_count

    return filled_string

def build_d(ls, id=None):
    out = {}

    if id == None:
        id_name = 'id'
    else:
        id_name = id

    for item in ls:
        assert item[id_name] not in out
        out[item[id_name]] = item

    return out

def join_d(d1, d2):
    out = {}
    for id1, item1 in d1.items():

        if not id1 in d2:
            continue

        #print('id1 = %s' % id1)
        out[id1] = d1[id1]
        for key, value in d2[id1].items():
            out[id1][key] = value

    return out

def read_column(d, name):
    out = []
    for key, value in d.items():
        out.append(value[name])

    return out

def read_column_from_ls(ls, name):
    out = []
    for item in ls:
        out.append(item[name])

    return out

def get_dn_ls(home):
    dn_ls = []
    bn_ls = []
    for bn in os.listdir(home):
        if bn == '.DS_Store':
            continue

        dn = os.path.join(home, bn)
        if not os.path.isdir(dn):
            continue

        dn_ls.append(dn)
        bn_ls.append(bn)

    return dn_ls, bn_ls


def get_latest_dn(home):

    dn_ls = []
    for bn in os.listdir(home):
        if bn == '.DS_Store':
            continue

        dn = os.path.join(home, bn)
        if os.path.isfile(dn):
            continue
        
        dn_ls.append(dn)

    dn_ls.sort()
    return dn_ls[-1]

def file_is_old(fn, mtime):
    assert os.path.exists(fn)

    fn_mtime = os.path.getmtime(fn)  
    out =  mtime > fn_mtime
    if out:
        print('The file [%s] is old.' % os.path.basename(fn))
        print('    Old: %s' % get_time_str(fn_mtime*1000))
        print('    New: %s' % get_time_str(mtime*1000))

    return out

#
# Check if fn1 need to be generated
#

def file_need_gen(fn1, fn2):
    assert os.path.exists(fn2)

    if not os.path.exists(fn1):
        print('The file [%s] will be generated.' % os.path.basename(fn1))
        return True

    fn1_mtime = os.path.getmtime(fn1)
    fn2_mtime = os.path.getmtime(fn2)
    out = fn1_mtime < fn2_mtime
    if out:
        print('The file [%s] is old.' % os.path.basename(fn1))
        print('    Old: %s' % get_time_str(fn1_mtime*1000))
        print('    New: %s @ %s' % (get_time_str(fn2_mtime*1000), os.path.basename(fn2)))

    return out

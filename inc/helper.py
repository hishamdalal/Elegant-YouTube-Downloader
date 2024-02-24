from pytube.exceptions import PytubeError
# from slugify import slugify
import ttkbootstrap as tb
from ttkbootstrap.toast import ToastNotification

import subprocess
from pathvalidate import sanitize_filename
from pathlib import Path
import traceback
import os

# import unicodedata
# import re

# def slugify(value, allow_unicode=True):
#     """
#     Taken from https://github.com/django/django/blob/master/django/utils/text.py
#     Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
#     dashes to single dashes. Remove characters that aren't alphanumerics,
#     underscores, or hyphens. Convert to lowercase. Also strip leading and
#     trailing whitespace, dashes, and underscores.
#     """
#     value = str(value)
#     if allow_unicode:
#         value = unicodedata.normalize('NFKC', value)
#     else:
#         value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
#     value = re.sub(r'[^\w\s-]', '', value.lower())
#     return re.sub(r'[-\s]+', '-', value).strip('-_?')


class AgeRestrictionError(PytubeError):
    def __init__(message):
        super().__init__(message)


class UnavailableError(PytubeError):
    def __init__(message):
        super().__init__(message)

def dump(obj, i=1):
    s = "-" * i
    i = i + 1
    for attr in dir(obj):
        print(f"{s} obj.%s = %r" % (attr, getattr(obj, attr)))
        # print(type(obj), type(object))
        if type(obj) is object:
            dump(obj, i)


# for more: https://stackoverflow.com/a/59672132/2269902
def slugify(filepath):
    filepath = str(filepath.replace('  ', ''))
    return sanitize_filename(filepath)



def is_valid_path(path, is_dir=False):
    # print('path:::', path, is_dir)
    if path:
        if is_dir and Path(path).is_dir():
            return True
        elif Path(path).is_file():
            return True
    else:
        return False


def show_error(e):
    # traceback.print_exc()
    file = traceback.extract_tb(e.__traceback__)[-1].filename
    line_number = traceback.extract_tb(e.__traceback__)[-1].lineno
    code = traceback.extract_tb(e.__traceback__)[-1].line
    col_no = traceback.extract_tb(e.__traceback__)[-1].colno
    func = traceback.extract_tb(e.__traceback__)[-1].name
    print(f"Exception occurred on {file}:{line_number}")
    print(f"Col Number: {col_no}")
    print(f"Code: {code}")
    print(f"Function: {func}")
    print(e)
    # dump(traceback.extract_tb(e.__traceback__)[-1])

#
# def cli_progress_bar(progress=0, total=100):
#     percent = 100 * (progress / float(total))
#     bar = '-' * int(percent) + '-' * (100 - int(percent))
#     print(f"\r{bar}| {percent:2f}%", end="\r")

def window_center(master, w, h):
    ws = master.winfo_screenwidth()
    hs = master.winfo_screenheight()
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    master.geometry('%dx%d+%d+%d' % (w, h, x, y))    
    master.position_center()
    
# ----------------------------------------------------------------------------
def toast_notify(title, message, color=tb.SUCCESS):
    ToastNotification(
        title=title,
        message=message,
        duration=4000,
        alert=True,
        bootstyle=color,
        position=(50, 100, "sw")
    ).show_toast()
# ----------------------------------------------------------------------------
# def get_parent_path(path):
#     parent = Path(path).resolve().parents[0]
#     print('parent', parent)
# # ----------------------------------------------------------------------------
# def get_dir_name(path):
#     without_extra_slash = os.path.normpath(path)
#     last_part = os.path.basename(without_extra_slash)
#     print('last_part', last_part)
#     return last_part

# ----------------------------------------------------------------------------
def close_process(window_title):
    cmd = f'TASKKILL /F /FI "WINDOWTITLE eq {window_title}" /IM explorer.exe"'
    subprocess.Popen(cmd)

# ----------------------------------------------------------------------------
def close_window(path, is_file=False):
    # parent_path = get_parent_path(path)
    # window_title = get_dir_name(parent_path)
    if is_file:
        window_title = path.split("/")[-2]
    else:
        window_title = path.split("/")[-1]
    # print('window_title:', window_title)
    close_process(window_title)
# ----------------------------------------------------------------------------
def explore_file(path):
    if os.path.isfile(path):
        close_window(path, True)
        cmd = f'explorer.exe /select,"%s"'
        path = os.path.realpath(path)
        subprocess.Popen(cmd % path)
    else:
        raise Exception(f"File '{path}' is not exist")
# ----------------------------------------------------------------------------
def explore_folder(path):
    cmd = f'explorer.exe "%s"'
    
    if os.path.isdir(path):
        close_window(path)
        path = os.path.realpath(path)
        subprocess.Popen(cmd % path)
    else:
        raise Exception(f"Directory '{path}' is not exist")

# path = self.config.get('MAIN', 'downloads_dir')
# ----------------------------------------------------------------------------
def bool(string):
    if string.lower() == 'true':
        return True
    
    return False
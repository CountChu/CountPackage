#
# FILENAME.
#       cnt_ft.py - Count UI Python Module.
#
# FUNCTIONAL DESCRIPTION.
#       The module provides functions of UI.
#
# NOTICE.
#       Author: visualge@gmail.com (CountChu)
#       Created on 2025/3/1
#       Updated on 2025/3/1
#

import ipywidgets as widgets

def build_dropdown(item_ls, description):
    # build a dropdown widget
    item_dropdown = widgets.Dropdown(
        options=item_ls,
        description=description,
    )

    return item_dropdown

def build_dropdown_1(item_d, description, sort=True):
    item_ls = list(item_d.keys())
    if sort:
        item_ls.sort()

    # build a dropdown widget
    item_dropdown = widgets.Dropdown(
        options=item_ls,
        description=description,
    )

    return item_dropdown, item_ls
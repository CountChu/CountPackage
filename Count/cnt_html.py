#
# FILENAME.
#       cnt_html.py - Count HTML Python Module.
#
# FUNCTIONAL DESCRIPTION.
#       The module provides functions to generate HTML content.
#
# NOTICE.
#       Author: visualge@gmail.com (CountChu)
#       Created on 2024/4/18
#       Updated on 2024/4/20
#

br = breakpoint

c_n = "#e0e0e0"  # normal color
c_r = "#ffcdd2"  # red color
c_g = "#dcedc8"  # green color
c_y = "#fff59d"  # yellow color
c_b = "#bbdefb"  # blue color

c_rh = "#e57373"  # red highlight color
c_gh = "#aed581"  # green highlight color
c_yh = "#ffeb3b"  # yellow highlight color
c_bh = "#64b5f6"  # blue highlight color

b_c_n = f'style="background-color: {c_n};"'
b_c_r = f'style="background-color: {c_r};"'
b_c_g = f'style="background-color: {c_g};"'
b_c_y = f'style="background-color: {c_y};"'
b_c_b = f'style="background-color: {c_b};"'

b_c_rh = f'style="background-color: {c_rh};"'
b_c_gh = f'style="background-color: {c_gh};"'
b_c_yh = f'style="background-color: {c_yh};"'
b_c_bh = f'style="background-color: {c_bh};"'


def meta():
    t = ""
    t += '<meta charset="utf-8"/>\n'
    return t


def style():
    out = """
<style>
td {
    font-family: monospace;
    font-size:  14;
    text-align: right;
    vertical-align: top;
    padding: 4;  
}
table {
    border-spacing: 0;
}
</style>
    """

    return out


def table(heads, names, rows, ctx=None, f=None, fc=None, fh=None):
    t = ""

    t += '<table border="1">\n'
    t += "    <thead>\n"
    t += '        <tr style="text-align: right;">\n'
    if fh == None:
        for head in heads:
            t += "            <th>%s</th>\n" % head
    else:
        for head in heads:
            text = fh(head)
            t += "            <th>%s</th>\n" % text
    t += "        </tr>\n"
    t += "    </thead>\n"

    t += "    <tbody>\n"
    for row in rows:
        t += "        <tr>\n"
        for name in names:
            if name in row:
                value = row[name]
            else:
                value = ""

            text = value
            if f != None:
                text = f(name, value, row, ctx)

            color = ""
            if fc != None:
                color = fc(name, value, text, row, ctx)

            t += "            <td %s>%s</td>\n" % (color, text)
        t += "        </tr>\n"
    t += "    </tbody>\n"
    t += "</table>\n"

    return t

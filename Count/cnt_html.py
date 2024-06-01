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

c_r = 'style="background-color: #ffcdd2;"'    # red color
c_rh = 'style="background-color: #e57373;"'

c_n = 'style="background-color: #e0e0e0;"'    # normal color

c_g = 'style="background-color: #dcedc8;"'    # green color
c_gh = 'style="background-color: #aed581;"'

def meta():
    t = ''
    t += '<meta charset="utf-8"/>\n'
    return t

def style():
    out = '''
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
    ''' 

    return out

def table(heads, names, rows, f=None, fc=None, fh=None):
    t =     ''

    t +=         '<table border="1">\n'
    t +=         '  <thead>\n'
    t +=         '    <tr style="text-align: right;">\n'
    if fh == None:
        for head in heads:
            t += '      <th>%s</th>\n' % head
    else:
        for head in heads:
            text = fh(head)
            t += '      <th>%s</th>\n' % text
    t +=         '    </tr>\n'       
    t +=         '  </thead>\n'    

    t +=         '  <tbody>\n'
    for row in rows:
        t +=     '    <tr>\n'
        for name in names:
            value = row[name]

            text = value
            if f != None:
                text = f(name, value, row)

            color = ''
            if fc != None:
                color = fc(name, value, row)

            t += '      <td %s>%s</td>' % (color, text) 
        t +=     '    </tr>\n'
    t +=         '  </tbody>\n'
    t +=         '</table>\n'  

    return t

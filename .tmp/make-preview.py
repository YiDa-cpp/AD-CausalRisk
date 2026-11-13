# -*- coding: utf-8 -*-
"""Extract boot markup + styles from index.html into a standalone preview page."""
import io
import re

html = io.open('frontend/index.html', encoding='utf-8').read()
style = re.search(r'(?s)<style>(.*?)</style>', html).group(1)
boot = re.search(r'(?s)<div id="boot".*?\n    </div>', html).group(0)

page = (
    '<!doctype html><html><head><meta charset="utf-8"><style>'
    + style
    + '</style></head><body style="margin:0">'
    + boot
    + '</body></html>'
)
io.open('frontend/.shots/boot-preview.html', 'w', encoding='utf-8', newline='\n').write(page)
print('preview html written:', len(page), 'chars')

# -*- coding: utf-8 -*-
"""Standalone preview of the boot loader (styles + canvas + inline script)."""
import io
import re

html = io.open('frontend/index.html', encoding='utf-8').read()
style = re.search(r'(?s)<style>(.*?)</style>', html).group(1)
boot = re.search(r'(?s)<div id="boot".*?\n    </div>', html).group(0)
script = re.search(r'(?s)<script>\n    // 首屏加载动画.*?</script>', html).group(0)

page = (
    '<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><style>'
    + style
    + '</style></head><body>'
    + boot
    + script
    + '</body></html>'
)
io.open('frontend/.shots/boot-preview.html', 'w', encoding='utf-8', newline='\n').write(page)
print('preview written', len(page))

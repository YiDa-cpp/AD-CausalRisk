# -*- coding: utf-8 -*-
"""Swap the old digit-ring inline script for the canvas boot script."""
import io
import re

path = 'frontend/index.html'
html = io.open(path, encoding='utf-8').read()

builder = io.open('.tmp/rebuild-boot.py', encoding='utf-8').read()
m = re.search(r"(?s)BOOT_JS = '''(.*?)'''", builder)
assert m, 'BOOT_JS template missing'
new_script = m.group(1)
assert 'boot-art' in new_script and 'SIGNALS' in new_script

i = html.find('// 逐字符')
assert i != -1, 'old script comment not found'
k = html.rfind('<script>', 0, i)
j = html.find('</script>', i)
assert k != -1 and j != -1, 'old script bounds not found'

html = html[:k] + new_script.lstrip('\n').rstrip('\n') + '\n' + html[j + len('</script>'):].lstrip('\n')
html = html.replace('\n        <div id="boot"', '\n    <div id="boot"')
io.open(path, 'w', encoding='utf-8', newline='\n').write(html)
print('script swapped; canvas:', 'boot-art' in html, 'signals:', 'SIGNALS' in html, 'old:', 'boot-digits' in html)

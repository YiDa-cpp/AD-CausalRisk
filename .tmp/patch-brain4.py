# -*- coding: utf-8 -*-
"""Fourth pass: smooth frontal contour, darker/larger ring digits."""
import io
import re

p = 'frontend/src/components/common/NeuroLoader.vue'
s = io.open(p, encoding='utf-8').read()

s = s.replace(
    '''             C62,100 66,90 76,85
             C80,76 90,70 101,70''',
    '''             C63,101 67,91 77,86
             C82,77 92,71 103,71''',
)

s = s.replace('stop-color="#5f938c"', 'stop-color="#4e857e"')
s = s.replace('stop-color="#93b5ad"', 'stop-color="#7ea7a0"')
s = s.replace('stop-color="#c8dcd6"', 'stop-color="#b9d2cc"')
s = s.replace('font-size: 14px;\n  fill: url(#neuro-digit-fade);', 'font-size: 15px;\n  fill: url(#neuro-digit-fade);')

io.open(p, 'w', encoding='utf-8', newline='\n').write(s)

h_path = 'frontend/index.html'
h = io.open(h_path, encoding='utf-8').read()
h = h.replace('stop-color="#5f938c"', 'stop-color="#4e857e"')
h = h.replace('stop-color="#93b5ad"', 'stop-color="#7ea7a0"')
h = h.replace('stop-color="#c8dcd6"', 'stop-color="#b9d2cc"')
h = re.sub(r'(\.boot-digit \{[^}]*?font-size:\s*)14px', r'\g<1>15px', h, flags=re.S)
io.open(h_path, 'w', encoding='utf-8', newline='\n').write(h)

print('brain v4 patched')

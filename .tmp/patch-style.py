# -*- coding: utf-8 -*-
"""Raise contrast/weight of loader strokes; sync Vue + index.html."""
import io
import re

def patch(path, prefix):
    s = io.open(path, encoding='utf-8').read()

    def block(name, **repl):
        pat = re.compile(r'(\.' + prefix + r'-brain__' + name + r' \{[^}]*\})')

        def sub(m):
            out = m.group(1)
            for k, v in repl.items():
                key = k.replace('_', '-')
                out = re.sub(r'(' + key + r':\s*)[^;]+;', r'\g<1>' + v + ';', out)
            return out

        return pat.sub(sub, s)

    s = block('shape', stroke='#2f6b66', stroke_width='2.4')
    s = block('folds', stroke='#4c8b83', stroke_width='1.9')
    s = block('links', stroke='#9cc0b9', stroke_width='1.1')
    s = block('nodes', fill='#4f8f87')

    s = s.replace('stroke: #6d9f99', 'stroke: #4c8b83')
    s = s.replace('stroke: #407a75', 'stroke: #2f6b66')
    s = s.replace('stroke: #b7cec9', 'stroke: #9cc0b9')
    s = s.replace('fill: #7aa9a2', 'fill: #4f8f87')
    s = s.replace('stop-color="#6e9c96"', 'stop-color="#5f938c"')
    s = s.replace('stop-color="#a6c0ba"', 'stop-color="#93b5ad"')
    s = s.replace('stop-color="#cfe0db"', 'stop-color="#c8dcd6"')
    if prefix == 'neuro':
        s = s.replace('<circle\n          v-for="(node, i) in nodes"', '<circle\n          v-for="(node, i) in nodes"')
        s = s.replace('r="3.8"', 'r="4.2"')
    else:
        s = s.replace('r="3.8"', 'r="4.2"')

    io.open(path, 'w', encoding='utf-8', newline='\n').write(s)
    print('patched', path)

patch('frontend/src/components/common/NeuroLoader.vue', 'neuro')
patch('frontend/index.html', 'boot')

# -*- coding: utf-8 -*-
"""Regenerate index.html's boot brain from NeuroLoader.vue (single source of truth)."""
import io
import re

vue = io.open('frontend/src/components/common/NeuroLoader.vue', encoding='utf-8').read()
html_path = 'frontend/index.html'
html = io.open(html_path, encoding='utf-8').read()

shape = re.search(r'(?s)        <path\s+class="neuro-brain__shape".*?/>', vue).group(0)
stems = re.findall(r'        <path class="neuro-brain__stem"[^\n]*/>', vue)
folds = re.search(r'(?s)        <g class="neuro-brain__folds">.*?</g>', vue).group(0)
links = re.search(r'(?s)        <g class="neuro-brain__links">.*?</g>', vue).group(0)
nodes_src = re.search(r'(?s)const nodes = \[(.*?)\n\]', vue).group(1)
nodes = re.findall(r'\[(\d+),\s*(\d+)\]', nodes_src)
assert shape and stems and folds and links and nodes, 'extract failed'

def to_boot(block):
    block = block.replace('neuro-brain', 'boot-brain')
    # Vue 6-space indentation -> index.html 12-space indentation (+6)
    return '\n'.join(('      ' + line) if line.strip() else line for line in block.split('\n'))

nodes_html = '\n'.join(
    '              <circle cx="%s" cy="%s" r="3.8" style="--i:%d" />' % (x, y, i)
    for i, (x, y) in enumerate(nodes)
)

brain = '\n'.join([
    '          <g class="boot-brain">',
    to_boot(shape),
    to_boot(stems[0]),
    to_boot(stems[1]),
    to_boot(folds),
    to_boot(links),
    '            <g class="boot-brain__nodes">',
    nodes_html,
    '            </g>',
    '          </g>',
])

pat = re.compile(r'(?s)<g class="boot-brain">.*?\n          </g>\n        </svg>')
assert pat.search(html), 'boot brain block not found'
html = pat.sub(brain + '\n        </svg>', html, count=1)

io.open(html_path, 'w', encoding='utf-8', newline='\n').write(html)
print('boot brain regenerated:', len(nodes), 'nodes')

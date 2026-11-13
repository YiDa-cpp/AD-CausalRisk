# -*- coding: utf-8 -*-
"""Third pass: denser cortical folds (20) + larger ring digits."""
import io
import re

p = 'frontend/src/components/common/NeuroLoader.vue'
s = io.open(p, encoding='utf-8').read()

FOLDS = '''        <g class="neuro-brain__folds">
          <path d="M80,94 C87,98 94,99 101,96" />
          <path d="M82,104 C89,108 96,109 103,106" />
          <path d="M92,82 C99,86 106,87 112,84" />
          <path d="M102,74 C109,78 115,79 120,76" />
          <path d="M122,68 C127,73 129,79 127,85" />
          <path d="M134,66 C139,71 141,78 139,85" />
          <path d="M146,72 C151,77 153,84 152,90" />
          <path d="M158,80 C163,85 165,92 164,98" />
          <path d="M170,94 C174,100 174,107 171,113" />
          <path d="M86,122 C92,127 99,129 107,127" />
          <path d="M98,133 C105,138 113,139 121,135" />
          <path d="M112,121 C119,125 127,125 134,121" />
          <path d="M126,133 C133,137 141,136 147,131" />
          <path class="neuro-brain__folds--fine" d="M138,120 C144,124 151,123 156,118" />
          <path class="neuro-brain__folds--fine" d="M150,128 C155,132 161,131 165,126" />
          <path class="neuro-brain__folds--fine" d="M110,112 C116,116 123,116 129,113" />
          <path class="neuro-brain__folds--fine" d="M128,98 C134,102 140,102 145,98" />
          <path class="neuro-brain__folds--main" d="M129,68 C126,80 122,92 116,102 C112,110 106,116 100,120" />
          <path class="neuro-brain__folds--main" d="M70,118 C86,126 102,128 118,124 C128,122 136,120 144,122" />
          <path class="neuro-brain__folds--main" d="M118,140 C124,146 130,152 134,158" />
        </g>
'''

old = re.search(r'(?s)        <g class="neuro-brain__folds">.*?</g>\n', s)
assert old, 'folds not found'
s = s[:old.start()] + FOLDS + s[old.end():]

s = s.replace('font-size: 12px;\n  fill: url(#neuro-digit-fade);', 'font-size: 14px;\n  fill: url(#neuro-digit-fade);')

io.open(p, 'w', encoding='utf-8', newline='\n').write(s)

# index.html boot digit size (CSS there uses 12px too)
h_path = 'frontend/index.html'
h = io.open(h_path, encoding='utf-8').read()
h = re.sub(r'(\.boot-digit \{[^}]*?font-size:\s*)12px', r'\g<1>14px', h, flags=re.S)
io.open(h_path, 'w', encoding='utf-8', newline='\n').write(h)
print('brain v3 patched')

# -*- coding: utf-8 -*-
"""Second refinement pass: rounder contour, denser folds, 10 nodes."""
import io
import re

p = 'frontend/src/components/common/NeuroLoader.vue'
s = io.open(p, encoding='utf-8').read()

SHAPE = '''        <path
          class="neuro-brain__shape"
          d="M64,112
             C62,100 66,90 76,85
             C80,76 90,70 101,70
             C107,63 118,60 127,63
             C135,58 145,61 150,68
             C160,69 168,76 171,85
             C178,91 180,101 177,111
             C180,121 175,131 166,136
             C163,144 154,148 145,146
             C139,152 128,154 120,149
             C111,153 100,150 94,143
             C83,144 73,137 69,128
             C62,124 60,118 64,112 Z"
        />
        <!-- brain stem + cerebellum lower edge -->
        <path class="neuro-brain__stem" d="M118,148 C120,157 124,165 131,171" />
        <path class="neuro-brain__stem" d="M104,144 C100,151 103,157 110,157 C116,157 119,152 119,146" />
'''

FOLDS = '''        <g class="neuro-brain__folds">
          <path d="M82,92 C88,96 94,97 100,95" />
          <path d="M84,102 C90,106 97,107 103,104" />
          <path d="M94,80 C100,84 106,85 112,82" />
          <path d="M104,72 C110,76 116,77 121,74" />
          <path d="M118,66 C122,72 124,79 123,86" />
          <path d="M132,64 C136,71 137,79 135,87" />
          <path d="M144,70 C149,77 151,84 150,92" />
          <path d="M158,78 C163,84 165,91 163,98" />
          <path d="M170,92 C174,99 174,107 171,114" />
          <path d="M84,120 C90,126 98,128 106,126" />
          <path d="M96,132 C104,137 113,137 121,133" />
          <path class="neuro-brain__folds--fine" d="M110,120 C118,124 127,123 134,119" />
          <path class="neuro-brain__folds--fine" d="M124,132 C131,136 139,135 145,130" />
          <path class="neuro-brain__folds--main" d="M129,66 C126,78 122,90 116,100 C112,108 106,114 100,118" />
          <path class="neuro-brain__folds--main" d="M70,116 C86,124 102,126 118,122 C128,120 136,118 144,120" />
        </g>
'''

LINKS = '''        <g class="neuro-brain__links">
          <path d="M86,96 Q93,90 100,84" />
          <path d="M100,84 Q107,79 114,74" />
          <path d="M114,74 Q122,71 130,70" />
          <path d="M130,70 Q138,72 146,76" />
          <path d="M146,76 Q154,81 160,88" />
          <path d="M160,88 Q165,95 168,102" />
          <path d="M168,102 Q160,110 150,116" />
          <path d="M150,116 Q139,121 128,124" />
          <path d="M128,124 Q116,121 104,116" />
          <path d="M104,116 Q94,107 86,96" />
        </g>
'''

NODES = '''const nodes = [
  [86, 96],
  [100, 84],
  [114, 74],
  [130, 70],
  [146, 76],
  [160, 88],
  [168, 102],
  [150, 116],
  [128, 124],
  [104, 116]
]'''

old = re.search(r'(?s)        <path\s+class="neuro-brain__shape".*?/>\s*\n\s*<!--.*?-->\s*\n\s*<path class="neuro-brain__stem"[^\n]*\n\s*<path class="neuro-brain__stem"[^\n]*\n', s)
assert old, 'shape not found'
s = s[:old.start()] + SHAPE + s[old.end():]

old = re.search(r'(?s)        <g class="neuro-brain__folds">.*?</g>\n', s)
assert old, 'folds not found'
s = s[:old.start()] + FOLDS + s[old.end():]

old = re.search(r'(?s)        <g class="neuro-brain__links">.*?</g>\n', s)
assert old, 'links not found'
s = s[:old.start()] + LINKS + s[old.end():]

s = re.sub(r'(?s)const nodes = \[.*?\n\]', NODES, s)

io.open(p, 'w', encoding='utf-8', newline='\n').write(s)
print('brain v2 patched:', len(s))

# -*- coding: utf-8 -*-
"""Patch NeuroLoader.vue: refined brain geometry + clean (ASCII) comments."""
import io
import re

p = 'frontend/src/components/common/NeuroLoader.vue'
s = io.open(p, encoding='utf-8').read()

SHAPE = '''        <path
          class="neuro-brain__shape"
          d="M62,110
             C60,98 66,88 78,84
             C84,74 96,68 108,70
             C114,62 126,60 134,66
             C142,60 152,64 156,72
             C166,74 173,82 174,92
             C180,100 180,112 172,120
             C168,130 158,136 148,136
             C144,144 134,147 126,143
             C118,147 108,145 103,138
             C94,142 84,138 80,130
             C70,128 62,120 62,110 Z"
        />
        <!-- brain stem + cerebellum lower edge -->
        <path class="neuro-brain__stem" d="M118,144 C120,153 124,161 131,167" />
        <path class="neuro-brain__stem" d="M104,141 C100,148 103,154 110,154 C116,154 119,149 119,143" />
'''

FOLDS = '''        <g class="neuro-brain__folds">
          <path d="M88,80 C82,90 82,100 88,108" />
          <path d="M96,74 C92,84 92,94 96,102" />
          <path d="M112,66 C108,78 107,90 110,100" />
          <path d="M148,72 C156,80 159,91 155,102" />
          <path d="M172,92 C176,102 175,112 169,118" />
          <path d="M92,132 C104,138 118,138 130,132" />
          <path d="M100,124 C110,130 122,130 132,126" />
          <path class="neuro-brain__folds--fine" d="M140,138 C146,144 154,144 158,137" />
          <path class="neuro-brain__folds--fine" d="M148,131 C154,136 160,135 163,129" />
          <path class="neuro-brain__folds--main" d="M128,64 C124,78 120,90 112,100 C108,106 104,110 100,112" />
          <path class="neuro-brain__folds--main" d="M68,116 C84,124 100,126 116,122 C126,120 134,118 142,120" />
        </g>
'''

LINKS = '''        <g class="neuro-brain__links">
          <path d="M84,94 Q94,88 104,82" />
          <path d="M104,82 Q115,76 126,72" />
          <path d="M126,72 Q138,75 148,80" />
          <path d="M148,80 Q157,85 164,92" />
          <path d="M164,92 Q162,102 158,110" />
          <path d="M158,110 Q142,122 126,128" />
          <path d="M126,128 Q112,124 100,118" />
          <path d="M100,118 Q92,106 84,94" />
        </g>
'''

NODES = '''const nodes = [
  [84, 94],
  [104, 82],
  [126, 72],
  [148, 80],
  [164, 92],
  [158, 110],
  [126, 128],
  [100, 118]
]'''

old_shape = re.search(r'(?s)        <path\s+class="neuro-brain__shape".*?/>\s*\n\s*<!--.*?-->\s*\n\s*<path class="neuro-brain__stem"[^\n]*\n\s*<path class="neuro-brain__stem"[^\n]*\n', s)
assert old_shape, 'shape block not found'
s = s[:old_shape.start()] + SHAPE + s[old_shape.end():]

old_folds = re.search(r'(?s)        <g class="neuro-brain__folds">.*?</g>\n', s)
assert old_folds, 'folds block not found'
s = s[:old_folds.start()] + FOLDS + s[old_folds.end():]

old_links = re.search(r'(?s)        <g class="neuro-brain__links">.*?</g>\n', s)
assert old_links, 'links block not found'
s = s[:old_links.start()] + LINKS + s[old_links.end():]

s = re.sub(r'(?s)const nodes = \[.*?\]', NODES, s)

# Replace corrupted (mojibake) HTML/CSS comments with short ASCII ones.
s = re.sub(r'<!--[^\n]*?-->', '<!-- side-view brain: lobes, cortical folds, node links -->', s)
s = re.sub(r'/\*[^\n]*?\*/', '/* neuro loader */', s)

io.open(p, 'w', encoding='utf-8', newline='\n').write(s)
print('patched', len(s), 'chars')

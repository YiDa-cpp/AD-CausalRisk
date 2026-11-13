# -*- coding: utf-8 -*-
"""Scale the loading animation down for desktop viewports."""
import io

# 1) boot layer in index.html
p = 'frontend/index.html'
s = io.open(p, encoding='utf-8').read()
s = s.replace(
    '''      .boot-art {
        display: block;
        width: clamp(194px, 45vw, 328px);
        height: auto;
        aspect-ratio: 1;
      }''',
    '''      .boot-art {
        display: block;
        width: clamp(140px, 17vw, 200px);
        height: auto;
        aspect-ratio: 1;
      }''',
)
s = s.replace('        gap: 14px;\n      }\n      .boot-label {', '        gap: 10px;\n      }\n      .boot-label {')
s = s.replace('        font-size: 18px;\n        font-weight: 600;\n        letter-spacing: 0.2px;\n        color: #384440;', '        font-size: 16px;\n        font-weight: 600;\n        letter-spacing: 0.2px;\n        color: #384440;')
io.open(p, 'w', encoding='utf-8', newline='\n').write(s)
print('boot scaled:', 'clamp(140px, 17vw, 200px)' in s)

# 2) component default size
p2 = 'frontend/src/components/common/NeuroLoader.vue'
v = io.open(p2, encoding='utf-8').read()
v = v.replace("size: { type: Number, default: 240 }", "size: { type: Number, default: 200 }")
v = v.replace('  gap: 14px;\n  width: var(--loader-size);', '  gap: 10px;\n  width: var(--loader-size);')
io.open(p2, 'w', encoding='utf-8', newline='\n').write(v)
print('component size:', 'default: 200' in v)

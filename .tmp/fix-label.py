# -*- coding: utf-8 -*-
"""Restore the corrupted default label (GBK round-trip ate the closing quote)."""
import io

p = 'frontend/src/components/common/NeuroLoader.vue'
lines = io.open(p, encoding='utf-8', errors='replace').read().split('\n')
for i, line in enumerate(lines):
    if line.strip().startswith('label: { type: String, default:'):
        lines[i] = "  label: { type: String, default: '\u6b63\u5728\u8f7d\u5165\u5de5\u4f5c\u53f0...' },"
        print('fixed line', i + 1)
io.open(p, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines))

# -*- coding: utf-8 -*-
"""Rebuild the boot splash in index.html: side-view brain + per-character 01 ring."""
import io

p = 'frontend/index.html'
s = io.open(p, encoding='utf-8').read()

CSS = '''      /* 首屏加载层：仅当资源加载较慢时才可能被看到，main.js 按耗时移除 */
      .app-boot {
        position: fixed;
        inset: 0;
        z-index: 9999;
        display: grid;
        place-items: center;
        background: #ffffff;
        transition: opacity 300ms ease;
        pointer-events: none;
      }
      .app-boot--done { opacity: 0; }
      .boot-logo {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 4px;
        width: 230px;
      }
      .boot-svg { width: 230px; height: 230px; overflow: visible; }
      .boot-outline { fill: none; stroke: #e3efec; stroke-width: 1.4; }
      .boot-ring {
        transform-origin: 120px 120px;
        animation: boot-ring-spin 56s linear infinite;
      }
      .boot-ring text {
        font-family: 'Consolas', 'SFMono-Regular', 'Microsoft YaHei', monospace;
        font-size: 12px;
        letter-spacing: 0;
        fill: url(#boot-digit-fade);
      }
      .boot-digit {
        animation: boot-digit-glow 3.6s ease-in-out infinite;
        animation-delay: calc(var(--i) * -0.0581s);
      }
      .boot-brain__shape {
        fill: #edf7f3;
        stroke: #407a75;
        stroke-width: 2.2;
        stroke-linejoin: round;
        stroke-linecap: round;
      }
      .boot-brain__stem {
        fill: none;
        stroke: #407a75;
        stroke-width: 2;
        stroke-linecap: round;
      }
      .boot-brain__folds {
        fill: none;
        stroke: #6d9f99;
        stroke-width: 1.55;
        stroke-linecap: round;
      }
      .boot-brain__folds--fine { stroke-width: 1.05; opacity: 0.8; }
      .boot-brain__folds--main { stroke-width: 1.8; opacity: 0.95; }
      .boot-brain__links { fill: none; stroke: #b7cec9; stroke-width: 0.85; }
      .boot-brain__nodes circle {
        fill: #7aa9a2;
        animation: boot-node-blink 2.4s ease-in-out infinite;
        animation-delay: calc(var(--i) * -0.3s);
      }
      .boot-label {
        margin: 0;
        font-family: 'Microsoft YaHei', 'Segoe UI', sans-serif;
        font-size: 14px;
        font-weight: 600;
        letter-spacing: 0.3px;
        color: #4a746f;
        text-align: center;
      }
      .boot-dots i {
        font-style: normal;
        animation: boot-dot 1.25s ease-in-out infinite;
      }
      .boot-dots i:nth-child(2) { animation-delay: 0.18s; }
      .boot-dots i:nth-child(3) { animation-delay: 0.36s; }

      @keyframes boot-ring-spin { to { transform: rotate(360deg); } }
      @keyframes boot-digit-glow {
        0%, 100% { opacity: 0.24; }
        40% { opacity: 1; }
        55% { opacity: 0.72; }
      }
      @keyframes boot-node-blink {
        0%, 100% { opacity: 0.3; }
        42% { opacity: 1; }
        62% { opacity: 0.6; }
      }
      @keyframes boot-dot {
        0%, 100% { opacity: 0.15; }
        40% { opacity: 1; }
      }
      @media (prefers-reduced-motion: reduce) {
        .boot-ring, .boot-digit, .boot-brain__nodes circle, .boot-dots i { animation-duration: 80s; }
      }
'''

NODES = [(84, 92), (104, 80), (124, 70), (146, 80), (160, 94), (152, 112), (126, 124), (100, 116)]
nodes_html = '\n'.join(
    '            <circle cx="%d" cy="%d" r="3.8" style="--i:%d" />' % (x, y, i)
    for i, (x, y) in enumerate(NODES)
)

BOOT_HTML = '''    <div id="boot" class="app-boot" aria-live="polite">
      <div class="boot-logo">
        <svg class="boot-svg" viewBox="0 0 240 240" aria-hidden="true">
          <defs>
            <linearGradient id="boot-digit-fade" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0" stop-color="#6e9c96" />
              <stop offset="0.55" stop-color="#a6c0ba" />
              <stop offset="1" stop-color="#cfe0db" />
            </linearGradient>
          </defs>
          <circle class="boot-outline" cx="120" cy="120" r="110" />
          <g class="boot-ring">
            <g id="boot-digits"></g>
          </g>
          <g class="boot-brain">
            <path
              class="boot-brain__shape"
              d="M66,116
                 C64,106 66,96 74,89
                 C76,81 83,74 92,73
                 C95,66 103,61 112,63
                 C117,57 127,56 133,62
                 C141,60 149,64 153,72
                 C161,75 167,83 168,92
                 C174,97 177,105 175,113
                 C172,122 165,128 157,131
                 C153,139 144,144 134,143
                 C127,148 117,148 110,143
                 C101,147 90,143 85,135
                 C76,133 68,125 66,116 Z"
            />
            <path class="boot-brain__stem" d="M116,145 C118,154 122,163 129,170" />
            <path class="boot-brain__stem" d="M102,143 C98,150 101,156 108,156 C114,156 117,151 117,145" />
            <g class="boot-brain__folds">
              <path d="M80,96 C86,100 92,101 98,99" />
              <path d="M82,86 C88,90 94,91 100,88" />
              <path d="M92,76 C98,80 104,81 110,78" />
              <path d="M120,64 C126,70 130,77 131,85" />
              <path d="M136,66 C141,72 144,79 144,87" />
              <path d="M150,76 C155,82 157,89 156,96" />
              <path d="M88,126 C96,131 106,132 115,129" />
              <path d="M98,136 C108,139 118,138 126,134" />
              <path d="M112,120 C120,122 128,121 134,117" />
              <path class="boot-brain__folds--fine" d="M140,136 C146,141 153,141 158,135" />
              <path class="boot-brain__folds--fine" d="M146,128 C152,133 158,132 161,126" />
              <path class="boot-brain__folds--main" d="M122,62 C119,72 116,82 112,90 C109,96 106,100 102,103" />
            </g>
            <g class="boot-brain__links">
              <path d="M84,92 Q94,86 104,80" />
              <path d="M104,80 Q114,74 124,70" />
              <path d="M124,70 Q136,73 146,80" />
              <path d="M146,80 Q155,86 160,94" />
              <path d="M160,94 Q158,104 152,112" />
              <path d="M152,112 Q140,120 126,124" />
              <path d="M126,124 Q112,122 100,116" />
              <path d="M100,116 Q92,104 84,92" />
            </g>
            <g class="boot-brain__nodes">
__NODES__
            </g>
          </g>
        </svg>
        <p class="boot-label">正在载入工作台<span class="boot-dots"><i>.</i><i>.</i><i>.</i></span></p>
      </div>
    </div>
'''.replace('__NODES__', nodes_html)

SCRIPT = '''    <script>
      // 逐字符定位在半径 100 的圆周上（字符沿切线），用 --i 做绕圈亮度波。
      ;(function () {
        var group = document.getElementById('boot-digits')
        if (!group) return
        var digits = '01001011010001001011010001001011010001001011010001001011010001'
        var R = 100
        var out = ''
        for (var i = 0; i < digits.length; i++) {
          var deg = (i / digits.length) * 360
          var rad = ((deg - 90) * Math.PI) / 180
          var x = (120 + R * Math.cos(rad)).toFixed(2)
          var y = (120 + R * Math.sin(rad)).toFixed(2)
          out += '<text class="boot-digit" x="' + x + '" y="' + y + '" transform="rotate(' +
            deg.toFixed(2) + ',' + x + ',' + y + ')" text-anchor="middle" dominant-baseline="central" ' +
            'style="--i:' + i + '">' + digits[i] + '</text>'
        }
        group.innerHTML = out
      })()
    </script>
'''

# 1) head: boot start timestamp
s = s.replace(
    '<title>AD-CausalRisk · 因果风险评估平台</title>',
    '<title>AD-CausalRisk · 因果风险评估平台</title>\n'
    '    <script>\n'
    '      // 记录首屏开始时间：main.js 据此判断"加载是否真的慢"。\n'
    '      window.__bootStartedAt = performance.now()\n'
    '    </script>'
)

# 2) boot CSS
start = s.index('      /* 首屏')
end = s.index('    </style>')
s = s[:start] + CSS + '    </style>' + s[end + len('    </style>'):]

# 3) boot markup
start = s.index('    <div id="boot"')
end = s.index('    <div id="app">')
s = s[:start] + BOOT_HTML + s[end:]

# 4) inline ring script before </body>
s = s.replace('    <script type="module" src="/src/main.js"></script>',
              '    <script type="module" src="/src/main.js"></script>\n' + SCRIPT)

io.open(p, 'w', encoding='utf-8', newline='\n').write(s)
print('index.html rebuilt:', len(s), 'chars')

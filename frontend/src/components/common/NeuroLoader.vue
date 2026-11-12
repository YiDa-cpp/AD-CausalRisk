<template>
  <div class="neuro-loader" :style="{ '--loader-size': `${size}px` }">
    <svg class="neuro-loader__svg" viewBox="0 0 240 240" role="img" :aria-label="label">
          <defs>
            <path id="neuro-digit-ring" d="M120,20 a100,100 0 1,1 -0.01,0" />
          </defs>
          <circle class="neuro-outline" cx="120" cy="120" r="110" />
          <g class="neuro-ring">
            <text>
              <textPath href="#neuro-digit-ring" startOffset="0">01001011010001001011010001001011010001001011010001001011010001</textPath>
            </text>
          </g>
                    <g class="neuro-brain">
            <path class="neuro-brain__shape" d="M118,72 C104,64 88,68 84,82 C70,88 66,104 76,112 C68,124 76,138 90,138 C94,150 108,154 116,146 C118,140 118,132 117,124 C116,108 117,88 118,72 Z" />
            <path class="neuro-brain__shape" d="M122,72 C136,64 152,68 156,82 C170,88 174,104 164,112 C172,124 164,138 150,138 C146,150 132,154 124,146 C122,140 122,132 123,124 C124,108 123,88 122,72 Z" />
            <path class="neuro-brain__stem" d="M120,140 C120,152 124,164 132,172" />
            <g class="neuro-brain__folds">
              <path d="M100,86 C94,98 96,110 104,118" />
              <path d="M90,104 C88,114 92,124 100,128" />
              <path d="M140,86 C146,98 144,110 136,118" />
              <path d="M150,104 C152,114 148,124 140,128" />
              <path d="M106,136 C112,142 128,142 134,136" />
            </g>
            <g class="neuro-brain__links">
              <line x1="102" y1="98" x2="118" y2="110" />
              <line x1="138" y1="98" x2="122" y2="110" />
              <line x1="110" y1="126" x2="118" y2="110" />
              <line x1="130" y1="126" x2="122" y2="110" />
            </g>
            <g class="neuro-brain__nodes">
              <circle cx="102" cy="98" r="3.2" />
              <circle cx="138" cy="98" r="3.2" />
              <circle cx="118" cy="110" r="3.2" />
              <circle cx="110" cy="126" r="3.2" />
              <circle cx="130" cy="126" r="3.2" />
            </g>
          </g>
    </svg>

    <p class="neuro-loader__label">
      {{ label }}
      <span class="neuro-loader__dots" aria-hidden="true"><i>.</i><i>.</i><i>.</i></span>
    </p>
  </div>
</template>

<script setup>
defineProps({
  label: { type: String, default: '正在载入工作台' },
  size: { type: Number, default: 220 }
})
</script>

<style scoped>
.neuro-loader {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  width: var(--loader-size);
}

.neuro-loader__svg {
  width: var(--loader-size);
  height: var(--loader-size);
  overflow: visible;
}

/* ---- 外圈细圆环 ---- */
.neuro-outline {
  fill: none;
  stroke: #e1f0ed;
  stroke-width: 1.6;
}

/* ---- 二进制数字环 ---- */
.neuro-ring {
  transform-origin: 120px 120px;
  animation: neuro-ring-spin 40s linear infinite;
}

.neuro-ring__text {
  font-family: var(--font-display, 'Segoe UI', sans-serif);
  font-size: 9.5px;
  letter-spacing: 3.2px;
  fill: #bccdc8;
}

/* ---- 手绘大脑 ---- */
.neuro-brain {
  transform: scale(1.1);
  transform-origin: 120px 120px;
}

.neuro-brain__shape {
  fill: #eef8f5;
  stroke: #3f7a76;
  stroke-width: 2.4;
  stroke-linejoin: round;
}

.neuro-brain__stem {
  fill: none;
  stroke: #3f7a76;
  stroke-width: 2.4;
  stroke-linecap: round;
}

.neuro-brain__folds {
  fill: none;
  stroke: #6fa39e;
  stroke-width: 1.6;
  stroke-linecap: round;
}

.neuro-brain__links {
  stroke: #9db8b3;
  stroke-width: 1;
}

.neuro-brain__nodes circle {
  fill: #7f9c98;
  stroke: #f4fbf9;
  stroke-width: 1;
}

/* ---- 省略号 ---- */
.neuro-loader__label {
  margin: 0;
  font-family: var(--font-sans, 'Microsoft YaHei', sans-serif);
  font-size: 14px;
  font-weight: 600;
  letter-spacing: 0.3px;
  color: #4a746f;
  text-align: center;
}

.neuro-loader__dots i {
  font-style: normal;
  animation: neuro-dot 1.25s ease-in-out infinite;
}

.neuro-loader__dots i:nth-child(2) {
  animation-delay: 0.18s;
}

.neuro-loader__dots i:nth-child(3) {
  animation-delay: 0.36s;
}

@keyframes neuro-ring-spin {
  to {
    transform: rotate(360deg);
  }
}

@keyframes neuro-dot {
  0%,
  100% {
    opacity: 0.15;
  }
  40% {
    opacity: 1;
  }
}

@media (prefers-reduced-motion: reduce) {
  .neuro-ring,
  .neuro-loader__dots i {
    animation-duration: 80s;
  }
}
</style>

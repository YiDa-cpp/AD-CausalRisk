<template>
  <div class="neuro-loader" :style="{ '--loader-size': `${size}px` }">
    <svg class="neuro-loader__svg" viewBox="0 0 240 240" role="img" :aria-label="label">
      <defs>
        <path id="neuro-digit-ring" d="M120,26 a94,94 0 1,1 -0.01,0" />
      </defs>

      <!-- 外圈：二进制数字环（缓慢旋转） -->
      <g class="neuro-ring neuro-ring--digits">
        <text class="neuro-ring__text">
          <textPath href="#neuro-digit-ring" startOffset="0">
            0100101101001011010010110100101101001011010010110100101101001011010010110100101101001011010010110100101101001011
          </textPath>
        </text>
      </g>

      <!-- 两段细弧线，反向旋转 -->
      <circle class="neuro-arc neuro-arc--a" cx="120" cy="120" r="103" />
      <circle class="neuro-arc neuro-arc--b" cx="120" cy="120" r="103" />

      <!-- 徽标底盘 -->
      <circle class="neuro-disc" cx="120" cy="120" r="64" />

      <!-- 手绘大脑（左右半球）+ 网络节点 -->
      <g class="neuro-brain">
        <path
          class="neuro-brain__shape"
          d="M116,76
             C104,68 88,72 82,86
             C68,92 62,108 70,122
             C64,136 72,152 90,154
             C98,164 110,164 116,156 Z"
        />
        <path
          class="neuro-brain__shape"
          d="M124,76
             C136,68 152,72 158,86
             C172,92 178,108 170,122
             C176,136 168,152 150,154
             C142,164 130,164 124,156 Z"
        />
        <g class="neuro-brain__folds">
          <path d="M92,94 C84,104 86,116 94,124" />
          <path d="M110,88 C104,102 106,118 112,130" />
          <path d="M148,94 C156,104 154,116 146,124" />
          <path d="M130,88 C136,102 134,118 128,130" />
        </g>
        <g class="neuro-brain__links">
          <line x1="100" y1="104" x2="118" y2="96" />
          <line x1="118" y1="96" x2="140" y2="104" />
          <line x1="100" y1="104" x2="108" y2="136" />
          <line x1="140" y1="104" x2="132" y2="136" />
          <line x1="108" y1="136" x2="132" y2="136" />
          <line x1="118" y1="96" x2="120" y2="122" />
        </g>
        <g class="neuro-brain__nodes">
          <circle cx="100" cy="104" r="3.2" />
          <circle cx="118" cy="96" r="3.2" />
          <circle cx="140" cy="104" r="3.2" />
          <circle cx="108" cy="136" r="3.2" />
          <circle cx="132" cy="136" r="3.2" />
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

/* ---- 二进制数字环 ---- */
.neuro-ring--digits {
  transform-origin: 120px 120px;
  animation: neuro-ring-spin 28s linear infinite;
}

.neuro-ring__text {
  font-family: var(--font-display, 'Segoe UI', sans-serif);
  font-size: 7.5px;
  letter-spacing: 1.6px;
  fill: #a9c9c6;
  opacity: 0.95;
}

/* ---- 旋转弧线 ---- */
.neuro-arc {
  fill: none;
  stroke-linecap: round;
  stroke-width: 2;
  transform-origin: 120px 120px;
}

.neuro-arc--a {
  stroke: #7cc8c5;
  stroke-dasharray: 70 560;
  animation: neuro-arc-spin 7.5s linear infinite;
}

.neuro-arc--b {
  stroke: #a7dbd7;
  stroke-dasharray: 34 560;
  animation: neuro-arc-spin 11s linear infinite reverse;
}

/* ---- 徽标与大脑 ---- */
.neuro-disc {
  fill: #eff9f8;
  stroke: #d8eeeb;
  stroke-width: 1;
}

.neuro-brain__shape {
  fill: #d9f0ed;
  stroke: #2f8f8d;
  stroke-width: 2.6;
  stroke-linejoin: round;
}

.neuro-brain__folds {
  fill: none;
  stroke: #67b8b4;
  stroke-width: 1.7;
  stroke-linecap: round;
  opacity: 0.9;
}

.neuro-brain__links {
  stroke: #67b8b4;
  stroke-width: 1.2;
  opacity: 0.75;
}

.neuro-brain__nodes circle {
  fill: #3a9b98;
  stroke: #e8f7f5;
  stroke-width: 1.2;
}

/* ---- 省略号 ---- */
.neuro-loader__label {
  margin: 0;
  font-family: var(--font-sans, 'Microsoft YaHei', sans-serif);
  font-size: 14px;
  font-weight: 600;
  letter-spacing: 0.3px;
  color: #3f6f6c;
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

@keyframes neuro-arc-spin {
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
  .neuro-ring--digits,
  .neuro-arc,
  .neuro-loader__dots i {
    animation-duration: 60s;
  }
}
</style>

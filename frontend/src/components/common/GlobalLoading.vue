<template>
  <transition name="global-loading">
    <div v-if="visible" class="global-loading" aria-live="polite" aria-busy="true">
      <div class="global-loading__card">
        <div class="global-loading__mark" aria-hidden="true">
          <span class="global-loading__ring"></span>
          <span class="global-loading__core">AD</span>
        </div>
        <p class="global-loading__title">AD-CausalRisk</p>
        <p class="global-loading__text">正在载入工作台…</p>
        <span class="global-loading__bar" aria-hidden="true"><i></i></span>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { onBeforeUnmount, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'

/**
 * 全局加载动画：路由切换时覆盖整页，最小可见时长 480ms，避免一闪而过。
 *
 * 遮罩不拦截点击（pointer-events: none），这样自动化测试与用户在过渡期间的
 * 操作不会被挡住；它只负责"看得见"的加载反馈。
 */
const router = useRouter()
const visible = ref(false)
const MIN_VISIBLE_MS = 480

let hideTimer = null
let shownAt = 0

function show() {
  if (hideTimer) {
    clearTimeout(hideTimer)
    hideTimer = null
  }
  if (visible.value) return
  shownAt = Date.now()
  visible.value = true
}

function hide() {
  const elapsed = Date.now() - shownAt
  const delay = Math.max(0, MIN_VISIBLE_MS - elapsed)
  hideTimer = window.setTimeout(() => {
    visible.value = false
    hideTimer = null
  }, delay)
}

onMounted(() => {
  router.beforeEach(show)
  router.afterEach(hide)
  router.onError(hide)
})

onBeforeUnmount(() => {
  if (hideTimer) clearTimeout(hideTimer)
})
</script>

<style scoped>
.global-loading {
  position: fixed;
  inset: 0;
  z-index: 2900;
  display: grid;
  place-items: center;
  background: rgba(236, 248, 255, 0.82);
  -webkit-backdrop-filter: blur(6px);
  backdrop-filter: blur(6px);
  pointer-events: none;
}

.global-loading__card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  min-width: 240px;
  padding: 26px 34px 24px;
  border: 1px solid rgba(10, 115, 173, 0.14);
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.86);
  box-shadow: 0 18px 50px rgba(10, 60, 85, 0.12);
}

.global-loading__mark {
  position: relative;
  display: grid;
  place-items: center;
  width: 58px;
  height: 58px;
  margin-bottom: 2px;
}

.global-loading__ring {
  position: absolute;
  inset: 0;
  border-radius: 50%;
  border: 3px solid rgba(10, 115, 173, 0.14);
  border-top-color: #0a73ad;
  border-right-color: #38bdf8;
  animation: global-spin 860ms linear infinite;
}

.global-loading__core {
  display: grid;
  place-items: center;
  width: 38px;
  height: 38px;
  border-radius: 50%;
  background: linear-gradient(140deg, #0a73ad 0%, #38bdf8 100%);
  color: #fff;
  font-size: 13px;
  font-weight: 800;
  letter-spacing: 0.5px;
  box-shadow: 0 6px 16px rgba(10, 115, 173, 0.28);
}

.global-loading__title {
  margin: 0;
  font-family: var(--font-display);
  font-size: 15px;
  font-weight: 700;
  letter-spacing: 0.4px;
  color: var(--ink);
}

.global-loading__text {
  margin: 0;
  font-size: 12px;
  color: var(--muted);
}

.global-loading__bar {
  position: relative;
  display: block;
  width: 168px;
  height: 4px;
  margin-top: 6px;
  overflow: hidden;
  border-radius: 999px;
  background: rgba(10, 115, 173, 0.12);
}

.global-loading__bar i {
  position: absolute;
  inset: 0 auto 0 0;
  width: 40%;
  border-radius: inherit;
  background: linear-gradient(90deg, #0a73ad 0%, #38bdf8 70%, #7dd3fc 100%);
  animation: global-bar 1.15s ease-in-out infinite;
}

.global-loading-enter-active,
.global-loading-leave-active {
  transition: opacity 180ms ease;
}

.global-loading-enter-from,
.global-loading-leave-to {
  opacity: 0;
}

@keyframes global-spin {
  to {
    transform: rotate(360deg);
  }
}

@keyframes global-bar {
  0% {
    transform: translateX(-110%);
  }
  55% {
    transform: translateX(150%);
  }
  100% {
    transform: translateX(280%);
  }
}

@media (prefers-reduced-motion: reduce) {
  .global-loading__ring,
  .global-loading__bar i {
    animation-duration: 2.4s;
  }
}
</style>

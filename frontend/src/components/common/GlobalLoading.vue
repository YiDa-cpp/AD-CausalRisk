<template>
  <transition name="global-loading">
    <div v-if="visible" class="global-loading" aria-live="polite" aria-busy="true">
      <NeuroLoader />
    </div>
  </transition>
</template>

<script setup>
import { onBeforeUnmount, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import NeuroLoader from '@/components/common/NeuroLoader.vue'

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
  background: rgba(247, 252, 252, 0.9);
  -webkit-backdrop-filter: blur(4px);
  backdrop-filter: blur(4px);
  pointer-events: none;
}

.global-loading-enter-active,
.global-loading-leave-active {
  transition: opacity 180ms ease;
}

.global-loading-enter-from,
.global-loading-leave-to {
  opacity: 0;
}
</style>

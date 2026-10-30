<template>
  <div class="patient-home">
    <!-- 卡片 1：我现在怎么样（最大字号） -->
    <section class="hcard hcard--status" aria-labelledby="status-title">
      <p id="status-title" class="hcard__label">我的风险状态</p>
      <p class="hcard__status" aria-live="polite">{{ statusText }}</p>
      <p class="hcard__note">{{ statusNote }}</p>
    </section>

    <!-- 卡片 2：下次复诊 -->
    <section class="hcard" aria-labelledby="visit-title">
      <p id="visit-title" class="hcard__label">下次复诊</p>
      <p class="hcard__value" :class="{ 'is-empty': nextVisit === null }">
        {{ nextVisit ?? '待医生安排' }}
      </p>
      <p class="hcard__note">复诊时间由医生安排，若有变动会电话通知。</p>
    </section>

    <!-- 卡片 3：一键求助 -->
    <section class="hcard hcard--help">
      <p class="hcard__label">需要帮助？</p>
      <el-button type="primary" class="help-button" @click="askHelp">
        一键联系医生
      </el-button>
      <p class="hcard__note">工作时间内医生会尽快回复；紧急情况请直接拨打 120。</p>
    </section>
  </div>
</template>

<script setup>
import { ElMessageBox } from 'element-plus'

/**
 * P1 骨架：患者端只呈现"结论 + 时间 + 求助"三件事，
 * 不出现任何原始分数、图权重或内部轨迹（等后端 PatientAssessmentSummary 上线后再接）。
 */
const statusText = '待医生确认'
const statusNote = '医生复核后，这里会显示通俗的风险说明。'
const nextVisit = null

async function askHelp() {
  await ElMessageBox.alert(
    '请联系您的主治医生。联系方式将在账号与档案绑定后显示在本页。',
    '联系医生',
    { confirmButtonText: '我知道了', type: 'info' }
  )
}
</script>

<style scoped>
.patient-home {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.hcard {
  padding: 28px 24px;
  background: var(--surface);
  border: 1px solid var(--line);
  border-radius: var(--r-xl);
  box-shadow: var(--shadow-card);
}

.hcard--status {
  background: linear-gradient(150deg, #ffffff 0%, #f0f9ff 100%);
  border-color: rgba(10, 115, 173, 0.22);
}

.hcard__label {
  margin: 0 0 12px;
  font-size: 18px;
  font-weight: 700;
  color: var(--muted);
}

/* 适老：结论字号 34–40px，行高宽松 */
.hcard__status {
  margin: 0;
  font-family: var(--font-heading);
  font-size: clamp(34px, 6vw, 40px);
  line-height: 1.25;
  font-weight: 700;
  color: var(--brand-700);
}

.hcard__value {
  margin: 0;
  font-family: var(--font-display);
  font-size: clamp(28px, 5vw, 34px);
  font-weight: 700;
  color: var(--ink);
}

.hcard__value.is-empty {
  font-size: clamp(24px, 4vw, 28px);
  color: var(--muted);
}

.hcard__note {
  margin: 14px 0 0;
  font-size: 16px;
  line-height: 1.7;
  color: var(--muted);
}

.help-button {
  width: 100%;
  height: 68px;
  font-size: 22px;
  font-weight: 700;
  border-radius: var(--r-lg);
}
</style>

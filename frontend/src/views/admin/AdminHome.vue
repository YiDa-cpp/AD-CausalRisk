<template>
  <div class="admin-home">
    <div class="admin-grid admin-grid--metrics">
      <article v-for="metric in metrics" :key="metric.key" class="panel metric">
        <p class="metric__label">{{ metric.label }}</p>
        <p class="metric__value" :class="{ 'is-empty': metric.value === null }">
          {{ metric.value ?? '待接入' }}
        </p>
        <p class="metric__hint">{{ metric.hint }}</p>
        <span class="metric__spark" aria-hidden="true" :class="metric.tone" />
      </article>
    </div>

    <div class="admin-grid admin-grid--charts">
      <article class="panel chart">
        <header class="panel__head">
          <h2>近 30 天评估量</h2>
          <span class="panel__tag">ECharts · P3</span>
        </header>
        <div class="chart__empty">
          <el-icon><TrendCharts /></el-icon>
          <p>等待接入聚合接口</p>
        </div>
      </article>

      <article class="panel chart">
        <header class="panel__head">
          <h2>风险等级分布</h2>
          <span class="panel__tag">ECharts · P3</span>
        </header>
        <div class="chart__empty">
          <el-icon><PieChart /></el-icon>
          <p>BLOCKED 不计入分布</p>
        </div>
      </article>
    </div>

    <article class="panel audit">
      <header class="panel__head">
        <h2>实时审计</h2>
        <span class="panel__tag">GET /api/audit-logs</span>
      </header>
      <div class="audit__empty">
        <el-icon><Tickets /></el-icon>
        <p>审计流将在 P3 接入，仅管理员可见</p>
      </div>
    </article>
  </div>
</template>

<script setup>
import { PieChart, Tickets, TrendCharts } from '@element-plus/icons-vue'

/**
 * P1 骨架：null 表示"尚未接入"，渲染成"待接入"，不编造任何业务数据。
 * P3 接入 /api/dashboard/summary（待后端新增）与 /api/audit-logs。
 */
const metrics = [
  { key: 'new', label: '今日新增档案', value: null, hint: '较昨日 —', tone: 'is-blue' },
  { key: 'high', label: '高危预警', value: null, hint: '风险等级 HIGH', tone: 'is-red' },
  { key: 'python', label: 'Python 服务', value: null, hint: '健康检查未接入', tone: 'is-green' }
]
</script>

<style scoped>
.admin-home {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.admin-grid {
  display: grid;
  gap: 16px;
}

.admin-grid--metrics {
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
}

.admin-grid--charts {
  grid-template-columns: minmax(0, 1.6fr) minmax(0, 1fr);
}

@media (max-width: 900px) {
  .admin-grid--charts {
    grid-template-columns: 1fr;
  }
}

.panel {
  position: relative;
  padding: 18px 20px;
  border: 1px solid rgba(120, 190, 235, 0.18);
  border-radius: var(--r-lg);
  background: linear-gradient(160deg, rgba(22, 54, 80, 0.72), rgba(12, 32, 50, 0.72));
  overflow: hidden;
}

.panel__head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 14px;
}

.panel__head h2 {
  margin: 0;
  font-size: 15px;
  font-weight: 700;
  letter-spacing: 0.3px;
  color: #dcecfb;
}

.panel__tag {
  font-size: 11px;
  padding: 2px 8px;
  border-radius: 999px;
  color: #7fa6c4;
  border: 1px solid rgba(120, 190, 235, 0.24);
}

.metric__label {
  margin: 0;
  font-size: 13px;
  color: #7fa6c4;
  letter-spacing: 0.3px;
}

.metric__value {
  margin: 10px 0 4px;
  font-family: var(--font-display);
  font-size: 34px;
  font-weight: 700;
  color: #eaf6ff;
  font-variant-numeric: tabular-nums;
}

.metric__hint {
  margin: 0;
  font-size: 12px;
  color: #5d86a4;
}

.metric__value.is-empty {
  font-size: 20px;
  color: #7fa6c4;
  letter-spacing: 0.5px;
}

.metric__spark {
  position: absolute;
  right: -20px;
  bottom: -30px;
  width: 120px;
  height: 120px;
  border-radius: 50%;
  filter: blur(28px);
  opacity: 0.5;
}

.metric__spark.is-blue { background: #2f9ad4; }
.metric__spark.is-red { background: #c5484f; }
.metric__spark.is-green { background: #2f9a72; }

.chart__empty,
.audit__empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
  min-height: 180px;
  color: #5d86a4;
  font-size: 13px;
}

.chart__empty .el-icon,
.audit__empty .el-icon {
  font-size: 30px;
  color: rgba(79, 195, 247, 0.55);
}

.audit__empty {
  min-height: 140px;
}
</style>

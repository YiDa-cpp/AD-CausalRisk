<template>
  <div class="research-home">
    <PageHeader title="研究员工作台" subtitle="导入队列数据、发起批量评估，并跟踪任务进度。">
      <template #extra>
        <el-button :icon="Refresh" @click="refresh">刷新</el-button>
      </template>
    </PageHeader>

    <!-- 数据导入：研究员的主入口，占满整行 -->
    <DataCard title="数据导入" subtitle="CSV 预检通过后再入库，错误行会逐条列出">
      <div class="dropzone" role="button" tabindex="0" aria-disabled="true">
        <el-icon class="dropzone__icon"><UploadFilled /></el-icon>
        <p class="dropzone__title">把 CSV 拖到这里</p>
        <p class="dropzone__hint">或将文件拖入后点击选择；P2 接入 POST /api/import-jobs（multipart）</p>
        <el-button type="primary" size="large" disabled>选择文件</el-button>
      </div>
    </DataCard>

    <div class="research-grid">
      <DataCard title="批量评估" subtitle="勾选受试者后一次发起">
        <EmptyState
          title="队列为空"
          description="导入数据后，这里会显示可评估的受试者与批量操作。"
          :icon="Cpu"
        />
      </DataCard>

      <DataCard title="任务进度" subtitle="最近提交的评估任务">
        <EmptyState
          title="还没有任务"
          description="P2 接入 POST /api/assessment-tasks 与任务轮询后，这里显示实时进度。"
          :icon="DataAnalysis"
        />
      </DataCard>
    </div>
  </div>
</template>

<script setup>
import { Cpu, DataAnalysis, Refresh, UploadFilled } from '@element-plus/icons-vue'
import PageHeader from '@/components/common/PageHeader.vue'
import DataCard from '@/components/common/DataCard.vue'
import EmptyState from '@/components/common/EmptyState.vue'

function refresh() {
  window.location.reload()
}
</script>

<style scoped>
.research-home {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.dropzone {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  padding: 40px 24px;
  border: 2px dashed var(--line-strong);
  border-radius: var(--r-lg);
  background: var(--bg-soft);
  text-align: center;
  transition: border-color var(--dur-base) var(--ease-out), background var(--dur-base) var(--ease-out);
}

.dropzone:hover {
  border-color: var(--brand-600);
  background: var(--brand-50);
}

.dropzone__icon {
  font-size: 34px;
  color: var(--brand-600);
}

.dropzone__title {
  margin: 0;
  font-size: 17px;
  font-weight: 700;
  color: var(--ink);
}

.dropzone__hint {
  margin: 0 0 6px;
  font-size: 13px;
  color: var(--muted);
}

.research-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 16px;
}
</style>

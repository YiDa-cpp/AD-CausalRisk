<template>
  <div class="research-page">
    <PageHeader
      back
      title="研究证据"
      subtitle="只读：封存的模型与报告清单，不加载模型、不执行推理或训练。"
    >
      <template #extra>
        <el-button :icon="Refresh" :loading="loading" @click="load">刷新</el-button>
      </template>
    </PageHeader>

    <EmptyState
      v-if="error"
      :icon="WarningFilled"
      title="研究证据加载失败"
      :description="error"
      action-text="重试"
      @action="load"
    />

    <el-skeleton v-else-if="loading && !catalog" :rows="5" animated />

    <template v-else-if="catalog">
      <DataCard title="证据版本与准入" padding="md">
        <div class="facts">
          <div><dt>证据版本</dt><dd>{{ catalog.evidenceVersion || '—' }}</dd></div>
          <div>
            <dt>产物目录</dt>
            <dd>{{ catalog.lookupConfigured ? '已配置' : '未配置（仅展示登记信息）' }}</dd>
          </div>
          <div><dt>预测准入</dt><dd>{{ admissionLabel(catalog.predictionAdmission) }}</dd></div>
          <div><dt>监测准入</dt><dd>{{ admissionLabel(catalog.monitoringAdmission) }}</dd></div>
        </div>

        <el-alert
          v-if="(catalog.limitations || []).length"
          class="note"
          type="warning"
          :closable="false"
          show-icon
          title="使用边界"
        >
          <ul class="note__list">
            <li v-for="item in catalog.limitations" :key="item">{{ item }}</li>
          </ul>
        </el-alert>
      </DataCard>

      <DataCard title="封存报告" subtitle="点击查看原文（Markdown 快照）" padding="none">
        <el-empty v-if="!(catalog.reports || []).length" description="没有登记的研究报告" />
        <el-table v-else :data="catalog.reports" class="table" row-key="key" @row-click="openReport">
          <el-table-column prop="title" label="标题" min-width="260" show-overflow-tooltip />
          <el-table-column prop="source" label="来源" min-width="240" show-overflow-tooltip />
          <el-table-column prop="sha256" label="SHA-256" min-width="180" show-overflow-tooltip />
          <el-table-column label="操作" width="110" fixed="right">
            <template #default="{ row }">
              <el-button text type="primary" @click.stop="openReport(row)">查看</el-button>
            </template>
          </el-table-column>
        </el-table>
      </DataCard>

      <DataCard title="模型产物" :subtitle="`共 ${(catalog.models || []).length} 个登记产物`" padding="none">
        <el-table :data="catalog.models || []" class="table" row-key="id">
          <el-table-column prop="id" label="产物 ID" min-width="220" />
          <el-table-column prop="family" label="家族" min-width="160" />
          <el-table-column prop="relativePath" label="相对路径" min-width="320" show-overflow-tooltip />
          <el-table-column label="文件存在" width="110">
            <template #default="{ row }">
              <el-tag :type="row.located ? 'success' : 'info'" size="small">
                {{ row.located ? '是' : '否' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="admission" label="准入" min-width="220" />
        </el-table>
      </DataCard>
    </template>

    <el-drawer
      v-model="drawerOpen"
      :title="activeReport?.title || '研究说明'"
      direction="rtl"
      size="760px"
      destroy-on-close
      :close-on-press-escape="true"
    >
      <el-skeleton v-if="reportLoading" :rows="8" animated />
      <template v-else-if="activeReport">
        <p class="meta">
          来源 {{ activeReport.source || '—' }} · SHA-256 {{ activeReport.sha256 || '—' }}
        </p>
        <pre class="markdown">{{ activeReport.markdown || '（没有可显示的正文）' }}</pre>
      </template>
    </el-drawer>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { Refresh, WarningFilled } from '@element-plus/icons-vue'
import PageHeader from '@/components/common/PageHeader.vue'
import DataCard from '@/components/common/DataCard.vue'
import EmptyState from '@/components/common/EmptyState.vue'
import { getResearchEvidence, getResearchReport } from '@/api/research.js'
import { useEscapeToClose } from '@/composables/useEscapeToClose.js'

const catalog = ref(null)
const loading = ref(false)
const error = ref('')

const drawerOpen = ref(false)
const reportLoading = ref(false)
const activeReport = ref(null)

function admissionLabel(value) {
  if (value === 'NO_GO_INDEPENDENT_EVIDENCE_INCOMPLETE') return '暂不纳入（个体证据不完整）'
  if (value === 'QUALIFIED_REFERENCE_AND_CURRENT_SNAPSHOTS_REQUIRED') {
    return '需参考与当前快照同时满足'
  }
  return value || '—'
}

async function load() {
  loading.value = true
  error.value = ''
  try {
    catalog.value = await getResearchEvidence()
  } catch (problem) {
    catalog.value = null
    error.value =
      problem?.code === 403 ? '当前账号无权查看研究证据' : problem?.message || '请稍后重试'
  } finally {
    loading.value = false
  }
}

async function openReport(row) {
  drawerOpen.value = true
  reportLoading.value = true
  activeReport.value = null
  try {
    activeReport.value = await getResearchReport(row.key)
  } catch (problem) {
    ElMessage.error(problem?.message || '研究说明读取失败')
    drawerOpen.value = false
  } finally {
    reportLoading.value = false
  }
}

useEscapeToClose(drawerOpen, () => {
  drawerOpen.value = false
})

onMounted(load)
</script>

<style scoped>
.research-page {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.facts {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 12px 20px;
  margin: 0;
}

.facts dt {
  font-size: 11px;
  letter-spacing: 0.4px;
  text-transform: uppercase;
  color: var(--soft);
}

.facts dd {
  margin: 2px 0 0;
  font-size: 14px;
  font-weight: 600;
  color: var(--ink);
  font-family: var(--font-display);
}

.note {
  margin-top: 14px;
}

.note__list {
  margin: 6px 0 0;
  padding-left: 18px;
  line-height: 1.7;
}

.table {
  width: 100%;
}

.meta {
  margin: 0 0 12px;
  font-size: 12px;
  color: var(--soft);
  word-break: break-all;
}

.markdown {
  margin: 0;
  padding: 16px;
  border: 1px solid var(--line);
  border-radius: var(--r-md);
  background: var(--bg-soft);
  font-size: 12.5px;
  line-height: 1.7;
  white-space: pre-wrap;
  word-break: break-word;
  color: var(--ink-700);
}
</style>

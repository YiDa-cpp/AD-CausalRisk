<template>
  <div class="research-page">
    <PageHeader
      back
      title="研究证据"
      subtitle="证据目录只读；研究表格评估需要受控登记流程产生的冻结快照 ID。"
    >
      <template #extra>
        <el-button :icon="Refresh" :loading="loading" @click="load">刷新</el-button>
      </template>
    </PageHeader>

    <el-tabs v-model="activeTab" class="tabs">
      <el-tab-pane label="证据目录" name="catalog">
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
      </el-tab-pane>

      <el-tab-pane label="研究表格评估" name="table">
        <div class="stack">
          <DataCard
            title="提交冻结快照评估"
            subtitle="同步执行并持久化结果；同一快照只允许一个任务，重复提交走幂等键。"
          >
            <el-form label-width="110px" @submit.prevent>
              <el-form-item label="快照 ID" required>
                <el-input
                  v-model="tableForm.snapshotId"
                  class="field"
                  placeholder="手输快照 ID（正整数）；由受控登记流程写入 research_table_snapshot，界面暂无列表可查"
                  clearable
                  @keyup.enter="submitTable"
                />
              </el-form-item>
            </el-form>
            <div class="table-actions">
              <el-button
                type="primary"
                :loading="tableSubmitting"
                :disabled="!tableForm.snapshotId"
                @click="submitTable"
              >
                提交评估
              </el-button>
              <span class="table-hint">每次提交自动生成 Idempotency-Key；失败会返回可读错误码。</span>
            </div>

            <el-alert
              v-if="tableError"
              class="note"
              type="error"
              :closable="false"
              show-icon
              :title="tableError"
            />
          </DataCard>

          <DataCard title="任务查询" subtitle="按任务 ID 读取已持久化的状态与结果（GET /{id}）。">
            <div class="query-row">
              <el-input
                v-model="queryForm.taskId"
                class="field"
                placeholder="手输任务 ID（正整数），例如 12"
                clearable
                @keyup.enter="loadTableTask"
              />
              <el-button :loading="queryLoading" :disabled="!queryForm.taskId" @click="loadTableTask">
                查询
              </el-button>
            </div>
          </DataCard>

          <DataCard v-if="tableTask" title="任务详情" :subtitle="`任务 #${tableTask.taskId}`">
            <template #header-extra>
              <el-button
                text
                :icon="Refresh"
                :loading="queryLoading"
                @click="refreshTableTask(tableTask.taskId)"
              >
                刷新
              </el-button>
            </template>
            <dl class="facts">
              <div>
                <dt>状态</dt>
                <dd><el-tag :type="statusTagType(tableTask.status)" size="small">{{ statusLabel(tableTask.status) }}</el-tag></dd>
              </div>
              <div><dt>快照</dt><dd>#{{ tableTask.snapshotId }}</dd></div>
              <div><dt>受试者</dt><dd>#{{ tableTask.subjectId }}</dd></div>
              <div><dt>runId</dt><dd class="mono">{{ tableTask.runId || '—' }}</dd></div>
              <div><dt>错误码</dt><dd class="mono">{{ tableTask.errorCode || '—' }}</dd></div>
              <div><dt>更新于</dt><dd>{{ formatTime(tableTask.updatedAt) }}</dd></div>
            </dl>

            <el-alert
              v-if="taskSummary"
              class="note"
              type="info"
              :closable="false"
              show-icon
              :title="taskSummary"
            />

            <el-collapse v-if="tableTask.result" class="result">
              <el-collapse-item title="完整结果 JSON" name="json">
                <pre class="json">{{ prettyResult }}</pre>
              </el-collapse-item>
            </el-collapse>
            <p v-else class="table-hint">该任务还没有结果（状态为 OUTCOME_UNKNOWN 或执行失败）。</p>
          </DataCard>
        </div>
      </el-tab-pane>
    </el-tabs>

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
        <div class="markdown-body" v-html="renderedMarkdown"></div>
      </template>
    </el-drawer>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { Refresh, WarningFilled } from '@element-plus/icons-vue'
import PageHeader from '@/components/common/PageHeader.vue'
import DataCard from '@/components/common/DataCard.vue'
import EmptyState from '@/components/common/EmptyState.vue'
import {
  getResearchEvidence,
  getResearchReport,
  getResearchTableTask,
  submitResearchTableTask
} from '@/api/research.js'
import { newIdempotencyKey } from '@/api/assessments.js'
import { renderMarkdown } from '@/utils/markdown.js'
import { useEscapeToClose } from '@/composables/useEscapeToClose.js'

const catalog = ref(null)
const loading = ref(false)
const error = ref('')

const drawerOpen = ref(false)
const reportLoading = ref(false)
const activeReport = ref(null)

// ---- 研究表格评估 ----
const activeTab = ref('catalog')
const tableForm = ref({ snapshotId: '' })
const tableSubmitting = ref(false)
const tableError = ref('')
const tableTask = ref(null)
const queryForm = ref({ taskId: '' })
const queryLoading = ref(false)

const STATUS_LABEL = {
  COMPLETED: '已完成',
  BLOCKED: '已阻断',
  FAILED: '失败',
  OUTCOME_UNKNOWN: '结果未知'
}

const STATUS_TAG = {
  COMPLETED: 'success',
  BLOCKED: 'warning',
  FAILED: 'danger',
  OUTCOME_UNKNOWN: 'info'
}

function statusLabel(value) {
  return STATUS_LABEL[value] || value || '—'
}

function statusTagType(value) {
  return STATUS_TAG[value] || 'info'
}

const prettyResult = computed(() => {
  if (!tableTask.value?.result) return ''
  try {
    return JSON.stringify(tableTask.value.result, null, 2)
  } catch {
    return String(tableTask.value.result)
  }
})

/** 结果里能稳定给出的摘要：记录数、阻断数、问题数、预测窗口。 */
const taskSummary = computed(() => {
  const result = tableTask.value?.result
  if (!result) return ''
  const admission = result.admission || {}
  const parts = []
  if (admission.recordCount !== undefined) parts.push(`记录 ${admission.recordCount} 条`)
  if (admission.blockedRecordCount !== undefined) {
    parts.push(`阻断 ${admission.blockedRecordCount} 条`)
  }
  if (Array.isArray(admission.issues)) parts.push(`问题 ${admission.issues.length} 项`)
  if (result.predictionWindowMonths !== undefined) parts.push(`窗口 ${result.predictionWindowMonths} 个月`)
  return parts.join(' · ')
})

/**
 * 提交冻结快照评估：后端同步执行并落库，返回的就是最终任务快照。
 * 失败时用后端错误消息（403 无权限 / 409 快照已有任务 / 400 参数无效）。
 */
async function submitTable() {
  const snapshotId = Number(tableForm.value.snapshotId)
  if (!Number.isInteger(snapshotId) || snapshotId <= 0) {
    ElMessage.warning('快照 ID 必须是正整数')
    return
  }
  tableSubmitting.value = true
  tableError.value = ''
  try {
    tableTask.value = await submitResearchTableTask({
      snapshotId,
      idempotencyKey: newIdempotencyKey()
    })
    queryForm.value.taskId = String(tableTask.value?.taskId ?? '')
    ElMessage.success(`任务 #${tableTask.value?.taskId} 已返回`)
  } catch (problem) {
    tableError.value = problem?.message || '提交失败，请确认快照存在且当前账号有权限'
  } finally {
    tableSubmitting.value = false
  }
}

async function refreshTableTask(taskId) {
  const id = Number(taskId)
  if (!Number.isInteger(id) || id <= 0) return
  queryLoading.value = true
  try {
    tableTask.value = await getResearchTableTask(id)
    tableError.value = ''
  } catch (problem) {
    tableError.value = problem?.message || '任务读取失败'
  } finally {
    queryLoading.value = false
  }
}

async function loadTableTask() {
  const id = Number(queryForm.value.taskId)
  if (!Number.isInteger(id) || id <= 0) {
    ElMessage.warning('任务 ID 必须是正整数')
    return
  }
  await refreshTableTask(id)
}

const timeFormatter = new Intl.DateTimeFormat('zh-CN', {
  year: 'numeric',
  month: '2-digit',
  day: '2-digit',
  hour: '2-digit',
  minute: '2-digit'
})

function formatTime(value) {
  if (!value) return '—'
  const date = new Date(value)
  return Number.isNaN(date.getTime()) ? '—' : timeFormatter.format(date)
}

/** Markdown → 安全 HTML（工具已做转义，链接仅 http(s)） */
const renderedMarkdown = computed(() =>
  renderMarkdown(activeReport.value?.markdown || '（没有可显示的正文）')
)

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

.tabs :deep(.el-tabs__header) {
  margin-bottom: 16px;
}

.stack {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.field {
  max-width: 520px;
}

.table-actions {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 4px;
}

.table-hint {
  margin: 0;
  font-size: 12px;
  line-height: 1.7;
  color: var(--muted);
}

.query-row {
  display: flex;
  gap: 12px;
  align-items: center;
}

.result {
  margin-top: 14px;
  border-top: 1px solid var(--line);
  border-bottom: 0;
}

.json {
  margin: 0;
  padding: 14px 16px;
  max-height: 420px;
  overflow: auto;
  border-radius: var(--r-sm);
  background: #0f2533;
  color: #e6f4fb;
  font-family: var(--font-display);
  font-size: 12px;
  line-height: 1.6;
}

.mono {
  font-family: var(--font-display);
  word-break: break-all;
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

.markdown-body {
  padding: 18px 20px;
  border: 1px solid var(--line);
  border-radius: var(--r-md);
  background: var(--bg-soft);
  font-size: 13px;
  line-height: 1.75;
  color: var(--ink-700);
  word-break: break-word;
}

.markdown-body :deep(h1),
.markdown-body :deep(h2),
.markdown-body :deep(h3),
.markdown-body :deep(h4) {
  margin: 18px 0 8px;
  color: var(--ink);
  line-height: 1.4;
}

.markdown-body :deep(h1) {
  font-size: 20px;
}

.markdown-body :deep(h2) {
  font-size: 17px;
}

.markdown-body :deep(h3) {
  font-size: 15px;
}

.markdown-body :deep(h4) {
  font-size: 14px;
}

.markdown-body :deep(p) {
  margin: 8px 0;
}

.markdown-body :deep(ul),
.markdown-body :deep(ol) {
  margin: 8px 0;
  padding-left: 20px;
}

.markdown-body :deep(li) {
  margin: 4px 0;
}

.markdown-body :deep(strong) {
  color: var(--ink);
}

.markdown-body :deep(code) {
  padding: 1px 5px;
  border-radius: 4px;
  background: rgba(10, 115, 173, 0.08);
  font-family: var(--font-display);
  font-size: 12px;
}

.markdown-body :deep(pre) {
  margin: 10px 0;
  padding: 12px 14px;
  overflow-x: auto;
  border-radius: var(--r-sm);
  background: #0f2533;
  color: #e6f4fb;
}

.markdown-body :deep(pre code) {
  padding: 0;
  background: transparent;
  color: inherit;
}

.markdown-body :deep(blockquote) {
  margin: 10px 0;
  padding: 6px 14px;
  border-left: 3px solid var(--brand-600);
  color: var(--muted);
  background: rgba(10, 115, 173, 0.04);
}

.markdown-body :deep(hr) {
  margin: 16px 0;
  border: 0;
  border-top: 1px dashed var(--line-strong);
}

.markdown-body :deep(table) {
  width: 100%;
  margin: 10px 0;
  border-collapse: collapse;
  font-size: 12px;
}

.markdown-body :deep(th),
.markdown-body :deep(td) {
  padding: 6px 10px;
  border: 1px solid var(--line);
  text-align: left;
  vertical-align: top;
}

.markdown-body :deep(th) {
  background: var(--brand-50);
  color: var(--ink);
  font-weight: 600;
}

.markdown-body :deep(a) {
  color: var(--brand-600);
  text-decoration: underline;
}
</style>

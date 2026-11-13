<template>
  <div class="qc-page">
    <PageHeader
      back
      title="数据质控"
      subtitle="系统对导入数据的自动质量检查：PASS 通过、WARN 需关注、BLOCKED 阻断评估。人工复核单在「评估复核」中处理。"
    >
      <template #extra>
        <el-radio-group v-model="status" size="small" @change="reload">
          <el-radio-button value="BLOCKED">被阻断</el-radio-button>
          <el-radio-button value="WARN">需关注</el-radio-button>
          <el-radio-button value="PASS">通过</el-radio-button>
          <el-radio-button value="">全部</el-radio-button>
        </el-radio-group>
        <el-button :icon="Refresh" @click="reload">刷新</el-button>
      </template>
    </PageHeader>

    <DataCard padding="none">
      <el-skeleton v-if="loading" :rows="4" animated />

      <EmptyState
        v-else-if="error"
        :icon="WarningFilled"
        title="质控列表加载失败"
        :description="error"
        action-text="重试"
        @action="reload"
      />

      <EmptyState
        v-else-if="items.length === 0"
        :icon="Checked"
        title="没有符合条件的质控记录"
        description="导入或补录数据后，系统会按规则自动生成检查结果；被阻断的记录会阻止发起评估。"
      />

      <template v-else>
        <el-table :data="items" class="table" row-key="id">
          <el-table-column label="受试者" min-width="180">
            <template #default="{ row }">
              <span class="subject">{{ row.subjectAlias || '—' }}</span>
              <span class="subject__code">{{ row.subjectCode || `#${row.subjectId}` }}</span>
            </template>
          </el-table-column>
          <el-table-column label="质控状态" width="120">
            <template #default="{ row }">
              <StatusTag :type="row.qualityStatus" />
            </template>
          </el-table-column>
          <el-table-column label="问题明细" min-width="320">
            <template #default="{ row }">
              <span v-if="issuesOf(row).length === 0" class="empty-cell">无异常</span>
              <ul v-else class="issues">
                <li v-for="(issue, index) in issuesOf(row)" :key="index">{{ issue }}</li>
              </ul>
            </template>
          </el-table-column>
          <el-table-column label="规则版本" width="140">
            <template #default="{ row }">
              <span class="mono">{{ row.ruleVersion || '—' }}</span>
            </template>
          </el-table-column>
          <el-table-column label="检查时间" width="170">
            <template #default="{ row }">{{ formatTime(row.checkedAt) }}</template>
          </el-table-column>
          <el-table-column label="数据版本" width="140">
            <template #default="{ row }">
              <span class="mono">{{ row.dataVersion || '—' }}</span>
            </template>
          </el-table-column>
        </el-table>

        <div class="pager">
          <el-pagination
            v-model:current-page="page"
            :page-size="pageSize"
            :total="total"
            layout="total, prev, pager, next"
            background
            @current-change="load"
          />
        </div>
      </template>
    </DataCard>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { Checked, Refresh, WarningFilled } from '@element-plus/icons-vue'
import PageHeader from '@/components/common/PageHeader.vue'
import DataCard from '@/components/common/DataCard.vue'
import StatusTag from '@/components/common/StatusTag.vue'
import EmptyState from '@/components/common/EmptyState.vue'
import { listQualityChecks } from '@/api/qc.js'

const items = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(20)
const status = ref('')
const loading = ref(true)
const error = ref('')

/** 请求序号守卫：翻页/切筛选时只认最后一次查询 */
let requestSeq = 0

const timeFormatter = new Intl.DateTimeFormat('zh-CN', {
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

/** issues 在库里是 JSON 字符串（如 ["缺失 MMSE"]），兼容已是数组的情况。 */
function issuesOf(row) {
  const raw = row?.issues
  if (Array.isArray(raw)) return raw.filter(Boolean)
  if (typeof raw !== 'string' || !raw.trim()) return []
  try {
    const parsed = JSON.parse(raw)
    return Array.isArray(parsed) ? parsed.filter(Boolean) : [raw]
  } catch {
    return [raw]
  }
}

async function load() {
  // 请求序号：翻页/切筛选很快时，旧页面的响应不能覆盖当前页
  const seq = ++requestSeq
  loading.value = true
  error.value = ''
  try {
    const data = await listQualityChecks({
      status: status.value || undefined,
      page: page.value,
      pageSize: pageSize.value
    })
    if (seq !== requestSeq) return
    items.value = Array.isArray(data?.items) ? data.items : []
    total.value = Number(data?.total ?? items.value.length)
  } catch (problem) {
    if (seq !== requestSeq) return
    items.value = []
    total.value = 0
    error.value = problem?.message || '请稍后重试'
  } finally {
    if (seq === requestSeq) loading.value = false
  }
}

function reload() {
  page.value = 1
  load()
}

onMounted(load)
</script>

<style scoped>
.qc-page {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.table {
  width: 100%;
}

.subject {
  font-weight: 600;
  color: var(--ink);
}

.subject__code {
  margin-left: 8px;
  font-size: 12px;
  color: var(--muted);
  font-family: var(--font-display);
}

.issues {
  margin: 0;
  padding-left: 16px;
  font-size: 13px;
  color: var(--ink);
  line-height: 1.6;
}

.empty-cell {
  font-size: 13px;
  color: var(--soft);
}

.mono {
  font-family: var(--font-display);
  font-size: 12px;
  color: var(--muted);
}

.pager {
  display: flex;
  justify-content: flex-end;
  padding: 14px 18px;
  border-top: 1px solid var(--line);
}
</style>

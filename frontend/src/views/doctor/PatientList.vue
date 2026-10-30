<template>
  <div class="patient-list">
    <PageHeader
      title="受试者档案"
      subtitle="仅展示授权范围内的受试者；点击任意一行查看档案概览。"
    >
      <template #extra>
        <el-input
          v-model="keyword"
          class="search"
          placeholder="在当前页搜索编号 / 别名"
          clearable
          :prefix-icon="Search"
        />
        <el-button :icon="Refresh" @click="load">刷新</el-button>
      </template>
    </PageHeader>

    <DataCard padding="none">
      <!-- 加载态：骨架屏，保持与表格相同的行高，避免布局跳动 -->
      <div v-if="loading" class="skeleton" aria-busy="true" aria-live="polite">
        <div v-for="row in 6" :key="row" class="skeleton__row">
          <el-skeleton-item variant="text" style="width: 14%" />
          <el-skeleton-item variant="text" style="width: 20%" />
          <el-skeleton-item variant="text" style="width: 10%" />
          <el-skeleton-item variant="text" style="width: 16%" />
          <el-skeleton-item variant="text" style="width: 12%" />
        </div>
      </div>

      <!-- 失败态：不是"空数据"，必须分开表达 -->
      <EmptyState
        v-else-if="error"
        :icon="WarningFilled"
        title="档案加载失败"
        :description="error.message || '请稍后重试；如果持续失败，请联系管理员确认授权。'"
        action-text="重新加载"
        @action="load"
      />

      <!-- 空态 -->
      <EmptyState
        v-else-if="filteredItems.length === 0"
        :icon="User"
        :title="keyword ? '当前页没有匹配的档案' : '授权范围内还没有档案'"
        :description="
          keyword
            ? '关键词只过滤当前页；清空关键词可看整页数据。'
            : '档案由医生建档或研究员导入后出现在这里。'
        "
      />

      <template v-else>
        <el-table
          :data="filteredItems"
          class="table"
          row-key="id"
          highlight-current-row
          @row-click="openDrawer"
        >
          <el-table-column prop="subjectCode" label="档案编号" min-width="160" />
          <el-table-column prop="alias" label="别名" min-width="140" />
          <el-table-column label="状态" width="120">
            <template #default="{ row }">
              <StatusTag :type="row.status" />
            </template>
          </el-table-column>
          <el-table-column prop="dataVersion" label="数据版本" min-width="140" />
          <el-table-column label="建档时间" width="180">
            <template #default="{ row }">{{ formatTime(row.createdAt) }}</template>
          </el-table-column>
          <el-table-column label="操作" width="100" fixed="right">
            <template #default="{ row }">
              <el-button text type="primary" @click.stop="openDrawer(row)">查看</el-button>
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

    <!-- 抽屉：基础信息占位，详情/因果图 P3 接入 -->
    <el-drawer
      v-model="drawerOpen"
      :title="selected?.alias || '档案概览'"
      direction="rtl"
      size="460px"
      class="patient-drawer"
    >
      <template v-if="selected">
        <div class="drawer__head">
          <StatusTag :type="selected.status" />
          <span class="drawer__code">{{ selected.subjectCode }}</span>
        </div>

        <el-descriptions :column="1" border class="drawer__desc">
          <el-descriptions-item label="别名">{{ selected.alias }}</el-descriptions-item>
          <el-descriptions-item label="档案编号">{{ selected.subjectCode }}</el-descriptions-item>
          <el-descriptions-item label="状态">
            <StatusTag :type="selected.status" />
          </el-descriptions-item>
          <el-descriptions-item label="数据版本">{{ selected.dataVersion }}</el-descriptions-item>
          <el-descriptions-item label="建档时间">
            {{ formatTime(selected.createdAt) }}
          </el-descriptions-item>
        </el-descriptions>

        <el-alert
          class="drawer__note"
          type="info"
          :closable="false"
          show-icon
          title="详细信息待接入"
          description="访视记录、评估结果与个体因果图将在 P3 接入 GET /api/subjects/{subjectId} 后显示。"
        />

        <div class="drawer__actions">
          <el-button disabled>查看访视记录</el-button>
          <el-button disabled>发起评估</el-button>
        </div>
      </template>
    </el-drawer>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { Refresh, Search, User, WarningFilled } from '@element-plus/icons-vue'
import PageHeader from '@/components/common/PageHeader.vue'
import DataCard from '@/components/common/DataCard.vue'
import StatusTag from '@/components/common/StatusTag.vue'
import EmptyState from '@/components/common/EmptyState.vue'
import { listSubjects } from '@/api/subjects.js'

const items = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(20)
const loading = ref(true)
const error = ref(null)
const keyword = ref('')

const drawerOpen = ref(false)
const selected = ref(null)

/**
 * 契约里 GET /api/subjects 只有 page / pageSize，没有 keyword。
 * 因此这里的关键词只过滤"当前页"，界面上也明确写清楚，避免让用户误以为在全局搜索。
 */
const filteredItems = computed(() => {
  const q = keyword.value.trim().toLowerCase()
  if (!q) return items.value
  return items.value.filter(
    (row) =>
      String(row.subjectCode || '').toLowerCase().includes(q) ||
      String(row.alias || '').toLowerCase().includes(q)
  )
})

async function load() {
  loading.value = true
  error.value = null
  try {
    const data = await listSubjects({ page: page.value, pageSize: pageSize.value })
    items.value = Array.isArray(data?.items) ? data.items : []
    total.value = Number(data?.total ?? 0)
  } catch (problem) {
    // request.js 已经弹过全局提示，这里只记录状态用于页面内呈现
    error.value = problem ?? { message: '' }
    items.value = []
    total.value = 0
  } finally {
    loading.value = false
  }
}

function openDrawer(row) {
  selected.value = row
  drawerOpen.value = true
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

onMounted(load)
</script>

<style scoped>
.patient-list {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.search {
  width: 260px;
}

.skeleton {
  padding: 18px 20px;
}

.skeleton__row {
  display: flex;
  gap: 24px;
  align-items: center;
  height: 48px;
  border-bottom: 1px solid var(--line);
}

.skeleton__row:last-child {
  border-bottom: none;
}

.table {
  width: 100%;
}

.table :deep(.el-table__row) {
  cursor: pointer;
}

.table :deep(.el-table__row:hover > td) {
  background: var(--brand-50);
}

.pager {
  display: flex;
  justify-content: flex-end;
  padding: 14px 20px;
  border-top: 1px solid var(--line);
}

.drawer__head {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.drawer__code {
  font-family: var(--font-display);
  font-size: 14px;
  color: var(--muted);
}

.drawer__desc :deep(.el-descriptions__label) {
  width: 96px;
  color: var(--muted);
}

.drawer__note {
  margin: 18px 0;
  border-radius: var(--r-md);
}

.drawer__actions {
  display: flex;
  gap: 12px;
}
</style>

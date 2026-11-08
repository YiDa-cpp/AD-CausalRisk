<template>
  <div class="audit-page">
    <PageHeader back title="审计日志" subtitle="谁在什么时候做了什么；仅管理员可见，按时间倒序。">
      <template #extra>
        <el-button :icon="Refresh" :loading="loading" @click="load(page)">刷新</el-button>
      </template>
    </PageHeader>

    <DataCard padding="none">
      <div class="filter">
        <el-input
          v-model="eventType"
          class="filter__input"
          size="small"
          clearable
          placeholder="事件类型（如 ASSESSMENT_REVIEW）"
          @keyup.enter="search"
        />
        <el-input
          v-model="actorId"
          class="filter__input filter__input--narrow"
          size="small"
          clearable
          placeholder="操作人 ID"
          @keyup.enter="search"
        />
        <el-input
          v-model="keyword"
          class="filter__input"
          size="small"
          clearable
          placeholder="摘要关键词"
          @keyup.enter="search"
        />
        <el-button size="small" :icon="Search" @click="search">查询</el-button>
        <span class="filter__count">共 {{ total }} 条</span>
      </div>

      <AuditStream :events="items" :loading="loading" :error="error" show-refresh @refresh="load(page)" />

      <div v-if="total > pageSize" class="pager">
        <el-pagination
          v-model:current-page="page"
          :page-size="pageSize"
          :total="total"
          layout="total, prev, pager, next"
          background
          @current-change="load"
        />
      </div>
    </DataCard>

    <p class="audit-page__foot">
      分页与筛选由服务端完成（GET /api/audit-logs/page）；事件类型需要精确匹配，操作人与摘要关键词支持筛选。
    </p>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { Refresh, Search } from '@element-plus/icons-vue'
import PageHeader from '@/components/common/PageHeader.vue'
import DataCard from '@/components/common/DataCard.vue'
import AuditStream from '@/components/admin/AuditStream.vue'
import { listAuditLogsPaged } from '@/api/audit.js'

const items = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = ref(20)
const eventType = ref('')
const actorId = ref('')
const keyword = ref('')
const loading = ref(false)
const error = ref('')

async function load(target = page.value) {
  loading.value = true
  error.value = ''
  try {
    const data = await listAuditLogsPaged({
      page: target,
      pageSize: pageSize.value,
      eventType: eventType.value.trim(),
      actorId: actorId.value.trim(),
      keyword: keyword.value.trim()
    })
    items.value = Array.isArray(data?.items) ? data.items : []
    total.value = Number(data?.total ?? items.value.length)
    page.value = Number(data?.page ?? target)
    if (items.value.length === 0 && total.value > 0 && page.value > 1) {
      page.value -= 1
      await load(page.value)
    }
  } catch (problem) {
    items.value = []
    total.value = 0
    error.value = problem?.code === 403 ? '仅管理员可查看审计日志' : '审计接口不可用'
  } finally {
    loading.value = false
  }
}

function search() {
  load(1)
}

onMounted(() => load(1))
</script>

<style scoped>
.audit-page {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.filter {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
  padding: 14px 18px;
  border-bottom: 1px solid var(--line);
}

.filter__input {
  width: 220px;
}

.filter__input--narrow {
  width: 130px;
}

.filter__count {
  margin-left: auto;
  font-size: 12px;
  color: var(--muted);
}

.pager {
  display: flex;
  justify-content: flex-end;
  padding: 14px 18px;
  border-top: 1px solid var(--line);
}

.audit-page__foot {
  margin: 0;
  font-size: 12px;
  color: var(--muted);
}
</style>

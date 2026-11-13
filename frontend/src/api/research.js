import request from './request.js'
import { newIdempotencyKey } from './assessments.js'

/**
 * 研究证据目录（ResearchEvidenceController）。
 *
 * GET /api/research/evidence → { evidenceVersion, lookupConfigured, models[], reports[],
 *   predictionAdmission, monitoringAdmission, limitations[] }
 * GET /api/research/evidence/{key} → 单份报告的元信息 + markdown 原文
 */
export function getResearchEvidence() {
  return request.get('/research/evidence')
}

export function getResearchReport(key) {
  return request.get(`/research/evidence/${key}`)
}

/**
 * 研究表格评估任务（ResearchTableAssessmentController，V13 新增）。
 *
 * POST /api/research/table-assessment-tasks
 *   Header: Idempotency-Key（必填，1–100 字符）
 *   Body:   { snapshotId }（正整数，来自受控登记流程写入的 research_table_snapshot）
 *   返回 ResearchTableTask：{ taskId, snapshotId, subjectId, runId, status, errorCode,
 *   result, createdAt, updatedAt }；status ∈ COMPLETED / BLOCKED / FAILED / OUTCOME_UNKNOWN。
 *
 * 注意：当前后端没有"快照列表/登记"的公开接口，snapshotId 只能由受控登记流程产生，
 * 因此前端暂不提供提交入口；此方法先作为联调/后续页面接入的请求封装。
 */
export function submitResearchTableTask({ snapshotId, idempotencyKey }) {
  return request.post(
    '/research/table-assessment-tasks',
    { snapshotId: Number(snapshotId) },
    { headers: { 'Idempotency-Key': idempotencyKey || newIdempotencyKey() } }
  )
}

/** GET /api/research/table-assessment-tasks/{id} —— 读取已持久化的研究任务与结果。 */
export function getResearchTableTask(taskId) {
  return request.get(`/research/table-assessment-tasks/${taskId}`)
}

import request from './request.js'

/**
 * GET /api/subjects
 *
 * 契约只声明 page（≥1，默认 1）与 pageSize（1..100，默认 20），没有 keyword 参数，
 * 所以关键词检索只能在当前页内做（见 views/doctor/PatientList.vue 的说明）。
 * 返回 PageSubject：{ items, page, pageSize, total }
 */
export function listSubjects({ page = 1, pageSize = 20, keyword = '' } = {}) {
  return request.get('/subjects', { params: { page, pageSize, keyword } })
}

/**
 * GET /api/subjects/{subjectId}
 * 返回 SubjectDetail：{ subject, visits[], features[] }
 * 访问不到时后端返回 403（存在但无权）或 400（不存在）。
 */
export function getSubjectDetail(subjectId) {
  return request.get(`/subjects/${subjectId}`)
}

/**
 * POST /api/subjects —— 新建档案（仅 ADMIN / RESEARCHER）。
 * body：{ subjectCode, alias, status? }
 * subjectCode 必须匹配 ^DEMO-[A-Za-z0-9-]{1,45}$
 */
export function createSubject({ subjectCode, alias, status }) {
  return request.post('/subjects', { subjectCode, alias, status })
}

/**
 * PATCH /api/subjects/{subjectId} —— 编辑档案。
 * body 与创建相同；subjectCode 不允许改动（必须与存量一致，否则后端拒绝）。
 */
export function updateSubject(subjectId, { subjectCode, alias, status }) {
  return request.patch(`/subjects/${subjectId}`, { subjectCode, alias, status })
}

/** POST /api/subjects/{subjectId}/visits —— 补录访视。 */
export function createSubjectVisit(subjectId, payload) {
  return request.post(`/subjects/${subjectId}/visits`, payload)
}

/** POST /api/subjects/{subjectId}/features —— 补录结构化特征。 */
export function createSubjectFeature(subjectId, payload) {
  return request.post(`/subjects/${subjectId}/features`, payload)
}

/**
 * POST /api/subjects/{subjectId}/observations —— 补录观测（访视型或特征型）。
 * body：{ kind, visitCode, visitDate, mmse, moca, cdrSb, featureName, featureValue,
 *         recordedAt, unit, source(必填), missingReason }
 */
export function createSubjectObservation(subjectId, payload) {
  return request.post(`/subjects/${subjectId}/observations`, payload)
}

/**
 * GET /api/subjects/{id}/feature-sources —— 特征数据来源（subject_feature 行）。
 * 每行含 feature 名、值、单位、来源与导入任务。
 */
export function getFeatureSources(subjectId) {
  return request.get(`/subjects/${subjectId}/feature-sources`)
}

/**
 * GET /api/subjects/{id}/visit-sources —— 访视数据来源。
 * 每行：{ id, visitCode, visitDate, rawMmse, rawMoca, rawCdrSb, source,
 *         missingReason, dataVersion, importJobId }
 */
export function getVisitSources(subjectId) {
  return request.get(`/subjects/${subjectId}/visit-sources`)
}

/**
 * GET /api/subjects/{id}/capabilities —— 当前账号对该档案的能力判定。
 * 返回布尔集合：{ readRaw, manage, record, writeClinical, requestAssessment }
 */
export function getSubjectCapabilities(subjectId) {
  return request.get(`/subjects/${subjectId}/capabilities`)
}

/**
 * GET /api/subjects/{id}/graph-diff?from&to —— 两次评估的图结构差异。
 * from/to 必须是同一受试者的两个 assessmentId；
 * 返回 { from, to, addedNodes, removedNodes, changedNodes, addedEdges,
 *        changedEdges, removedEdges, limitation }。
 */
export function getGraphDiff(subjectId, from, to) {
  return request.get(`/subjects/${subjectId}/graph-diff`, { params: { from, to } })
}

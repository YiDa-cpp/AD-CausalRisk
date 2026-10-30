import request from './request.js'

/**
 * GET /api/subjects
 *
 * 契约只声明 page（≥1，默认 1）与 pageSize（1..100，默认 20），没有 keyword 参数，
 * 所以关键词检索只能在当前页内做（见 views/doctor/PatientList.vue 的说明）。
 * 返回 PageSubject：{ items, page, pageSize, total }
 */
export function listSubjects({ page = 1, pageSize = 20 } = {}) {
  return request.get('/subjects', { params: { page, pageSize } })
}

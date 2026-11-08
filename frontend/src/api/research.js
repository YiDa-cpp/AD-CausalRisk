import request from './request.js'

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

import request from './request.js'

/**
 * GET /api/system/info —— 运行时版本 / Python 健康 / 模型开关（仅 ADMIN）。
 */
export function getSystemInfo() {
  return request.get('/system/info')
}

/**
 * GET /api/me/preferences —— 当前账号的界面偏好。
 * 默认：{ density: 'comfortable', fontSize: 16, notifications: true }
 */
export function getMyPreferences() {
  return request.get('/me/preferences')
}

/**
 * PATCH /api/me/preferences —— 只传要改的键，后端按现有值合并后保存。
 */
export function saveMyPreferences(patch) {
  return request.patch('/me/preferences', patch)
}

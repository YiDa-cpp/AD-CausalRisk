# 前端功能完备性 —— 缺失接口与交互清单

> **更新时间**：2026-11-08（后端 `#26` 合并后，含 V11/V12、UserManagement / ReportExport / PatientDoctor / AssessmentTrace / Observation / System 等新接口）
> **当前分支**：`feat/backend-integration`
> **结论**：**P0 已清零**。当前剩余问题不再是"没有接口"，而是两类：
> 1. 后端已就绪、前端还没做入口（P1）；
> 2. 需要后端补字段或产品先定口径（P2）；
> 再加上少数受接口上限影响的兜底（P3）。
>
> **历史**：本文件最初（2026-11-07）记录 16 处"手输 ID / 当前页过滤 / 前 100 条自算"的降级。P0 三项已于 `feat/missing-p0-endpoints` 落地；2026-11-08 又完成了用户管理、真实 PDF 导出、患者医生/随访、服务端筛选、审计分页、随访待办、研究证据等适配，历史记录保留在 [附录 A](#附录-a已完成历史记录2026-11-07--2026-11-08)。
>
> **2026-11-14 更新**：P1-4 报告 HTML/JSON 导出、P1-6 质控关键词/受试者筛选、P1-12 任务输入快照查看、P3-7 报告/复核风险等级与受试者筛选均已接入；P2-8 研究表格评估入口已随快照下拉落地（`071e0f0`）。以下正文保留原状，完成状态以本行为准。

---

## 目录

- [一、P0 级：阻断级（已清零）](#一p0-级阻断级已清零)
- [二、P1 级：体验升级与交互补全（有待开发）](#二p1-级体验升级与交互补全有待开发)
- [三、P2 级：需后端配合或产品定调（待定项）](#三p2-级需后端配合或产品定调待定项)
- [四、P3 级：当前受限于接口上限（已知限制）](#四p3-级当前受限于接口上限已知限制)
- [附录 A：已完成历史记录（2026-11-07 / 2026-11-08）](#附录-a已完成历史记录2026-11-07--2026-11-08)
- [附录 B：接口设计约定](#附录-b接口设计约定)
- [附录 C：建议实施顺序](#附录-c建议实施顺序)
- [附录 D：影响面矩阵](#附录-d影响面矩阵)
- [附录 E：核对依据](#附录-e核对依据)

---

## 一、P0 级：阻断级（已清零）

**无。**

P0 核心闭环已 100% 完成，前端不再依赖"手输 ID / 写死文案"：

| 闭环 | 接口 | 落地页面 |
| --- | --- | --- |
| 评估结果列表（分页 + 服务端筛选） | `GET /api/assessments?page&pageSize&reviewStatus&riskLevel&keyword&subjectId&from&to` | `/reviews`、`/reports` |
| 评估任务历史（分页 + 状态筛选） | `GET /api/assessment-tasks?page&pageSize&status&subjectId&from&to` | `/tasks` |
| 患者脱敏摘要 | `GET /api/patients/me/summary` | `/patient` |
| 评估报告（按评估渲染 + 真实 PDF） | `GET /api/reports/{id}`、`GET /api/reports/{id}/download` | `/reports` |
| 患者医生与随访 | `GET /api/patients/me/doctor`、`GET /api/patients/me/follow-up` | `/patient` |

> 历史 P0-1 / P0-2 / P0-3 的原始问题、建议接口与验收标准已归档在 [附录 A](#附录-a已完成历史记录2026-11-07--2026-11-08)，不再作为待办。

---

## 二、P1 级：体验升级与交互补全（有待开发）

> 判定标准：**后端接口已就绪并已确认路径/结构**，只差前端交互入口。全部为纯前端改动。

### 未接入端点总清单（2026-11-13 更新：16 项全部接入）

> 口径：接口矩阵对照 `contracts/java-business.target.openapi.json` 与后端 Controller，筛出「后端已存在、前端尚未封装或未接入 UI」的端点；`GET /api`（根转发）、`/reports/{id}/download`（已用 fetch 接入 PDF）、`/assessment-tasks/{id}/cancel`、`/assessment-tasks/{id}/input` 不计入。导入历史列表与详情合并为 1 项，合计 **16 项**。
>
> 2026-11-13：按管理员要求「后端已存在但前端未实现的接口全部接入 UI」，1–16 已全部实现并验证（最后一批为 7 质控新分页、13 发起质控、15 大屏 summary）。各页面口径如仍需调整，属于展示层微调，不再是「接口未接入」。

| # | 优先级 | 端点 | 现状（2026-11-13） | 口径说明 | 对应条目 |
| --- | --- | --- | --- | --- | --- |
| 1 | P1 | `POST /api/assessment-tasks/submit` | ✅ 已接入：任务页「异步提交」弹窗（受试者 ID + 预测窗口，自动 `modelVersion`） | 需产品确认失败重试/取消时序 | P1-1 |
| 2 | P1 | `GET /api/subjects/{id}/feature-sources` | ✅ 已接入：360 抽屉「数据溯源」卡片 | 字段按接口原样展示（下划线键） | P1-2 |
| 3 | P1 | `GET /api/subjects/{id}/visit-sources` | ✅ 已接入：同上 | 与访视历史同屏展示 | P1-2 |
| 4 | P1 | `GET /api/subjects/{id}/capabilities` | ✅ 已接入：抽屉打开时读取，决定「编辑档案」「发起质控」按钮与补录入口 | 无权限时降级为只读 | P1-2 |
| 5 | P1 | `GET /api/import-jobs` + `GET /api/import-jobs/{jobId}` | ✅ 已接入：导入页「历史导入记录」表格 + 详情弹窗 | — | P1-3 |
| 6 | P1 | `GET /api/import-jobs/{id}/errors.csv` | ✅ 已接入：历史表格「导出错误 CSV」（鉴权 fetch + blob） | — | P1-3 |
| 7 | P1 | `GET /api/quality-checks` | ✅ 已接入：质控页改为服务端分页 + `PASS/WARN/BLOCKED` 筛选（旧 `/api/qc/list` 不再被页面调用） | 展示自动检查结果，人工复核单仍走 `/api/qc/*` | P1-6 |
| 8 | P1 | `PATCH /api/subjects/{subjectId}` | ✅ 已接入：360 概览「编辑档案」弹窗（别名/状态，编号只读） | — | P1-7 |
| 9 | P1 | `POST /api/subjects` | ✅ 已接入：档案列表「新建档案」弹窗（`DEMO-*` 校验） | — | P1-7 |
| 10 | P1 | `POST /api/subjects/{subjectId}/features` | ✅ 已接入：「补录特征」弹窗（基础必填项） | 动态字段字典待产品补充 | P1-8 |
| 11 | P1 | `POST /api/subjects/{id}/observations` | ✅ 已接入：「补录观测」弹窗（visit/feature 两类） | 单位/缺失原因字典待产品给出 | P1-8 |
| 12 | P1 | `POST /api/subjects/{subjectId}/visits` | ✅ 已接入：「补录访视」弹窗（编号/日期/MMSE/MoCA/CDR-SB） | — | P1-8 |
| 13 | P1 | `POST /api/subjects/{subjectId}/quality-checks` | ✅ 已接入：360 概览「发起质控检查」弹窗（PASS/WARN/BLOCKED + issues + 规则版本） | 仅 `canReadRawScores` 可见；与人工复核单是两套记录 | P1-8 |
| 14 | P1 | `GET /api/subjects/{id}/graph-diff?from&to` | ✅ 已接入：360 概览「图谱对比」弹窗（两个评估 + 六项统计 + 免责声明） | — | P1-11 |
| 15 | P2 | `GET /api/dashboard/summary` | ✅ 已接入：管理员大屏 4 指标卡 + 建档趋势 + 状态分布全部改用 summary | 不再前端拉全量档案/质控统计 | P2-2 |
| 16 | P2 | `PATCH /api/system/models/{version}` | ✅ 已接入：系统设置「模型配置」卡片（开关 + 刷新） | 仅 ADMIN、仅已安装模型 | P2-6 |

> 已完成/部分完成的 P1 项（不计入上表）：P1-1 取消（`POST /cancel` 已接入任务抽屉）、P1-4 PDF（`/download?format=pdf` 已接入，HTML/JSON 未做）、P1-5 复核历史（`/assessments/{id}/reviews` 已用于患者 360 抽屉，独立时间线页未做）、P1-9（`GET /system/info` 已接入系统设置）、P1-10（偏好已完成）、P1-12（`/assessment-tasks/{id}/input` 已用于预测窗口，完整快照视图未做）。研究表格评估接口（`POST/GET /api/research/table-assessment-tasks`）已按 P2-8 接入 /research 页内 Tab。

### P1-1 评估任务的「取消 / 提交」（取消已完成，提交待办）

| 项 | 内容 |
| --- | --- |
| 接口 | `POST /api/assessment-tasks/{taskId}/cancel`；`POST /api/assessment-tasks/submit`（与 create 同 body，带 `Idempotency-Key`） |
| 建议交互 | 任务抽屉对 `PENDING/RUNNING` 状态显示「取消任务」（二次确认 + loading + 失败原因展示）；批量评估面板提供「提交」入口替代同步 create |
| 验收 | 取消后任务状态变为 `CANCELLED`，列表与抽屉同步；取消失败（已完成）提示原因 |
| 影响文件 | `views/researcher/TaskList.vue`、`components/doctor/AssessmentPanel.vue` |
| 状态 | **取消已完成**：任务抽屉对 `PENDING` 显示「取消任务」（二次确认 + loading + 失败原因），实测调用 `POST /assessment-tasks/7/cancel`；**提交未做**（见总清单 #1） |

### P1-2 档案数据来源与能力展示

| 项 | 内容 |
| --- | --- |
| 接口 | `GET /api/subjects/{id}/feature-sources`、`GET /api/subjects/{id}/visit-sources`、`GET /api/subjects/{id}/capabilities` |
| 建议交互 | 档案抽屉新增「数据来源」标签页：特征/访视逐行显示 `source`、`missingReason`、`dataVersion`、`importJobId`；「能力」区块显示该档案支持哪些操作（补录/评估/随访） |
| 验收 | 医生能回答"这条 MMSE 是哪次导入、缺失原因是什么"；无权限时不显示原始值 |
| 影响文件 | `views/doctor/PatientList.vue`、`components/doctor/VisitHistory.vue` |

### P1-3 导入历史与错误 CSV 导出

| 项 | 内容 |
| --- | --- |
| 接口 | `GET /api/import-jobs?page&pageSize&status&keyword&from&to`（分页历史）；`GET /api/import-jobs/{id}/errors.csv`（`text/csv` 附件） |
| 建议交互 | `/imports` 下半屏加「最近导入」表（任务号/状态/总行数/有效/无效/时间）；行内「下载错误明细」直接触发 CSV 下载；点击行回填预检面板 |
| 验收 | 刷新页面仍能看到历史任务；错误 CSV 可用 Excel 打开且包含行号与原因 |
| 影响文件 | `views/researcher/ImportCenter.vue`、`api/imports.js` |

### P1-4 报告多格式导出（HTML / JSON，PDF 已接入）

| 项 | 内容 |
| --- | --- |
| 接口 | `GET /api/reports/{id}/download?format=pdf\|html\|json&audience=research\|doctor`（已支持三种格式） |
| 建议交互 | 报告页「下载」改为下拉：PDF（默认）/ HTML（可打印预览）/ JSON（研究归档）；保留按角色选择 `audience` |
| 验收 | 三种格式均能下载且文件名正确；HTML 在浏览器中可读、JSON 可被解析 |
| 影响文件 | `views/doctor/ReportList.vue`、`api/reports.js` |
| 状态 | **PDF 已接入**（报告页「下载文本版 PDF」经 fetch 触发 `/download?format=pdf&audience=...`）；HTML/JSON 格式切换未做 |

### P1-5 复核历史时间线（360 抽屉已展示，独立页未做）

| 项 | 内容 |
| --- | --- |
| 接口 | `GET /api/assessments/{assessmentId}/reviews`（后端早已存在，前端从未调用） |
| 建议交互 | 复核抽屉底部展示时间线：谁在何时做了 `ACKNOWLEDGED / NEEDS_DATA / REJECTED`，以及意见全文 |
| 验收 | 多次复核的评估能看到完整改判历史；无权限时不加载 |
| 影响文件 | `views/doctor/ReviewBoard.vue` |
| 状态 | `/assessments/{id}/reviews` 已封装并用于患者 360 时间线（点击复核显示意见）；复核页独立的完整改判时间线未做 |

### P1-6 质控搜索与新分页接口

| 项 | 内容 |
| --- | --- |
| 接口 | `GET /api/qc/list?subjectCode&subjectAlias&status&page&pageSize`（旧接口已支持搜索）；`GET /api/quality-checks?page&pageSize&status&subjectId&keyword&from&to`（新分页接口） |
| 建议交互 | 质控页加档案编号/别名搜索框；逐步迁移到 `/api/quality-checks` 服务端分页，保留现有审核操作 |
| 验收 | 搜 `DEMO-050` 能命中；分页 `total` 为过滤后总数 |
| 影响文件 | `views/researcher/QcList.vue`、`api/qc.js` |

### P1-7 档案编辑（别名 / 状态）

| 项 | 内容 |
| --- | --- |
| 接口 | `PATCH /api/subjects/{subjectId}`（已存在，前端无入口） |
| 建议交互 | 档案抽屉加「编辑」按钮：别名、状态（`ACTIVE/ARCHIVED`）；保存后列表与抽屉同步，后端已写审计 |
| 验收 | 修改别名后列表即时刷新；非法值由后端 400 并有可读提示 |
| 影响文件 | `views/doctor/PatientList.vue`、`api/subjects.js` |

### P1-8 数据补录（观测 / 访视 / 质控）

| 项 | 内容 |
| --- | --- |
| 接口 | `POST /api/subjects/{id}/observations`、`POST /api/subjects/{subjectId}/visits`、`POST /api/subjects/{subjectId}/quality-checks` |
| 建议交互 | 研究员/医生在档案抽屉里「补录观测」「补录访视」「发起质控」，表单字段按后端 `Input` DTO 生成；提交后刷新来源与历史 |
| 验收 | 补录的数据能在 `visit-sources`/`feature-sources` 与质控列表中看到，且带 `dataVersion` |
| 影响文件 | 新增 `components/subject/ObservationDialog.vue`、`VisitDialog.vue`；`views/doctor/PatientList.vue` |

### P1-9 系统设置接运行时信息（API 已封装，页面未接）

| 项 | 内容 |
| --- | --- |
| 接口 | `GET /api/system/info`（`appVersion / gitCommit / javaVersion / contractVersion / models[]`；`python` 成功时为 `{available, health, latencyMs}`，失败时为 `{available:false, message}`） |
| 建议交互 | `SystemSettings.vue` 用运行时数据替换 `__APP_VERSION__` 等构建常量；Python 不可用时显示明确状态 |
| 验收 | 页面显示的版本/提交号与后端实际运行一致；后端不可达时回退为"离线" |
| 影响文件 | `views/admin/SystemSettings.vue`、新增 `api/system.js` |
| 状态 | `api/system.js` 已封装 `GET /system/info`；`SystemSettings.vue` 仍使用 `__APP_VERSION__` 构建常量，待接运行时数据 |

### P1-10 用户偏好设置（已完成，2026-11-12）

| 项 | 内容 |
| --- | --- |
| 接口 | `GET /api/me/preferences`、`PATCH /api/me/preferences`（默认 `{ density: 'comfortable', fontSize: 16, notifications: true }`） |
| 建议交互 | 顶栏用户菜单加「偏好」：界面密度、字号、通知开关；保存后本地即时生效并写入后端 |
| 验收 | 刷新/换设备后偏好保留；非法键值由后端 400 |
| 影响文件 | `layouts/SidebarLayout.vue`、新增 `api/preferences.js` |
| 状态 | **已完成**：顶栏用户名 →「用户设置」弹窗（字号/密度/通知），`GET/PATCH /api/me/preferences` 已接，保存后即时生效并写后端 |

### P1-11 图谱版本对比入口

| 项 | 内容 |
| --- | --- |
| 接口 | `GET /api/subjects/{id}/graph-diff?from={assessmentId}&to={assessmentId}` |
| 建议交互 | `/graph` 顶部加「对比两次评估」：选择该档案的两个评估 → 展示新增/移除/变更的节点与边，并固定标注"仅比较结构与观测状态，不证明个体因果变化" |
| 验收 | 对比结果与后端返回一致；同一档案不同受试者的评估被后端 400 拒绝时提示清楚 |
| 影响文件 | `views/doctor/GraphView.vue`、`api/assessments.js` |

### P1-12 任务输入快照查看（预测窗口已接入）

| 项 | 内容 |
| --- | --- |
| 接口 | `GET /api/assessment-tasks/{id}/input`（`available=false` 时返回"历史任务未保存输入快照"） |
| 建议交互 | 任务抽屉加「输入快照」区块：输入摘要、数据版本、采集时间、请求体、质控与来源；不可用时展示后端说明而非空白 |
| 验收 | 新任务可看到快照；老任务明确显示"不能从当前资料追溯重建" |
| 影响文件 | `views/researcher/TaskList.vue` |

---

## 三、P2 级：需后端配合或产品定调（待定项）

> 判定标准：**接口/字段尚不存在，或已存在但指标口径/交互规范需要产品先决定**。

### P2-1 用户「最近登录」

| 项 | 内容 |
| --- | --- |
| 现状 | `GET /api/users` 返回 `id/username/status/dataScope/createdAt/displayName/department/phone/officeHours/roles`，**没有 `lastLoginAt`**；`sys_user` 表也没有该列 |
| 需要的后端 | V13 增加 `last_login_at`，登录成功时更新，并在 users 列表返回 |
| 前端准备 | 表格已预留列位，字段一到即可展示；此前不编造"最近登录" |

### P2-2 大屏改用 `dashboard/summary` 与指标口径

| 项 | 内容 |
| --- | --- |
| 现状 | 大屏仍用 `GET /api/subjects` 全量（上限 2000）+ `/api/qc/stats` + `/api/audit-logs` 前端聚合；`GET /api/dashboard/summary` 已存在，返回 `subjects/pendingReview/highRisk/todayFollowups/overdueFollowups/followupPreviewLimit` |
| 待定 | 现有四个指标是「档案总数 / 待审质控 / 质控拦截 / 审计事件」，与 summary 字段（评估复核数、高风险数、今日随访）语义不同，需要产品确认最终展示哪些指标、是否需要趋势序列 |
| 前端准备 | 尚未封装 `api/dashboard.js`；待口径确认后新增该客户端并替换 `loadAll()` 的三请求聚合 |

### P2-3 审计事件详情（前后值）

| 项 | 内容 |
| --- | --- |
| 现状 | `/api/audit-logs` 与 `/api/audit-logs/page` 都只返回 `summary`，没有变更前后值 |
| 需要的后端 | `GET /api/audit-logs/{id}` 返回脱敏后的 `payload.before/after`，或在分页接口内联 |
| 产品 | 需要确认哪些事件类型允许展示 diff（避免泄露敏感字段） |

### P2-4 患者「我的摘要」独立页与导航

| 项 | 内容 |
| --- | --- |
| 现状 | 患者布局（`PatientLayout`）没有侧边栏，`menuRegistry.summary` 仍 `ready:false`；首页已承载摘要 + 复诊 + 医生卡片 |
| 待定 | 是否需要独立 `/summary` 页面（可打印版），以及患者端是否引入底部导航；当前首页信息已覆盖，不重复建设 |
| 前端准备 | 摘要卡片组件可直接复用；打印样式已就绪 |

### P2-5 报告 `audience=patient`（患者版）

| 项 | 内容 |
| --- | --- |
| 现状 | `ReportExportService` 仅接受 `research` / `doctor`；患者摘要走 `/api/patients/me/summary` |
| 待定 | 是否需要"患者版 PDF"（脱敏、无分数/图），以及患者能否自行下载 |
| 风险 | 若开放，必须确保 PDF 不含 `riskScore`、`graph`、`explanations` 等原始字段 |

### P2-6 模型配置界面

| 项 | 内容 |
| --- | --- |
| 现状 | `PATCH /api/system/models/{version}` 已存在（启用/停用模型），前端无入口 |
| 待定 | 需要产品定义"模型启用"的业务语义与审批流程；当前仅系统设置页展示只读信息 |

### P2-7 输入快照 / 图谱对比的展示规范

| 项 | 内容 |
| --- | --- |
| 现状 | `GET /api/assessment-tasks/{id}/input` 与 `/graph-diff` 已就绪（P1-11/P1-12 是入口层） |
| 待定 | 快照与 diff 的展示字段、免责声明措辞、是否允许导出，需要研究/临床双方确认 |

### P2-8 研究表格评估入口（无快照查询接口，暂不加入口）

| 项 | 内容 |
| --- | --- |
| 现状 | `frontend/src/api/research.js` 已封装 `POST /api/research/table-assessment-tasks`（body `{ snapshotId }` + `Idempotency-Key`）与 `GET /api/research/table-assessment-tasks/{id}`。参数与 `contracts/java-business.target.openapi.json`、`ResearchTableProtocol`/`ResearchTableAssessmentService` 完全一致（`snapshotId` 为正整数 int64，body 仅此一个字段）。 |
| 阻塞点 | 后端只有"按已登记的冻结快照提交"，没有快照列表或快照登记接口。`backend/src/test/java/com/adcausalrisk/backend/research/ResearchTableDemo.java` 是**测试侧本地启动器**：需要 manifest.json、handoff.json 两个参数与 `RESEARCH_TABLE_TEST_TOKEN`，启动 `test` profile + H2 内存库 + 随机端口的应用，进程内插入 `seven/ten/blocked` 三个快照后写 handoff JSON 即退出；类注释明确 `There is no writable registration endpoint`。因此产品运行环境拿不到可用的 `snapshotId`。 |
| 结论 | 保持现状：API 已就绪但**不新增 UI 入口**；需等待后端提供可查询（或可创建）的快照列表接口。接口就绪后在图谱大屏 / 研究证据页加入口：选择或输入快照 → 提交任务 → 轮询 `GET /{id}` 展示 `status` 与 `result`。 |

---

## 四、P3 级：当前受限于接口上限（已知限制）

> 这些不是"缺接口"，而是现有接口没有分页/搜索参数，前端只能用"前 N 条"兜底。后端加上参数即可消除。

### P3-1 授权弹窗的档案 / 账号选择上限 100

| 项 | 内容 |
| --- | --- |
| 现状 | `UserManagementController` 的 `GET /api/subjects/{id}/permissions` 与授权写入没有搜索参数；`UserAdmin` 的档案下拉与授权账号下拉各取前 100 条 |
| 消除条件 | `GET /api/users` 已支持 `keyword`（用户列表搜索）；授权下拉可改为远程搜索。档案侧 `GET /api/subjects?keyword=` 也已支持，可同样改远程搜索，或给授权接口加分页 |
| 前端现状 | 下拉已提示"最多列出前 100 个"，不会静默漏选 |

### P3-2 随访「按受试者」下拉上限 100

| 项 | 内容 |
| --- | --- |
| 现状 | `FollowUpList` 的受试者选择器一次拉 100 条；超过 100 个档案选不到 |
| 消除条件 | 改为 `el-select remote` 调 `GET /api/subjects?keyword=`（接口已支持），或给下拉加专用搜索端点 |

### P3-3 大屏档案统计上限 2000

| 项 | 内容 |
| --- | --- |
| 现状 | `AdminHome` 按 `total` 循环拉取，`MAX_SUBJECT_PAGES = 20` → 最多 2000 条；超出会在"档案总数"指标提示"仅统计前 2000 条"，不再冒充全量 |
| 消除条件 | 接入 `dashboard/summary`（P2-2）后，计数由后端 `COUNT(*)` 直接给出 |

### P3-4 列表 CSV 导出仅当前页 / 当前筛选

| 项 | 内容 |
| --- | --- |
| 现状 | 报告、任务、随访的「导出 CSV」只导当前页数据（最多 20 行），不是全量 |
| 消除条件 | 后端提供导出接口（CSV 流）或允许 `pageSize=1000`；也可由前端循环翻页后合并（请求数随页数增长） |

### P3-5 受试者搜索仅按档案编号

| 项 | 内容 |
| --- | --- |
| 现状 | 后端 `keyword` 只匹配 `s.subject_code`；别名搜索会返回空（页面占位符已注明"按档案编号搜索"） |
| 消除条件 | 后端把 `keyword` 扩展到 `alias`（`LIKE %kw%`），并转义 `%`/`_` |

### P3-6 审计事件类型需精确匹配

| 项 | 内容 |
| --- | --- |
| 现状 | `/api/audit-logs/page` 的 `eventType` 是等值匹配，前端只能输入完整常量（如 `ASSESSMENT_REVIEW`），没有枚举下拉 |
| 消除条件 | 后端提供事件类型字典（`GET /api/audit-logs/event-types`）或在文档中固化常量列表 |

### P3-7 报告/复核列表缺少风险等级与受试者筛选 UI

| 项 | 内容 |
| --- | --- |
| 现状 | 后端 `GET /api/assessments` 已支持 `riskLevel`、`subjectId`、`keyword`，前端目前只用了 `reviewStatus` |
| 消除条件 | 纯前端工作（不在 P3 上限问题内），可随时补一个筛选条；记录在此避免遗漏 |

---

## 附录 A：已完成历史记录（2026-11-07 / 2026-11-08）

### A.1 P0-1 评估结果列表（原阻断项，已实现）

**原问题**：`/reviews` 必须手输评估 ID，"全部/待复核"只对已载入的几条做前端过滤，真实"今天有 12 份待复核"无法呈现。

**落地**：`GET /api/assessments` 分页摘要（不含 `agentResult`），支持 `reviewStatus/riskLevel/keyword/subjectId/from/to`；医生看授权档案，ADMIN/RESEARCHER 全量；PATIENT 与 `SUMMARY_READ`-only 医生在列表、任务历史、任务详情上都拿不到 `riskScore/runId`。

**验收**：医生进入 `/reviews` 直接看到待复核列表，无需输入 ID。

### A.2 P0-2 评估任务列表（原阻断项，已实现）

**原问题**：批量评估后刷新即丢，只能记 taskId。

**落地**：`GET /api/assessment-tasks` 分页历史 + `status` 筛选 + `errorCode/message`；任务抽屉展示阶段耗时；`?taskId=` 深链保留。

**验收**：刷新后仍能看到最近任务及失败原因。

### A.3 P0-3 患者个人摘要（原阻断项，已实现）

**原问题**：患者首页写死"等待医生复核"，不管有没有评估。

**落地**：`GET /api/patients/me/summary` 返回脱敏结论、复诊摘要、局限声明；另接 `GET /api/patients/me/doctor` 与 `/api/patients/me/follow-up` 展示主治医生、下次复诊与逾期条数。响应不含 `riskScore`、图权重、解释贡献。

**验收**：患者看到的是"结论句 + 复诊时间 + 医生信息"，不是固定文案。

### A.4 2026-11-08 深度适配完成项

| 能力 | 接口 | 落地 |
| --- | --- | --- |
| 用户管理 | `GET/POST /api/users`、`PATCH /api/users/{id}` | `/admin/users` 真实列表、新增/编辑、角色/状态/资料字段、PATIENT 独立校验 |
| 档案授权 | `GET/POST /api/subjects/{id}/permissions`、`DELETE .../{id}` | 用户管理页「档案授权」标签页 |
| 真实 PDF 导出 | `GET /api/reports/{id}/download` | 报告页「下载 PDF」，按角色选 `audience=doctor/research` |
| 患者医生/随访 | `GET /api/patients/me/doctor`、`/follow-up` | 患者首页医生卡片、复诊与逾期提示 |
| 服务端筛选 | `GET /api/assessments`、`/assessment-tasks`、`/subjects` | 复核/报告/任务/档案页筛选改服务端 |
| 审计分页 | `GET /api/audit-logs/page` | `/admin/audit` 服务端分页 + 事件类型/操作人/关键词筛选 |
| 随访待办 | `GET /api/follow-ups` | `/followups`「全部待办」服务端分页 + `due` 窗口，删除前端 N+1 |
| 研究证据 | `GET /api/research/evidence`、`/{key}` | 新页面 `/research`（版本、准入、封存报告、模型产物、使用边界） |

---

## 附录 B：接口设计约定

1. **统一 Envelope** `{ code, message, data, errorCode, traceId, timestamp }`，成功 `code=0`；分页统一 `PageResult<T> { items, page, pageSize, total }`。
2. **分页**：`page ≥ 1`，`pageSize ∈ [1,100]`，超界钳制；`GET /api/audit-logs` 的数组形态是历史遗留，新代码用 `/api/audit-logs/page`。
3. **筛选**：统一 `keyword/status/from/to` 命名；服务端过滤先于分页与计数。
4. **列表不带大字段**：评估列表不带 `agentResult`；需要看图/解释时再取详情。
5. **权限**：对象级授权在 Java 判定；PATIENT 禁止拿到原始分数/图权重/runId；PATIENT 与其它角色叠加时仍按否决处理。
6. **审计**：写操作落 `audit_event`；`eventType` 用稳定常量。
7. **幂等**：创建类接口沿用 `Idempotency-Key`。
8. **契约同步**：新增/变更必须更新 `contracts/*.openapi.json` 与 `docs/Integration_Contract.md`，并补契约测试。

---

## 附录 C：建议实施顺序

### 第一批（纯前端、价值最高）
1. P1-1 任务提交（取消已完成）
2. P1-3 导入历史 + 错误 CSV
3. P1-5 复核历史时间线（360 抽屉已有，独立页待做）

### 第二批（数据可信度）——2026-11-13 已完成
4. P1-6 质控搜索与分页迁移（未做，仍用 `/api/qc/list`）
5. P1-2 档案来源与能力（✅ 360 抽屉「数据溯源」）
6. P1-7 档案编辑 + P1-8 数据补录（✅ 新建/编辑档案、补录访视/特征/观测）

### 第三批（管理与研究）——2026-11-13 已完成
7. P1-9 系统信息（✅ 系统设置接 `/system/info` + 模型开关）、P1-10 用户偏好（已完成，2026-11-12）
8. P1-11 图谱对比（✅ 360 抽屉弹窗）、P1-12 输入快照（预测窗口已接，完整视图待做）
9. P1-4 报告多格式导出（PDF 已接，HTML/JSON 待做）

### 待后端/产品解锁
- P2-1 最近登录（需 V13 字段）
- P2-2 大屏 summary 口径
- P2-3 审计 diff
- P2-5 患者版 PDF
- P2-6 模型配置（✅ 已接入系统设置「模型配置」）

---

## 附录 D：影响面矩阵

| 项 | 受影响页面 | 不做的后果 |
| --- | --- | --- |
| P1-1 任务取消/提交 | `TaskList`、`AssessmentPanel` | 取消已接入；提交未做时任务只能等超时 |
| P1-2 来源/能力 | `PatientList` 抽屉 | ✅ 已接入「数据溯源」：能力/特征来源/访视来源 |
| P1-3 导入历史/错误 CSV | `ImportCenter` | ✅ 已接入「历史导入记录」+ 详情 + 错误 CSV |
| P1-4 多格式导出 | `ReportList` | 研究归档缺 HTML/JSON（PDF 已接） |
| P1-5 复核时间线 | `ReviewBoard` | 改判历史不可追溯（360 抽屉已展示） |
| P1-6 质控搜索 | `QcList` | 只能按状态翻页找记录 |
| P1-7 档案编辑 | `PatientList` | ✅ 已接入「新建档案」「编辑档案」 |
| P1-8 数据补录 | `PatientList` | ✅ 已接入访视/特征/观测补录 |
| P1-9 系统信息 | `SystemSettings` | ✅ 已接入真实 `/system/info` + 模型配置 |
| P1-10 用户偏好 | 全局 | 已完成：字号/密度/通知可调 |
| P1-11 图谱对比 | `GraphView` | ✅ 已接入 360 抽屉「图谱对比」弹窗 |
| P1-12 输入快照 | `TaskList` | 无法解释历史任务用了什么输入 |
| P2-1 最近登录 | `UserAdmin` | 无法判断账号是否在用 |
| P2-2 大屏口径 | `AdminHome` | 指标口径需产品确认 |
| P3-1/2 前 100 上限 | `UserAdmin`、`FollowUpList` | 超限时选不到（已有提示） |
| P3-3 大屏 2000 上限 | `AdminHome` | 超大库统计不完整（已有截断提示） |
| P3-4 导出仅当前页 | 三个列表 | 导出不是全量 |
| P3-5 仅编号搜索 | `PatientList` | 别名搜索无效 |
| P3-6 事件类型精确匹配 | `AuditLog` | 需记住常量 |
| P3-7 风险等级筛选 | `ReportList`/`ReviewBoard` | 少一个筛选维度 |

---

## 附录 E：核对依据

```bash
# 后端实际映射（含新 Controller）
grep -rn "@GetMapping\|@PostMapping\|@PatchMapping\|@DeleteMapping" backend/src/main/java --include=*Controller.java

# 前端调用面
grep -rn "from '@/api/" frontend/src/views frontend/src/components

# 前端本地过滤/写死上限（应持续减少）
grep -rn "\.filter(\|pageSize: 100\|PAGE_SIZE\|MAX_SUBJECT_PAGES" frontend/src/views frontend/src/components

# 构建与回归
cd frontend && npm run build
node scripts/e2e-roles.mjs
node scripts/e2e-task-list.mjs
node scripts/e2e-graph-interaction.mjs
```

---

**一句话结论**：P0 已清零，P1 是"后端已就绪、前端补入口"的 12 项纯前端工作；P2 是 7 项需要字段或口径决策的事项；P3 是 7 项有明确消除条件的已知上限。下一阶段按附录 C 的第一批开工即可。

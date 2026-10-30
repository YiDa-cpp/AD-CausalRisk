# AD-CausalRisk 前端

Vue 3 + Vite + Element Plus 的单页应用，对接 Java 业务 API（Python 由 Java 的 `AgentClient` 调用，
浏览器不直接访问 Python）。

## 环境与命令

- Node.js ≥ 18（本地验证版本 v24.22.1，npm 11.19.1）
- 安装：`npm install`
- 开发：`npm run dev`（默认 http://localhost:5173，`/api` 代理到 http://localhost:8080）
- 构建：`npm run build`（产物在 `dist/`）
- 预览：`npm run preview`

后端未启动时页面会提示“无法连接服务器”，不再使用本地 Mock 数据。

## 目录结构

```
src/
├─ api/                 # 契约映射层：request.js 是唯一 Axios 实例
│   ├─ request.js       # Envelope 脱壳、401/403 处理、60s 超时
│   ├─ auth.js          # login / logout / fetchCurrentUser
│   ├─ subjects.js      # GET /api/subjects（page / pageSize）
│   └─ imports.js       # POST /api/import-jobs（multipart + Idempotency-Key）/ commit
├─ layouts/             # AppShell + 4 种布局 + 菜单注册表
│   ├─ AppShell.vue     # 按 route.meta.layout 选布局，统一页面过渡
│   ├─ BlankLayout.vue  # 登录 / 异常页
│   ├─ SidebarLayout.vue# 医生、研究员（侧边栏 + 顶栏）
│   ├─ PatientLayout.vue# 患者（无侧栏、单列、大字号）
│   ├─ ScreenLayout.vue # 管理员数据大屏（深色、无侧栏）
│   └─ menuRegistry.js  # 后端 menus key -> 文案/图标/路径
├─ components/
│   ├─ common/          # 原子组件：PageHeader / DataCard / StatusTag / EmptyState
│   ├─ BrainCanvas.vue  # 3D 登录页 Three.js 场景（保留原有逻辑）
│   └─ LoginCard.vue    # 身份选择 + 账号表单
├─ data/                # 角色元信息与 3D 场景文案
├─ directives/          # v-permission（按 roles/permissions 控制元素）
├─ router/              # 路由表 + 守卫（登录态、meta.roles）
├─ stores/              # Pinia：user（roles / menus / permissions，持久化）
├─ styles/
│   ├─ tokens.css       # 设计令牌（唯一真源）
│   ├─ element-overrides.css  # Element Plus 主题覆盖
│   └─ login-3d.css     # 3D 登录页专属样式，仅该路由加载
└─ views/
    ├─ doctor/ researcher/ admin/ patient/   # 四角色首页
    └─ exception/       # 401 / 404 / 500（共用 ExceptionPage）
```

## 布局与菜单

- 路由用 `meta.layout` 决定外壳：`blank`（登录/异常）、`sidebar`（医生、研究员）、
  `patient`（患者，**不挂载侧边栏**）、`screen`（管理员大屏）。
- 侧边栏菜单 = 固定「工作台」+ 后端 `/api/me` 下发的 `menus`（`menuRegistry` 负责文案与图标）。
  后端没给的 key 不渲染；尚未交付的页面渲染成禁用项并标「待建」。
- 路由守卫：未登录 → `/login?redirect=…`；角色不匹配 → `/401`；已登录访问 `/login` → 回到工作台。

## 请求层约定

所有后端响应都是统一 Envelope `{ code, message, data, errorCode, traceId, timestamp }`：

- `code === 0`：拦截器直接返回 `data`，业务代码不再解包；
- `code !== 0` 或非 2xx：统一 `ElMessage` 提示并 reject `{ code, errorCode, message }`；
- `401`：清理登录态并跳回 `/login?redirect=...`（登录接口自身的 401 除外，交由表单内联提示）；
- `403`：提示无权限，不跳转；
- 超时 60s（评估任务需要等待 Python 计算完成）；
- **不发送 `X-Allow-OOR`**：越界值必须由后端正常拦截。

## 设计令牌

颜色、圆角、阴影、字体、动效曲线全部定义在 `styles/tokens.css`，组件里不写死色值：
主色 `--brand-600: #0a73ad`、深色 `--brand-700`、浅底 `--brand-50`、页面底 `--bg`，
圆角 10/14/20/32，阴影用双层环境阴影（不用纯黑），动效统一
`cubic-bezier(.22,1,.36,1)`，并尊重 `prefers-reduced-motion`。

Element Plus 通过 `styles/element-overrides.css` 覆盖：主色、12px 圆角、
大按钮 56px 高、卡片 20px 圆角。

## 当前进度

- **P0（已完成）**：依赖切换（移除 Arco / antd / bw-pro-table / vueuse / dayjs / unocss，
  引入 element-plus 与 icons）、唯一请求实例、Vite 代理与 `@` 别名、路由守卫、Pinia 用户态。
- **P0.5（已完成）**：设计令牌、Element Plus 主题、四个原子组件、
  3D 登录页样式拆分（`tokens.css` + `login-3d.css`）。
- **P1（已完成）**：五种布局（AppShell + Blank/Sidebar/Patient/Screen）、
  由 `menus` 驱动的菜单、四角色首页骨架、Element Plus 按需引入、
  `meta.roles` 守卫；主 chunk 1.07 MB → 381 KB。
- **P2（已完成）**：医生「受试者档案」（分页表格 + 骨架屏 + 空/错态 + 抽屉）
  与研究员「数据导入」（拖拽上传 + Idempotency-Key + 预检面板 + 错误明细 + 确认入库）。
- **P3（下一步）**：评估任务与业务复核、个体因果图（3D 图谱）接入。

## 已知限制（P2）

- `GET /api/subjects` 的冻结契约只有 `page` / `pageSize`，**没有 keyword**，
  因此列表页的搜索框只过滤当前页，界面文案已注明；服务端检索需要契约新增参数。
- 档案抽屉只展示列表已有字段；访视、评估与因果图待 P3 接入 `GET /api/subjects/{subjectId}`。

## 端到端冒烟（可选）

`scripts/e2e-roles.mjs` 用无头 Chrome 跑四种角色：登录 → 落地页 → 布局 → 菜单 → 守卫，
不依赖后端（拦截 `/api/auth/login` 与 `/api/me`）。运行前需要：

```bash
npm i --no-save puppeteer-core
npm run dev -- --port 5199      # 另开终端
node scripts/e2e-roles.mjs      # 截图输出到 .shots/（已 gitignore）
```

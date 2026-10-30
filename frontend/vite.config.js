import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import Components from 'unplugin-vue-components/vite'
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'
import { fileURLToPath, URL } from 'node:url'

export default defineConfig({
  plugins: [
    vue(),
    // Element Plus 按需注册：模板里出现 <el-xxx> 才引入对应组件与 JS。
    // importStyle: false —— 样式统一由 main.js 里的一份 index.css 提供，
    // 保证我们自己 element-overrides.css 的层叠顺序稳定。
    Components({
      resolvers: [ElementPlusResolver({ importStyle: false })],
      dts: false
    })
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    port: 5173,
    proxy: {
      // 浏览器只访问 Java 业务 API；Java 再按需调用 Python 子服务。
      '/api': {
        target: 'http://localhost:8080',
        changeOrigin: true
      }
    },
    watch: {
      // Windows 上编辑器/格式化的短命写入会让 chokidar 报 EBUSY。
      ignored: ['**/.*.tmpdir/**', '**/*.tmp']
    }
  }
})

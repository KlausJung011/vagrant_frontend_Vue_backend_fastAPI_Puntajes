import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    // Proxy para desarrollo local: redirige /puntajes al backend FastAPI
    proxy: {
      '/puntajes': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})

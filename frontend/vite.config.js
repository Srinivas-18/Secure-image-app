import { defineConfig } from 'vite'

export default defineConfig({
  root: '.',
  build: {
    outDir: 'dist',
    rollupOptions: {
      input: {
        main: './templates/index.html',
        logs: './templates/logs.html'
      }
    }
  },
  server: {
    port: 3000
  }
})

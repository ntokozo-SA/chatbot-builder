import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  build: {
    lib: {
      entry: 'src/widget.js',
      name: 'AIChatbotWidget',
      fileName: 'widget',
      formats: ['iife', 'es']
    },
    rollupOptions: {
      external: ['react', 'react-dom'],
      output: {
        globals: {
          react: 'React',
          'react-dom': 'ReactDOM'
        }
      }
    },
    outDir: 'dist',
    assetsDir: 'assets'
  },
  server: {
    port: 5174
  }
}) 
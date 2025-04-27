import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { client_port } from './app.config.json'

// https://vite.dev/config/
export default defineConfig({
  server: {
    port: client_port
  },
  plugins: [react()],
  resolve: {
    alias: {
      src: "/src",
    }
  }
})

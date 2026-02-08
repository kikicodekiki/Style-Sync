import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
const isGitHubPages = process.env.DEPLOY_TARGET === 'gh-pages';

export default defineConfig({
  base: isGitHubPages ? '/Style-Sync/' : '/',
  plugins: [react()],
  server: {
    port: 3000,
    open: true
  }
})

import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),
  ],
<<<<<<< HEAD
  build: {
    outDir: 'dist',
  },
=======
>>>>>>> c1ff09266e50a3e4698620158bc1be04963e8a2d
})

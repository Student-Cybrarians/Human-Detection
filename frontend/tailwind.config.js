/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#00ff88',
        secondary: '#ff00ff',
        dark: '#0a0e27',
        darker: '#050812',
        gray: {
          800: '#1a1f3a',
          700: '#2a2f4a',
        }
      },
      animation: {
        pulse: 'pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        spin: 'spin 1s linear infinite',
      }
    },
  },
  plugins: [],
}

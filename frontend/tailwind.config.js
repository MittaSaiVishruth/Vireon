/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: '#0a0a0f',
        foreground: '#ededed',
        primary: '#7c3aed',
        'primary-hover': '#6d28d9',
        card: '#1a1a24',
        'card-hover': '#242433',
        border: '#2a2a35'
      }
    },
  },
  plugins: [],
}

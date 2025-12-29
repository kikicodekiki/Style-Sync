/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'soft-grey': '#f5f5f5',
        'charcoal': '#2c2c2c',
      },
    },
  },
  plugins: [],
}

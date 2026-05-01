/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}", // Isso aqui é o que faz o App.jsx ficar azul!
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
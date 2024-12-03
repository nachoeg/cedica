import formsPlugin from '@tailwindcss/forms'
import prelinePlugin from 'preline/plugin'

/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}', 'node_modules/preline/dist/*.js'],
  theme: {
    extend: {},
  },
  darkMode: 'class',
  plugins: [formsPlugin, prelinePlugin],
}

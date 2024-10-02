/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/web/templates/**/*.html", "node_modules/preline/dist/*.js"],
  theme: {
    extend: {
      screens: {
        xs: "425px",
      },
    },
    container: {
      center: true,
    },
  },
  darkMode: "class",
  plugins: [require("preline/plugin")],
};

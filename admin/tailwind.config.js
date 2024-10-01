/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/web/templates/**/*.html", "node_modules/preline/dist/*.js"],
  theme: {
    extend: {},
    container: {
      center: true,
    },
  },
  darkMode: "class",
  plugins: [require("preline/plugin")],
};

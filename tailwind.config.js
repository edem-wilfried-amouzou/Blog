/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    // './templates/**/*.html',         // Si vous avez un dossier templates à la racine
    // './mysite/templates/**/*.html',  // Vos templates dans mysite
    // './blog/templates/**/*.html',    // Vos templates dans blog
    // './home/templates/**/*.html',    // Vos templates dans home
    // Recherche tous les fichiers HTML dans n'importe quel sous-dossier "templates"
    './**/templates/**/*.html',
    
    // Si vous avez des fichiers JS qui contiennent des classes Tailwind
    './**/static/**/*.js',
  ],
  theme: {
    extend: {},
  },
  plugins: [require("daisyui")],
}
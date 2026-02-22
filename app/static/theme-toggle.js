const themeBtn = document.getElementById("themeToggleBtn");
const themeIcon = document.getElementById("themeIcon");

const themes = ["auto", "light", "dark"];
let current = 0;

function applyTheme(theme) {
  if (theme === "auto") {
    document.documentElement.setAttribute(
      "data-bs-theme",
      window.matchMedia("(prefers-color-scheme: dark)").matches
        ? "dark"
        : "light",
    );
  } else {
    document.documentElement.setAttribute("data-bs-theme", theme);
  }
  localStorage.theme = theme;
  updateIcon(theme);
}

function updateIcon(theme) {
  switch (theme) {
    case "light":
      themeIcon.className = "bi bi-sun-fill";
      break;
    case "dark":
      themeIcon.className = "bi bi-moon-stars-fill";
      break;
    default:
      themeIcon.className = "bi bi-circle-half";
  }
}

function toggleTheme() {
  current = (current + 1) % themes.length;
  applyTheme(themes[current]);
}

(() => {
  const saved = localStorage.theme || "auto";
  current = themes.indexOf(saved);
  applyTheme(saved);
})();

themeBtn.addEventListener("click", toggleTheme);

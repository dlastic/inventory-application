(function () {
  const el = document.documentElement;

  const saved = localStorage.getItem("theme") || "light";
  el.setAttribute("data-bs-theme", saved);

  window.toggleTheme = function () {
    const current = el.getAttribute("data-bs-theme");
    const next = current === "dark" ? "light" : "dark";

    el.setAttribute("data-bs-theme", next);
    localStorage.setItem("theme", next);
  };
})();

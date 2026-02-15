document.addEventListener("DOMContentLoaded", () => {
  setTimeout(() => {
    document.querySelectorAll(".alert").forEach((alert) => {
      alert.classList.add("fade-out");
      alert.addEventListener("transitionend", () => alert.remove());
    });
  }, 5000);
});

(function () {
  const reader = document.querySelector(".reader");
  if (!reader) return;

  const open = () => reader.classList.add("is-open");
  const close = () => reader.classList.remove("is-open");

  reader.querySelector(".reader__menu-btn")?.addEventListener("click", open);
  reader.querySelector(".reader__backdrop")?.addEventListener("click", close);
  reader.querySelectorAll(".reader__sidebar a").forEach((a) =>
      a.addEventListener("click", close)
  );
  document.addEventListener("keydown", (e) => {
      if (e.key === "Escape") close();
  });
})();

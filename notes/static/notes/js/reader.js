(function () {
    const reader = document.querySelector(".reader");
    if (!reader) return;

    const close = () => reader.classList.remove("is-open");

    reader.addEventListener("click", (e) => {
        if (e.target.closest(".reader__menu-btn")) { reader.classList.add("is-open"); return; }
        if (e.target.closest(".reader__backdrop")) { close(); return; }

        const noteLink = e.target.closest(".reader__note");
        if (noteLink) {
            reader.querySelectorAll(".reader__note.is-active")
                  .forEach((el) => el.classList.remove("is-active"));
            noteLink.classList.add("is-active");
            close();   
        }
    });

    document.addEventListener("keydown", (e) => {
        if (e.key === "Escape") close();
    });
})();

document.addEventListener("click", (e) => {
    if (!e.target.closest("#print-btn")) return;
    const scroller = document.getElementById("pdf-scroll");
    if (!scroller) return;
    const frame = document.createElement("iframe");
    frame.style.cssText = "position:fixed;right:0;bottom:0;width:0;height:0;border:0;";
    frame.src = scroller.dataset.pdfUrl;
    document.body.appendChild(frame);
    frame.onload = () => {
        frame.contentWindow.focus();
        frame.contentWindow.print();
        setTimeout(() => frame.remove(), 1000);
    };
});

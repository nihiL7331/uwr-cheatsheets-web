(function () {
    const el = document.getElementById("brand-text");
    const cursor = document.querySelector(".brand-cursor");
    if (!el) return;

    const FINAL = "noted.";

    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
        el.textContent = FINAL;
        return;
    }

    const START = "notiid.";
    const STOP = "not";
    const wait = (ms) => new Promise((r) => setTimeout(r, ms));
    const typing = (on) => cursor && cursor.classList.toggle("is-typing", on);

    async function run() {
        el.textContent = START;
        await wait(1000);
        typing(true);
        while (el.textContent.length > STOP.length) {
            el.textContent = el.textContent.slice(0, -1);
            await wait(85);
        }
        await wait(180);
        for (let i = STOP.length; i < FINAL.length; i++) { 
            el.textContent = FINAL.slice(0, i + 1);
            await wait(120);
        }
        typing(false);
    }
    run();
})();

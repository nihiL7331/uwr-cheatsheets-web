(function () {
    const canvas = document.getElementById("hero-bg");
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    const CELL = 26;                 
    const MAX_ALPHA = 0.13;         
    const DRAW_THRESHOLD = 0.02;   
    const CURSOR_RADIUS = 130;    
    const CURSOR_BOOST = 0.28;   
    const SPEED = 0.00035;      
    const CHARSET = "abcdefghijklmnopqrstuvwxyz0123456789{}[]()<>;=+/*".split("");

    let dpr, cols, rows, chars, w, h, rect;
    let mouseX = -9999, mouseY = -9999;
    let raf = null, lastDraw = 0;

    function setup() {
        rect = canvas.getBoundingClientRect();
        w = rect.width; h = rect.height;
        dpr = Math.min(window.devicePixelRatio || 1, 1.5);
        canvas.width = Math.floor(w * dpr);
        canvas.height = Math.floor(h * dpr);
        ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
        ctx.font = `${Math.floor(CELL * 0.82)}px ui-monospace, "JetBrains Mono", Menlo, monospace`;
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        ctx.fillStyle = "rgb(230,231,234)";

        cols = Math.ceil(w / CELL) + 1;
        rows = Math.ceil(h / CELL) + 1;
        chars = new Array(cols * rows);
        for (let i = 0; i < chars.length; i++) chars[i] = CHARSET[(Math.random() * CHARSET.length) | 0];
    }

    function field(cx, cy, t) {
        const a = Math.sin(cx * 0.30 + t);
        const b = Math.sin(cy * 0.42 - t * 0.8);
        const c = Math.sin((cx + cy) * 0.20 + t * 1.25);
        const d = Math.sin(Math.hypot(cx - cols * 0.5, cy - rows * 0.5) * 0.18 - t);
        return (a + b + c + d) * 0.25;
    }

    function paint(t, withCursor) {
        ctx.clearRect(0, 0, w, h);
        for (let r = 0; r < rows; r++) {
            for (let c = 0; c < cols; c++) {
                const v = (field(c, r, t) + 1) * 0.5;        
                let alpha = MAX_ALPHA * Math.pow(v, 1.7);    
                const px = c * CELL + CELL * 0.5;
                const py = r * CELL + CELL * 0.5;

                if (withCursor) {
                    const dx = px - mouseX, dy = py - mouseY;
                    const dist2 = dx * dx + dy * dy;
                    if (dist2 < CURSOR_RADIUS * CURSOR_RADIUS) {
                        const f = 1 - Math.sqrt(dist2) / CURSOR_RADIUS;
                        alpha += CURSOR_BOOST * f * f;
                    }
                }

                if (alpha < DRAW_THRESHOLD) continue;   
                ctx.globalAlpha = alpha > 0.6 ? 0.6 : alpha;
                ctx.fillText(chars[r * cols + c], px, py);
            }
        }
        ctx.globalAlpha = 1;
    }

    function loop(now) {
        raf = requestAnimationFrame(loop);
        if (now - lastDraw < 33) return;   
        lastDraw = now;
        paint(now * SPEED, true);
    }

    function start() { if (!raf && !reduce) raf = requestAnimationFrame(loop); }
    function stop() { if (raf) { cancelAnimationFrame(raf); raf = null; } }

    window.addEventListener("mousemove", (e) => { mouseX = e.clientX - rect.left; mouseY = e.clientY - rect.top; });
    window.addEventListener("mouseout", () => { mouseX = -9999; mouseY = -9999; });
    window.addEventListener("scroll", () => { rect = canvas.getBoundingClientRect(); }, { passive: true });

    let resizeTimer;
    window.addEventListener("resize", () => {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(() => { setup(); if (reduce) paint(0, false); }, 150);
    });

    document.addEventListener("visibilitychange", () => { document.hidden ? stop() : start(); });

    setup();
    reduce ? paint(0, false) : start();
})();

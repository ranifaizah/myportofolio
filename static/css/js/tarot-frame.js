/*
 * tarot-frame.js
 * Memasang bingkai "kartu tarot" (garis ganda, bulan sabit, bintang, fase bulan)
 * ke semua modal yang sudah ada. Tidak mengubah markup, id, form, atau event
 * apa pun: hanya menambahkan class "tarot-modal" dan satu elemen dekoratif
 * (aria-hidden, pointer-events: none) di dalam konten modal.
 */
(function () {
    "use strict";

var SELECTOR = [
    ".experience-form-modal__content",
    ".project-form-modal__content",
    ".skill-delete-modal__content",
    ".cosmic-form-panel"
].join(",");

    var NS = "http://www.w3.org/2000/svg";
    var counter = 0;

    function cssVar(name, fallback) {
        var v = getComputedStyle(document.documentElement).getPropertyValue(name).trim();
        return v || fallback;
    }

    function star(x, y, R, opacity, fill, twinkleDelay) {
        var c = R * 0.14;
        var cls = twinkleDelay == null ? "" :
            ' class="tw" style="animation-delay:' + twinkleDelay.toFixed(2) + 's"';
        return '<path' + cls + ' transform="translate(' + x + " " + y + ')" d="M0 ' + (-R) +
            "Q" + c + " " + (-c) + " " + R + " 0Q" + c + " " + c + " 0 " + R +
            "Q" + (-c) + " " + c + " " + (-R) + " 0Q" + (-c) + " " + (-c) + " 0 " + (-R) +
            'Z" fill="' + fill + '" opacity="' + opacity + '"/>';
    }

    function draw(el, svg, uid, hasClose) {
        var w = el.clientWidth, h = el.clientHeight;
        if (!w || !h) return;

        var gold = cssVar("--tarot-gold", "#f0cf94");
        var lineA = cssVar("--tarot-line-a", "#f0cf94");
        var lineB = cssVar("--tarot-line-b", "#d95d39");
        var rose = cssVar("--tarot-rose", "#e8aeae");
        var paper = cssVar("--tarot-paper", "#faf6f0");
        var glow = cssVar("--tarot-glow", "#f6b98a");
        var spark = cssVar("--tarot-spark", "#fff0cf");

        var cx = w / 2, a = 14, b = 23;
        var gid = "tg" + uid, glid = "tl" + uid, mk = "tm" + uid;

        function ring(o, r, gt, gb) {
            return "M" + (cx - gt) + " " + o + "H" + (o + r) +
                "A" + r + " " + r + " 0 0 1 " + o + " " + (o + r) +
                "V" + (h - o - r) +
                "A" + r + " " + r + " 0 0 1 " + (o + r) + " " + (h - o) +
                "H" + (cx - gb) +
                "M" + (cx + gt) + " " + o + "H" + (w - o - r) +
                "A" + r + " " + r + " 0 0 0 " + (w - o) + " " + (o + r) +
                "V" + (h - o - r) +
                "A" + r + " " + r + " 0 0 0 " + (w - o - r) + " " + (h - o) +
                "H" + (cx + gb);
        }

        var o = '<defs>' +
            '<linearGradient id="' + gid + '" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="' + w + '" y2="0">' +
            '<stop offset="0" stop-color="' + lineA + '"/><stop offset=".5" stop-color="' + lineB + '"/><stop offset="1" stop-color="' + lineA + '"/></linearGradient>' +
            '<radialGradient id="' + glid + '"><stop offset="0" stop-color="' + glow + '" stop-opacity=".55"/><stop offset="1" stop-color="' + glow + '" stop-opacity="0"/></radialGradient>' +
            '<mask id="' + mk + '" maskUnits="userSpaceOnUse" x="0" y="0" width="' + w + '" height="' + h + '">' +
            '<rect width="' + w + '" height="' + h + '" fill="#fff"/><circle cx="' + (cx + 6) + '" cy="' + (a - 4) + '" r="10.5" fill="#000"/></mask>';

        // fase bulan di bawah
        var phases = "";
        [4, 2, 0, -2, -4].forEach(function (d, i) {
            var x = cx + (i - 2) * 11, y = h - a;
            if (!d) {
                phases += '<circle cx="' + x + '" cy="' + y + '" r="4.6" fill="' + gold + '"/>';
                return;
            }
            o += '<mask id="' + mk + "p" + i + '" maskUnits="userSpaceOnUse" x="0" y="0" width="' + w + '" height="' + h + '">' +
                '<rect width="' + w + '" height="' + h + '" fill="#fff"/><circle cx="' + (x + d) + '" cy="' + y + '" r="4.6" fill="#000"/></mask>';
            phases += '<circle cx="' + x + '" cy="' + y + '" r="4.6" fill="' + gold + '" mask="url(#' + mk + "p" + i + ')"/>';
        });

        // garis bingkai ganda
        o += "</defs><g fill=\"none\" stroke=\"url(#" + gid + ")\" stroke-linecap=\"round\">" +
            '<path d="' + ring(a, 14, 36, 42) + '" stroke-width="2.2"/>' +
            '<path d="' + ring(b, 8, 30, 36) + '" stroke-width="1"/></g>';

        // bintang sudut, bintang kecil, titik, garis titik-titik
        var len = Math.max(0, Math.min(80, h / 2 - a - 70));
        var offs = [[50, 26, 3.2, 0.9], [27, 53, 2.6, 0.8], [64, 36, 2.2, 0.7], [39, 66, 2.2, 0.7], [20, 40, 1.6, 0.6]];
        var dots = [[58, 20], [22, 66], [72, 52], [34, 34]];
        [[1, 1], [-1, 1], [1, -1], [-1, -1]].forEach(function (q) {
            var sx = q[0], sy = q[1];
            function X(d) { return sx > 0 ? a + d : w - a - d; }
            function Y(d) { return sy > 0 ? a + d : h - a - d; }
            // tombol tutup menempati pojok kanan atas: bintang besar di sana dilewati
            var isTopRight = sx < 0 && sy > 0;
            if (!(hasClose && isTopRight)) {
                o += '<circle cx="' + X(30) + '" cy="' + Y(30) + '" r="20" fill="url(#' + glid + ')"/>' + star(X(30), Y(30), 15, 1, spark);
            }
            offs.forEach(function (t) { o += star(X(t[0]), Y(t[1]), t[2], t[3], gold); });
            dots.forEach(function (t) {
                o += '<circle cx="' + X(t[0]) + '" cy="' + Y(t[1]) + '" r=".9" fill="' + gold + '" opacity=".6"/>';
            });
            if (len > 10) {
                var x = sx > 0 ? b + 5 : w - b - 5, y1 = Y(62), y2 = sy > 0 ? y1 + len : y1 - len;
                o += '<path d="M' + x + " " + y1 + "V" + y2 + '" stroke="' + gold + '" stroke-width="1.8" stroke-linecap="round" stroke-dasharray="0.1 5" opacity=".7"/>';
            }
        });

        // bulan sabit + bintang kecil di atas, fase bulan di bawah
        o += '<circle cx="' + cx + '" cy="' + a + '" r="12" fill="' + gold + '" mask="url(#' + mk + ')"/>' +
            star(cx + 5, a - 3, 3.6, 1, gold) + phases;

        // bintang tersebar yang berkedip pelan
        var scatter = [
            [0.14, 0.2, 5, paper], [0.86, 0.17, 4, rose], [0.1, 0.36, 3, "#f08a63"], [0.9, 0.42, 5, gold],
            [0.07, 0.58, 4, gold], [0.93, 0.64, 3, paper], [0.12, 0.8, 5, rose], [0.88, 0.84, 3.5, "#f08a63"],
            [0.3, 0.07, 3, gold], [0.7, 0.07, 2.6, paper], [0.32, 0.94, 3, "#f08a63"], [0.68, 0.93, 3, paper]
        ];
        if (h < 420) scatter = scatter.slice(0, 6);
        scatter.forEach(function (t, i) {
            o += star(w * t[0], h * t[1], t[2], 0.9, t[3], i * 0.45);
        });

        svg.setAttribute("width", w);
        svg.setAttribute("height", h);
        svg.setAttribute("viewBox", "0 0 " + w + " " + h);
        svg.innerHTML = o;
    }

    function init(el) {
        if (el.__tarotFrame) return;
        el.__tarotFrame = true;
        el.classList.add("tarot-modal");

        var wrap = document.createElement("div");
        wrap.className = "tarot-frame";
        wrap.setAttribute("aria-hidden", "true");
        var svg = document.createElementNS(NS, "svg");
        wrap.appendChild(svg);
        el.insertBefore(wrap, el.firstChild);

        var uid = ++counter;
        function render() {
            draw(el, svg, uid, !!el.querySelector('[class*="__close"]'));
        }
        // bingkai tetap diam di tempatnya saat isi modal di-scroll
        el.addEventListener("scroll", function () {
            wrap.style.transform = "translateY(" + el.scrollTop + "px)";
        }, { passive: true });

        if (window.ResizeObserver) {
            new ResizeObserver(render).observe(el);
        } else {
            window.addEventListener("resize", render);
        }
        render();
    }

    function initAll(root) {
        (root || document).querySelectorAll(SELECTOR).forEach(init);
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", function () { initAll(); });
    } else {
        initAll();
    }

    // modal yang ditambahkan belakangan (mis. lewat render JavaScript)
    if (window.MutationObserver) {
        new MutationObserver(function (muts) {
            muts.forEach(function (m) {
                m.addedNodes.forEach(function (n) {
                    if (n.nodeType !== 1) return;
                    if (n.matches && n.matches(SELECTOR)) init(n);
                    if (n.querySelectorAll) initAll(n);
                });
            });
        }).observe(document.documentElement, { childList: true, subtree: true });
    }
})();
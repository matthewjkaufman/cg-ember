// Motion helpers for the explainer page. Every value is a pure function of time t (seconds):
// no clocks, no CSS transitions, nothing carried between frames. The renderer calls
// window.seek(t) once per frame, so any frame renders the same on its own.

const M = {};

// Closed-form damped spring, 0 at t=0 settling to 1. freq in Hz, damp 0..1 (below 1 overshoots).
M.spring = (t, freq = 2.2, damp = 0.45) => {
  if (t <= 0) return 0;
  const w = 2 * Math.PI * freq, z = Math.min(damp, 0.999), wd = w * Math.sqrt(1 - z * z);
  return 1 - Math.exp(-z * w * t) * (Math.cos(wd * t) + (z * w / wd) * Math.sin(wd * t));
};
M.clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
M.seg = (t, a, b) => M.clamp((t - a) / (b - a));              // 0..1 progress across [a, b]
M.lerp = (a, b, k) => a + (b - a) * k;
M.inOutCubic = k => k < .5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2;

// A parabolic hop from p0 to p1 with its top `lift` px above the straight path.
M.hop = (p0, p1, k, lift) => ({ x: M.lerp(p0.x, p1.x, k), y: M.lerp(p0.y, p1.y, k) - lift * 4 * k * (1 - k) });

// One span per letter, or one per word. Letters sit inside an unbreakable span per word, so
// text that wraps still breaks only between words, exactly where it did before the split.
M.letters = el => {
  const parts = el.textContent.trim().split(/\s+/); el.textContent = '';
  const out = [];
  parts.forEach((w, i) => {
    const word = document.createElement('span'); word.style.cssText = 'display:inline-block;white-space:nowrap';
    for (const c of w) {
      const s = document.createElement('span'); s.className = 'ch'; s.textContent = c;
      word.appendChild(s); out.push(s);
    }
    el.appendChild(word); if (i < parts.length - 1) el.appendChild(document.createTextNode(' '));
  });
  return out;
};
M.words = el => {
  const parts = el.textContent.trim().split(/\s+/); el.textContent = '';
  return parts.map((w, i) => {
    const s = document.createElement('span'); s.className = 'wd'; s.textContent = w;
    el.appendChild(s); if (i < parts.length - 1) el.appendChild(document.createTextNode(' '));
    return s;
  });
};

// A message the person reads. The renderer prints only the text after "PLAIN: ".
M.plain = msg => new Error('PLAIN: ' + msg);

// Shrink an element's font until its text fits maxW wide in at most `lines` lines.
// Throws a plain message when even the smallest size does not fit, rather than clip words.
M.fit = (el, maxW, lines, start, min, lh, what) => {
  el.style.width = maxW + 'px'; el.style.lineHeight = lh;
  let size = start;
  const tooBig = () => el.getBoundingClientRect().height > size * lh * lines + 2 || el.scrollWidth > maxW + 1;
  for (;;) {
    el.style.fontSize = size + 'px';
    if (!tooBig()) return size;
    if (size <= min) break;
    size = Math.max(min, size - Math.max(1, start * 0.03));
  }
  throw M.plain(what + ' is too long to fit on the screen: "' + el.textContent + '". Shorten it and try again.');
};

// The union box of a list of elements (the real width of wrapped text).
M.box = els => {
  const r = els.map(e => e.getBoundingClientRect());
  return { left: Math.min(...r.map(b => b.left)), right: Math.max(...r.map(b => b.right)),
           top: Math.min(...r.map(b => b.top)), bottom: Math.max(...r.map(b => b.bottom)) };
};

// Color helpers: relative luminance and contrast ratio (the WCAG formula).
M.lum = hex => {
  const v = hex.replace('#', ''), n = v.length === 3 ? v.split('').map(c => c + c).join('') : v;
  const ch = [0, 2, 4].map(i => parseInt(n.slice(i, i + 2), 16) / 255)
    .map(c => c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4));
  return 0.2126 * ch[0] + 0.7152 * ch[1] + 0.0722 * ch[2];
};
M.contrast = (a, b) => { const x = M.lum(a), y = M.lum(b); return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05); };
M.bestOn = (bg, choices) => choices.reduce((best, c) => M.contrast(bg, c) > M.contrast(bg, best) ? c : best);

// True when a font with this name is really drawing text, not a stand-in: its text must
// measure differently from both a monospace and a serif fallback.
M.hasFont = name => {
  const c = document.createElement('canvas').getContext('2d'), s = 'mmmmmmmmmmlliWW0123456789';
  return ['monospace', 'serif'].some(f => {
    c.font = `72px ${f}`; const base = c.measureText(s).width;
    c.font = `72px "${name}", ${f}`; return Math.abs(c.measureText(s).width - base) > 0.5;
  });
};

// Fonts and images loaded, layout measured, then the renderer may start.
M.ready = async setup => {
  try {
    await document.fonts.ready;
    await Promise.all([...document.images].map(im => im.complete ? 0 : new Promise(r => { im.onload = im.onerror = r; })));
    await setup();
    window.seek(0); window.__ready = true;
  } catch (e) {
    window.__failed = String(e && e.message || e);
    throw e;
  }
};

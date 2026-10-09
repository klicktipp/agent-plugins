# Craft: a dashboard page that holds up

Requires nothing — no library, no CDN, no other skill. Everything here fits in one HTML file, and
that is the point: a report is opened weeks later, often offline.

## Contents

- The artifact frame
- Colour layer
- Type
- The tile
- Charts in plain SVG
- Interaction
- Layout
- Check before it goes out

## The artifact frame

**Write the page without a document frame.** No `<!DOCTYPE>`, `<html>`, `<head>` or `<body>` — the
artifact environment supplies those, and a second one inside is an error. Start with `<title>` and
`<style>`, then the content. The `<title>` is the name in the tab and the gallery: a short proper
name like "Newsletter report September", not a description.

**Loading is blocked, not merely discouraged.** External scripts are allowed from a few CDNs only,
and stylesheets, images and `fetch` from anywhere else are blocked **without a visible error** — a
chart library from an arbitrary host simply does not load and the page stays empty there. Hence:
SVG by hand, CSS and JS inline, fonts from the fallback chain.

## Colour layer

Define colours **once** as CSS variables and use only the names afterwards. Never a hex colour in
the markup — otherwise there is no second mode.

**As an artifact the viewer has three theme states, not two.** An explicit choice sets
`data-theme="dark"` or `="light"` on the root; the "System" default sets nothing and
`prefers-color-scheme` decides. Writing only the media query builds a page that ignores the toggle.
So three blocks:

```css
/* 1. Light as the base — never defined inside a media block only */
:root {
  color-scheme: light dark;

  --bg:    #f8fafc;  --panel:        #ffffff;
  --grid:  #e2e8f0;  --panel-border: #e2e8f0;
  --text:  #0f172a;  --text-muted:   #64748b;  --text-dim: #94a3b8;

  /* series and states — named by meaning, not by colour */
  --series-open:  #22d3ee;
  --series-click: #34d399;
  --series-bounce:#fb923c;
  --warn:         #fbbf24;
  --danger:       #fb7185;
}

/* 2. System is dark — but not when light was chosen explicitly */
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --bg: #020617;  --panel: #0f172a;
    --grid: #1e293b; --panel-border: #1e293b;
    --text: #ffffff; --text-muted: #94a3b8; --text-dim: #475569;
  }
}

/* 3. Dark chosen explicitly — wins on a light system too */
:root[data-theme="dark"] {
  --bg: #020617;  --panel: #0f172a;
  --grid: #1e293b; --panel-border: #1e293b;
  --text: #ffffff; --text-muted: #94a3b8; --text-dim: #475569;
}
```

`body` needs its own `background: var(--bg)`. A transparent body takes the environment's backdrop and
looks right in one mode and broken in the other.

- **No tone defined only inside a media block** — it would be missing in one of the three states.
- **Accent colours do not switch.** They come from the middle brightness range so they stay legible
  in both modes; a pure `#ff0000` disappears on dark exactly where it should warn.
- **`--series-open`, not `--cyan`.** If the mapping changes, one line changes and the legend stays
  right.
- **`color-scheme`** makes scrollbars and form controls follow.

Check every warning colour **in both modes** before the page goes out.

## Type

```css
--font-data: ui-monospace, SFMono-Regular, Menlo, Consolas,
             'DejaVu Sans Mono', 'Liberation Mono', monospace;
--font-ui:   system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif;
```

**Numbers monospace**, so stacked values compare; for table columns also
`font-variant-numeric: tabular-nums`.

| Where | Value | Why |
| --- | --- | --- |
| Big number in a tile | `letter-spacing: -0.02em`, `font-weight: 700` | large digits otherwise look pulled apart |
| Tile label | `letter-spacing: 0.02em`, `text-transform: uppercase`, small | quiet, clearly a label |
| Running text | normal | do not track what gets read |

**No web fonts.** The chain above looks good on every system and needs no network.

## The tile

```html
<div class="tile">
  <div class="tile-label">Open rate</div>
  <div class="tile-value">42.0<span class="tile-unit">%</span></div>
  <div class="tile-base">1,208 of 2,876</div>
</div>
```

The **third line is not optional** — a percentage without its base cannot be checked, and a tile is
exactly where someone takes it at face value. The unit goes in its own `<span>`, smaller and in
`--text-muted`, so the number dominates.

If a value is unavailable, it says **"not available"** plus half a line why. No dash, no `0 %`.

## Charts in plain SVG

No library — a line chart is about 30 lines.

```
viewBox="0 0 800 300"   fixed inner size, the page scales it
margins: 48 left (axis labels), 16 right, 16 top, 32 bottom
```

**Markup order is stacking order** — SVG has no z-index:

1. grid lines (`--grid`, `stroke-width: 1`) — four or five horizontal, no more
2. axis labels (`--text-dim`, small, monospace)
3. area under the line for a single series: same colour at `opacity: 0.12`
4. the line: `fill="none"`, `stroke-width: 2`, `stroke-linejoin="round"`, `stroke-linecap="round"`
5. the points: `r="3.5"`, filled in the series colour, `stroke="var(--panel)"`, `stroke-width="2"` —
   the background-coloured rim separates points that sit close together
6. the invisible hit areas for hover

**No interpolation between dates that have nothing to do with each other.** Sends are single events:
straight segments, no Bézier smoothing. A curve claims a trend that does not exist.

**One point is not a trend.** Under four sends, drop the chart and show the table.

**The hit area.** A point at `r="3.5"` is hard to hit with a mouse and impossible with a finger:

```html
<circle cx="..." cy="..." r="14" fill="transparent"
        tabindex="0" role="button"
        aria-label="14 March: open rate 42.0 percent, 1208 of 2876"/>
```

The `aria-label` is also the keyboard answer: tabbing through hears exactly what hovering reads.

## Interaction

- **`pointerover`/`pointerout`, not `mouseover`** — covers mouse, pen and touch in one handler.
- **Every mouse action has a keyboard equivalent.** What appears on hover appears on `focus`.

```js
const show = (el) => { /* position and fill the tooltip */ };
pt.addEventListener('pointerover', () => show(pt));
pt.addEventListener('focus',       () => show(pt));
pt.addEventListener('pointerout',  hide);
pt.addEventListener('blur',        hide);
```

- **Announce changes.** A toggle between open and click rate changes the picture without a screen
  reader noticing — unless there is a live region:
  `<div aria-live="polite" class="sr-only">Now showing the click rate.</div>`
- **State on the element, not in a class alone.** A toggle carries `aria-pressed="true|false"`, a
  collapsible panel `aria-expanded`. CSS may style on `[aria-pressed="true"]` so looks and meaning
  cannot drift apart.
- **The tooltip shows what the chart cannot**: the exact value, the base and the date. It does not
  repeat the label beside it.

## Layout

- **One column, read top to bottom**: header → tiles → chart → table → footer.
- Tiles in `display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr))` — adapts
  without breakpoints.
- **Maximum reading width** for the page (about 1200px), centred.
- The table may scroll in its own `overflow-x: auto` container. **The page may not.**

## Check before it goes out

1. `document.documentElement.scrollWidth <= window.innerWidth` at **1440×900 and 1920×1080**. Fix by
   removing content or tightening spacing — **never** `overflow: hidden`, an inner scroller or
   smaller type.
2. Switch both modes; warning colours legible in **both**.
3. Tab through: every data point reachable, focus visible.
4. Every percentage has its base beside it.
5. No `NaN`, no `Infinity`, no `0 %` at `sentCount: 0`.
6. Search the finished HTML for `http://` and `https://` — nothing but the links into the app may
   load.

**"Looks good" is not a check.** Say separately what you measured and what you merely looked at.

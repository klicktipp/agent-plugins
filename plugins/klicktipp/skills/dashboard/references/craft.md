# Handwerk: eine Dashboard-Seite, die etwas hermacht

Diese Datei ist die Gestaltungsseite von `dashboard`. Sie setzt **nichts** voraus — keine
Bibliothek, kein CDN, keinen weiteren Skill. Alles hier lässt sich in einer einzigen HTML-Datei
umsetzen, und genau das ist der Punkt: ein Report wird Wochen später geöffnet, oft ohne Netz.

## Inhalt

- 0. Was ein Artifact von einer HTML-Datei unterscheidet
- 1. Der Farb-Layer
- 2. Schrift
- 3. Die Kachel
- 4. Diagramme in reinem SVG
- 5. Interaktion
- 6. Layout
- 7. Prüfen, bevor es rausgeht

## 0. Was ein Artifact von einer HTML-Datei unterscheidet

**Schreib die Seite ohne Dokumentrahmen.** Kein `<!DOCTYPE>`, kein `<html>`, kein `<head>`, kein
`<body>` — die Artifact-Umgebung setzt diesen Rahmen selbst, und ein zweiter darin ist ein Fehler.
Fang direkt mit `<title>` und `<style>` an, dann kommt der Inhalt. Der `<title>` ist der Name in
Tab und Galerie: ein kurzer Eigenname wie „Newsletter-Report September", keine Beschreibung.

**Nachladen ist gesperrt, nicht nur unerwünscht.** Die Artifact-Umgebung erlaubt externe Skripte
nur von wenigen CDNs und blockiert Stylesheets, Bilder und `fetch` von überall sonst — **ohne
sichtbaren Fehler**. Eine Diagrammbibliothek von einem beliebigen Host lädt also nicht, und die
Seite bleibt an dieser Stelle einfach leer. Das ist der zweite Grund für alles Folgende: SVG von
Hand, CSS und JS inline, Schriften aus der Fallback-Kette.

**Das Ergebnis muss unter 16 MB bleiben** — bei einem Report nie ein Thema, außer jemand bettet
Bilder als `data:`-URI ein.

## 1. Der Farb-Layer

Definier Farben **einmal** als CSS-Variablen und benutze danach nur noch die Namen. Nie eine
Hex-Farbe mitten im Markup — sonst gibt es keinen zweiten Modus mehr.

**Als Artifact hat der Betrachter drei Theme-Zustände, nicht zwei.** Eine ausdrückliche Wahl setzt
`data-theme="dark"` oder `data-theme="light"` auf das Wurzelelement; die Voreinstellung „System"
setzt gar nichts, dort entscheidet allein `prefers-color-scheme`. Wer nur die Media-Query schreibt,
baut eine Seite, die den Umschalter ignoriert. Deshalb **drei** Blöcke:

```css
/* 1. Hell als Grundlage — nie nur in einem Media-Block definiert */
:root {
  color-scheme: light dark;

  --bg:    #f8fafc;  --panel:        #ffffff;
  --grid:  #e2e8f0;  --panel-border: #e2e8f0;
  --text:  #0f172a;  --text-muted:   #64748b;  --text-dim: #94a3b8;

  /* Serien und Zustände — nach Bedeutung benannt, nicht nach Farbe */
  --series-open:  #22d3ee;  /* Öffnungen  */
  --series-click: #34d399;  /* Klicks     */
  --series-bounce:#fb923c;  /* Bounces    */
  --warn:         #fbbf24;  /* Achtung    */
  --danger:       #fb7185;  /* Schwelle überschritten */
}

/* 2. System steht auf dunkel — aber nicht, wenn hell ausdrücklich gewählt wurde */
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --bg: #020617;  --panel: #0f172a;
    --grid: #1e293b; --panel-border: #1e293b;
    --text: #ffffff; --text-muted: #94a3b8; --text-dim: #475569;
  }
}

/* 3. Dunkel ausdrücklich gewählt — gewinnt auch auf einem hellen System */
:root[data-theme="dark"] {
  --bg: #020617;  --panel: #0f172a;
  --grid: #1e293b; --panel-border: #1e293b;
  --text: #ffffff; --text-muted: #94a3b8; --text-dim: #475569;
}
```

Und **`body` braucht eine eigene Hintergrundfarbe** (`background: var(--bg)`). Ein durchsichtiger
Body übernimmt den Untergrund der Umgebung — die Seite sieht dann in einem Modus richtig aus und
im anderen wie ein Fehler.

Vier Dinge, die diese Zeilen richtig machen:

- **Kein Ton ist nur in einem Media-Block definiert.** Sonst fehlt er in einem der drei Zustände.
- **Die Akzentfarben wechseln nicht mit.** Cyan, Grün, Orange, Bernstein und Rosé sind in beiden
  Modi lesbar — das ist der Grund, warum sie aus dem mittleren Helligkeitsbereich stammen und nicht
  aus dem satten. Ein reines `#ff0000` verschwindet auf Dunkel genau dort, wo es warnen soll.
- **`--series-open` statt `--cyan`.** Wenn die Zuordnung sich ändert, ändert sich eine Zeile, und
  die Legende bleibt richtig.
- **`color-scheme`** sorgt dafür, dass auch Scrollbalken und Formularelemente mitziehen.

Prüf jede Warnfarbe **in beiden Modi**, bevor die Seite rausgeht. Eine Schwellenwertfarbe, die nur
hell funktioniert, ist schlimmer als keine.

## 2. Schrift

```css
--font-data: ui-monospace, SFMono-Regular, Menlo, Consolas,
             'DejaVu Sans Mono', 'Liberation Mono', monospace;
--font-ui:   system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif;
```

**Zahlen monospace.** Untereinanderstehende Werte sollen sich vergleichen lassen; mit
Proportionalschrift springen die Spalten. Für Tabellenspalten zusätzlich
`font-variant-numeric: tabular-nums`.

Feinheiten, die den Unterschied zwischen „gebaut" und „gestaltet" ausmachen:

| Wo | Wert | Warum |
| --- | --- | --- |
| Große Zahl in der Kachel | `letter-spacing: -0.02em`, `font-weight: 700` | Große Ziffern wirken sonst auseinandergerissen |
| Kachel-Beschriftung | `letter-spacing: 0.02em`, `text-transform: uppercase`, klein | Ruhig, klar als Etikett erkennbar |
| Fließtext | normal | Nicht tracken, was gelesen wird |

**Keine Webfonts laden.** Die Fallback-Kette oben sieht auf jedem System gut aus und braucht kein
Netz.

## 3. Die Kachel

Eine Kennzahl-Kachel hat drei Ebenen, immer in derselben Reihenfolge:

```html
<div class="tile">
  <div class="tile-label">Öffnungsrate</div>
  <div class="tile-value">42,0<span class="tile-unit">%</span></div>
  <div class="tile-base">1.208 von 2.876</div>
</div>
```

Die **dritte Zeile ist nicht optional**. Eine Prozentzahl ohne Basis ist nicht prüfbar, und die
Kachel ist genau der Ort, an dem jemand sie für bare Münze nimmt. Die Einheit kommt in ein eigenes
`<span>`, kleiner und in `--text-muted` — dann dominiert die Zahl.

Ist ein Wert nicht verfügbar, steht dort **„nicht verfügbar"** und eine halbe Zeile warum. Kein
Strich, kein `0 %`, kein `–`.

## 4. Diagramme in reinem SVG

Ohne Bibliothek, von Hand — für ein Liniendiagramm sind das ungefähr 30 Zeilen.

```
viewBox="0 0 800 300"   Feste Innenmaße, außen skaliert die Seite.
Rand: 48 links (Achsenbeschriftung), 16 rechts, 16 oben, 32 unten.
```

**Die Reihenfolge der Elemente ist die Reihenfolge im Markup** — SVG kennt kein z-index:

1. Gitterlinien (`--grid`, `stroke-width: 1`) — vier bis fünf waagerechte, mehr nicht
2. Achsenbeschriftung (`--text-dim`, klein, monospace)
3. Fläche unter der Linie, wenn es *eine* Serie ist: dieselbe Farbe mit `opacity: 0.12`
4. Die Linie: `fill="none"`, `stroke-width: 2`, `stroke-linejoin="round"`, `stroke-linecap="round"`
5. Die Punkte: `r="3.5"`, gefüllt in Serienfarbe, `stroke="var(--panel)"`, `stroke-width="2"` —
   der Rand in Hintergrundfarbe trennt Punkte, die dicht beieinanderliegen
6. Die unsichtbaren Trefferflächen für Hover, siehe unten

**Keine Interpolation zwischen Terminen, die nichts miteinander zu tun haben.** Aussendungen sind
Einzelereignisse: gerade Segmente, keine Bézier-Glättung. Eine geschwungene Kurve behauptet einen
Verlauf, den es nicht gibt.

**Ein Punkt allein ist kein Verlauf.** Unter vier Aussendungen: lass das Diagramm weg und zeig die
Tabelle.

### Die Trefferfläche

Ein Punkt mit `r="3.5"` ist mit der Maus kaum zu treffen und mit dem Finger gar nicht. Leg über
jeden Datenpunkt einen unsichtbaren, großzügigen Bereich:

```html
<circle cx="..." cy="..." r="14" fill="transparent"
        tabindex="0" role="button"
        aria-label="14. März: Öffnungsrate 42,0 Prozent, 1208 von 2876"/>
```

Das `aria-label` ist zugleich die Tastatur-Antwort: wer mit Tab durchgeht, hört genau das, was ein
anderer im Tooltip liest.

## 5. Interaktion

**`pointerover` / `pointerout`, nicht `mouseover`.** Deckt Maus, Stift und Touch mit einem
Handler ab.

**Jede Mausaktion hat eine Tastatur-Entsprechung.** Was per Hover erscheint, erscheint auch bei
`focus`. Ein Report wird weitergereicht.

```js
const show = (el) => { /* Tooltip positionieren und füllen */ };
pt.addEventListener('pointerover', () => show(pt));
pt.addEventListener('focus',       () => show(pt));
pt.addEventListener('pointerout',  hide);
pt.addEventListener('blur',        hide);
```

**Änderungen ansagen.** Ein Umschalter zwischen Öffnungs- und Klickrate ändert das Bild, ohne dass
ein Screenreader etwas merkt — außer es gibt eine Live-Region:

```html
<div aria-live="polite" class="sr-only">Zeigt jetzt die Klickrate.</div>
```

**Zustand am Element, nicht in einer Klasse allein.** Ein Umschalter trägt `aria-pressed="true|false"`,
ein aufklappbares Panel `aria-expanded`. Das CSS darf auf `[aria-pressed="true"]` stylen — dann
können Aussehen und Bedeutung nicht auseinanderlaufen.

**Der Tooltip zeigt, was das Diagramm nicht kann**: den exakten Wert, die Basis und das Datum. Er
wiederholt nicht die Beschriftung, die daneben steht.

## 6. Layout

- **Eine Spalte, von oben nach unten gelesen**: Kopf → Kacheln → Diagramm → Tabelle → Fußzeile.
  Kein Raster, in dem das Auge suchen muss, wo es anfängt.
- Kacheln in `display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr))` — passt
  sich ohne Breakpoints an.
- **Maximale Lesebreite** für die Seite (etwa 1200px), zentriert. Eine Tabelle über 2560px ist
  unlesbar.
- Die Tabelle darf in einem eigenen `overflow-x: auto`-Container scrollen. **Die Seite nicht.**

## 7. Prüfen, bevor es rausgeht

Sechs Punkte, die sich in zwei Minuten prüfen lassen und die häufigsten Fehler abfangen:

1. `document.documentElement.scrollWidth <= window.innerWidth` bei **1440×900 und 1920×1080**.
   Repariert wird durch Weglassen oder engere Abstände — **nie** mit `overflow: hidden`, einem
   inneren Scroller oder kleinerer Schrift. Das versteckt den Fehler.
2. Beide Modi umschalten, Warnfarben in **beiden** lesbar.
3. Mit Tab durch die Seite: jeder Datenpunkt erreichbar, Fokus sichtbar.
4. Jede Prozentzahl hat ihre Basis daneben.
5. Kein `NaN`, kein `Infinity`, kein `0 %` bei `sentCount: 0`.
6. Suche nach `http://` und `https://` im fertigen HTML — außer den Links in die App darf nichts
   nachgeladen werden.

**„Sieht gut aus" ist keine Prüfung.** Sag getrennt, was du gemessen und was du nur angesehen hast.

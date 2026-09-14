# Überschrift (`heading`)

Die Gliederung einer E-Mail. Eine Überschrift ist kein großgeschriebener Absatz: sie strukturiert, und Empfänger überfliegen eine Mail an ihr entlang.

Familie **Text**. Modultyp im Dokument: `mailup-bee-newsletter-modules-heading`.

## Werkzeuge

| Anlegen | `email-heading-add` |
| --- | --- |
| Ändern | `email-text-write` |
| Entfernen | `email-block-remove` |
| Verschieben | `email-block-move` |
| Aussehen | `email-block-style-write` (Innenabstand, Ausrichtung, Sichtbarkeit je Gerät) |

## Felder

| Feld | gespeichert unter |
| --- | --- |
| `text` | `descriptor.heading.text` |
| `level` | `descriptor.heading.title` (der Name täuscht: dort steht die Ebene) |

Beide Werkzeuge — Anlegen und Ändern — nehmen genau diese Felder.

## Worauf zu achten ist

Die Ebene ist **Struktur, nicht Größe.** `h1` ist die eine Schlagzeile der Mail, `h2` ein Abschnitt,
`h3` ein Unterabschnitt — wie groß die Überschrift *aussieht*, steht dagegen im Markup. Ein
Newsletter mit mehreren Abschnitten will `h2`; das ist auch die Ebene, die echte Newsletter am
häufigsten benutzen.

Erlaubt sind genau `h1`, `h2` und `h3` — mehr kennt der Editor nicht, und das Schema des Anbieters
sagt dasselbe. Ein anderer Wert wird abgelehnt, ein **leerer** erst recht: die Ebene ist ein
Strukturwert, den der Editor liest, und geleert hat sie ihn schon zum Absturz gebracht.

Ohne Angabe legt `email-heading-add` eine `h1` an.

Die Wörter stehen in `text`, **nicht** in `html` — die einzige Textart, die aus der Reihe fällt. Der Text steckt dort in `<span>`s.

## Gestaltung

`email-block-style-write` setzt, wie bei jedem Baustein: Innenabstand auf vier Seiten, Ausrichtung des Inhalts und die Sichtbarkeit je Gerät (`hideOnMobile`, `hideOnDesktop`).

## Beim HTML-Import

Der Baustein übersteht einen HTML-Import als er selbst.

Das gilt **nur** für den Import (`email-content-import`), nicht fürs Ändern: dort wird nichts konvertiert.

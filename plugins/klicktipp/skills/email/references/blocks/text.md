# Text (`text`)

Ein Fließtextbaustein. Inhaltlich dasselbe wie ein Absatz — beide heißen im Produkt „Text" und tragen ihr Markup in `html`.

Familie **Text**. Modultyp im Dokument: `mailup-bee-newsletter-modules-text`.

## Werkzeuge

| Anlegen | `email-text-add` |
| --- | --- |
| Ändern | `email-text-write` |
| Entfernen | `email-block-remove` |
| Verschieben | `email-block-move` |
| Aussehen | `email-block-style-write` (Innenabstand, Ausrichtung, Sichtbarkeit je Gerät) |

## Felder

| Feld | gespeichert unter |
| --- | --- |
| `html` | `descriptor.text.html` |

Beide Werkzeuge — Anlegen und Ändern — nehmen genau diese Felder.

## Worauf zu achten ist

Zwei gespeicherte Arten, ein Produktbegriff: `text` und `paragraph` sind für einen Leser dasselbe. Wenn du die Wahl hast, nimm `paragraph` — die Art, die in echten Newslettern überwiegt.

## Gestaltung

`email-block-style-write` setzt, wie bei jedem Baustein: Innenabstand auf vier Seiten, Ausrichtung des Inhalts und die Sichtbarkeit je Gerät (`hideOnMobile`, `hideOnDesktop`).

## Beim HTML-Import

Der Baustein übersteht einen HTML-Import als er selbst.

Das gilt **nur** für den Import (`email-content-import`), nicht fürs Ändern: dort wird nichts konvertiert.

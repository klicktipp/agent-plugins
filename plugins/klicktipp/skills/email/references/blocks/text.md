# Text (`text`)

Ein Fließtextbaustein. Inhaltlich dasselbe wie ein Absatz — beide heißen im Produkt „Text" und tragen ihr Markup in `html`.

Familie **Text**. Modultyp im Dokument: `mailup-bee-newsletter-modules-text`.

## Werkzeuge

| Anlegen | `add-email-editor-text` |
| --- | --- |
| Ändern | `update-email-editor-text` |
| Entfernen | `remove-email-editor-block` |
| Verschieben | `move-email-editor-block` |
| Aussehen | `update-email-editor-block-style` (Innenabstand, Ausrichtung, Sichtbarkeit je Gerät) |

## Felder

| Feld | gespeichert unter |
| --- | --- |
| `html` | `descriptor.text.html` |

Beide Werkzeuge — Anlegen und Ändern — nehmen genau diese Felder.

## Worauf zu achten ist

Zwei gespeicherte Arten, ein Produktbegriff: `text` und `paragraph` sind für einen Leser dasselbe. Wenn du die Wahl hast, nimm `paragraph` — die Art, die in echten Newslettern überwiegt.

## Gestaltung

`update-email-editor-block-style` setzt, wie bei jedem Baustein: Innenabstand auf vier Seiten, Ausrichtung des Inhalts und die Sichtbarkeit je Gerät (`hideOnMobile`, `hideOnDesktop`).

## Beim HTML-Import

Der Baustein übersteht einen HTML-Import als er selbst.

Das gilt **nur** für den Import (`replace-email-editor-content-from-html`), nicht fürs Ändern: dort wird nichts konvertiert.

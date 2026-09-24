# Liste (`list`)

Eine Aufzählung, geordnet oder ungeordnet. Für alles, was ein Empfänger überfliegen soll, statt es zu lesen.

Familie **Text**. Modultyp im Dokument: `mailup-bee-newsletter-modules-list`.

## Werkzeuge

| Anlegen | `add-email-editor-list` |
| --- | --- |
| Ändern | `update-email-editor-text` |
| Entfernen | `remove-email-editor-block` |
| Verschieben | `move-email-editor-block` |
| Aussehen | `update-email-editor-block-style` (Innenabstand, Ausrichtung, Sichtbarkeit je Gerät) |

## Felder

| Feld | gespeichert unter |
| --- | --- |
| `html` | `descriptor.list.html` |

Beide Werkzeuge — Anlegen und Ändern — nehmen genau diese Felder.

## Worauf zu achten ist

Das `html` ist das vollständige `<ul>`- oder `<ol>`-Markup, nicht nur die Einträge.

## Gestaltung

`update-email-editor-block-style` setzt, wie bei jedem Baustein: Innenabstand auf vier Seiten, Ausrichtung des Inhalts und die Sichtbarkeit je Gerät (`hideOnMobile`, `hideOnDesktop`).

## Beim HTML-Import

Der Baustein übersteht einen HTML-Import als er selbst.

Das gilt **nur** für den Import (`replace-email-editor-content-from-html`), nicht fürs Ändern: dort wird nichts konvertiert.
